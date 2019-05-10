from opentrons import labware, instruments, modules, robot
from opentrons.legacy_api.modules import magdeck

metadata = {
    'protocolName': 'NGS Prep',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

"""Controlling two of the same module in the protocol:
1. SSH into robot
2. run $ls /dev/tty*
   you are looking for two values with the format /dev/ttyACM*
   you will use those values in line 26 and 27.
If you need to know which magdeck is hooked up to which port:
1. unplug one of the modules
2. run $ls /dev/tty* : the results correlates to the module that is plugged in
3. plug the other module in and run ls /dev/tty* again, you will be able to
   know the value of the second module
"""

# defining two Magnetic Modules
magdeck1 = magdeck.MagDeck()
magdeck2 = magdeck.MagDeck()

magdeck1._port = '/dev/ttyACM3'
magdeck2._port = '/dev/ttyACM2'

if not robot.is_simulating():
    magdeck1.connect()
    magdeck2.connect()

# custom labware
plate_1_2_name = 'Biorad-Hardshell-High-96'
if plate_1_2_name not in labware.list():
    labware.create(plate_1_2_name,
                   grid=(12, 8),
                   spacing=(9, 9),
                   diameter=5.5,
                   depth=19.85,
                   volume=350)

plate_3_name = 'Biorad-Hardshell-Low-96'
if plate_3_name not in labware.list():
    labware.create(plate_3_name,
                   grid=(12, 8),
                   spacing=(9, 9),
                   diameter=5.46,
                   depth=14.81,
                   volume=200)

tips10_name = 'TipOne-10ul-Filter'
if tips10_name not in labware.list():
    labware.create(tips10_name,
                   grid=(12, 8),
                   spacing=(9, 9),
                   diameter=5,
                   depth=20)

tips200_name = 'TipOne-200ul-Filter'
if tips200_name not in labware.list():
    labware.create(tips200_name,
                   grid=(12, 8),
                   spacing=(9, 9),
                   diameter=5,
                   depth=20)

# load labware and modules
magdeck1 = modules.load('magdeck', '1')
plate1 = labware.load(plate_1_2_name, '1', share=True)
magdeck2 = modules.load('magdeck', '4')
plate2 = labware.load(plate_1_2_name, '4', share=True)
plate3 = labware.load(plate_3_name, '2')
tips10 = [labware.load(tips10_name, slot) for slot in ['3', '6', '9', '11']]
tips200 = labware.load(tips200_name, '10')
trough = labware.load('trough-12row', '5')
ethanol_tips = labware.load(tips200_name, '7')
TE_tips = labware.load(tips10_name, '8')

# pipettes
m10 = instruments.P10_Multi(mount='right', tip_racks=tips10)
m300 = instruments.P300_Multi(mount='left', tip_racks=[tips200])

# reagent setup
beads = trough.wells('A1')
ethanol = trough.wells('A2')
TE = trough.wells('A3')
liquid_trash = trough.wells('A12')


def run_custom_protocol(number_of_sample_columns: int = 12):
    # setup samples according to input number of sample columns
    plate1_samples = plate1.rows('A')[0:number_of_sample_columns]
    plate2_samples = plate2.rows('A')[0:number_of_sample_columns]
    plate3_samples = plate3.rows('A')[0:number_of_sample_columns]

    # function for ethanol wash
    def ethanol_wash(discard=False):
        m300.transfer(200,
                      ethanol,
                      [well.top() for well in plate2_samples])

        # incubate for 20 seconds
        m300.delay(seconds=20)

        # transfer out ethanol supernatant with corresponding tip
        for tip, samp in zip(ethanol_tips.rows('A'), plate2_samples):
            m300.pick_up_tip(tip)
            m300.transfer(200, samp, liquid_trash, new_tip='never')
            if discard is False:
                m300.return_tip()
            else:
                m300.drop_tip()

    # function for TE transfer
    def TE_transfer(discard=False, mix=False):
        # disengage magnetic module
        magdeck2.disengage()

        # distribute TE buffer and mix
        for samp in plate2_samples:
            m10.pick_up_tip()
            m10.transfer(10, TE, samp, new_tip='never')
            m10.mix(10, m10.max_volume, samp)
            m10.drop_tip()

        # incubate plate 2 on engaged magnet for 5 minutes
        magdeck2.engage(height=18)
        m10.delay(minutes=1)

        # transfer to plate 3
        for tip, source, dest in zip(TE_tips, plate2_samples, plate3_samples):
            m10.pick_up_tip(tip)
            m10.transfer(10, source, dest, new_tip='never')
            if mix is True:
                m10.mix(10, m10.max_volume, dest)
            if discard is False:
                m10.return_tip()
            else:
                m10.drop_tip()

    # mix beads before distributing
    m10.pick_up_tip()
    m10.mix(10, m10.max_volume, beads)
    m10.drop_tip()

    # distribute beads to plate 1
    for s in plate1_samples:
        m10.pick_up_tip()
        m10.transfer(15,
                     beads,
                     s.top(),
                     new_tip='never')
        m10.drop_tip()

    # distribute beads to plate 2
    m10.transfer(5,
                 beads,
                 [well.top() for well in plate2_samples])

    # incubate plate 1 on engaged magnet for 5 minutes
    magdeck1.engage(height=18)
    m10.delay(minutes=5)

    # transfer plate 1 supernatant to corresponding well in plate 2
    for source, dest in zip(plate1_samples, plate2_samples):
        m10.pick_up_tip()
        m10.transfer(15, source, dest, new_tip='never')
        m10.mix(10, m10.max_volume, dest)
        m10.drop_tip()

    # incubate plate 2 on engaged magnet for 5 minutes.
    magdeck2.engage(height=18)
    m10.delay(minutes=5)

    # discard supernatant from plate 2
    m10.transfer(20, plate2_samples, liquid_trash, new_tip='always')

    # set slow flow rate for P300 multi-channel pipettes and distribute ethanol
    m300.set_flow_rate(aspirate=50, dispense=100)

    # 3 ethanol washes, drop tip after last wash
    ethanol_wash()
    ethanol_wash()
    ethanol_wash(discard=True)

    # remove any remaining supernatant
    m10.transfer(10, plate2_samples, liquid_trash, new_tip='always')

    robot.pause('Replace 10ul tips before resuming.')
    m10.reset()

    # distribute TE buffer and mix
    TE_transfer()
    TE_transfer(mix=True, discard=True)

    magdeck1.disengage()
    magdeck2.disengage()
