from opentrons import labware, instruments, modules, robot
from otcustomizers import StringSelection
import math

metadata = {
    'protocolName': 'NGS Library Prep: BP Post Index 1',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# create custom labware
deep_name = 'Zymo-96-deep'
if deep_name not in labware.list():
    labware.create(
        deep_name,
        grid=(12, 8),
        spacing=(8, 8),  # check
        diameter=7,  # check
        depth=31,  # check
        volume=1100)

plate_name = 'MicroAmp-96-PCR'
if plate_name not in labware.list():
    labware.create(
        plate_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=5.49,
        depth=20.1,
        volume=200)

# labware
strips = labware.load('PCR-strip-tall', '2')
tubes_ep = labware.load('opentrons-tuberack-2ml-eppendorf', '3')
tubes_falcon = labware.load('opentrons-tuberack-15ml', '4')
tips200 = labware.load('tiprack-200ul', '7')
sample_tips = labware.load('tiprack-200ul', '9')

# modules
magdeck = modules.load('magdeck', '1')
mag_plate = labware.load(plate_name, '1', share=True)

# pipettes
m300 = instruments.P300_Multi(mount='right', tip_racks=[tips200])
p300 = instruments.P300_Single(mount='left')

# reagent setup
TE = tubes_ep.wells('A1')
ethanol = tubes_falcon.wells('A1', length=6)


def run_custom_protocol(
        beads_strip_column: StringSelection('1', '2', '3', '4', '5', '6', '7',
                                            '8', '9', '10', '11', '12') = '1',
        elution_strip_start_column: StringSelection('1', '2', '3', '4', '5'
                                                    '6', '7', '8', '9', '10',
                                                    '11', '12') = '3'):
    # reagent setup
    beads = strips.columns(beads_strip_column)
    empty_strips = [well for col in
                    strips.columns(elution_strip_start_column, length=2)
                    for well in col]
    TE = tubes_ep.wells('A1')
    ethanol = tubes_falcon.wells('A1')

    # initialize ethanol height trackers, assuming that reagents are filled to
    # 14ml line in standard 15ml tube
    h_track = -18
    pi = math.pi
    r_cyl = 7.52

    # distribute beads and mix:
    beads_dests = [col for col in mag_plate.cols('1', length=3)]
    for dest in beads_dests:
        m300.pick_up_tip()
        m300.transfer(40.6, beads, dest, new_tip='never')
        m300.mix(8, 40, dest)
        m300.drop_tip()

    # first pooling
    for set in range(2):
        for i in range(6):
            tip = sample_tips.wells(set*6+i)
            p300.pick_up_tip(tip)
            pool_ind = set*12+i
            p300.transfer(91.4,
                          mag_plate.wells(pool_ind+6),
                          mag_plate.wells(pool_ind),
                          new_tip='never')
            p300.return_tip()

    # move pools 7-12 directly after pools 1-6
    for tip, source, dest in zip(sample_tips.wells(6, length=6),
                                 mag_plate.wells(12, length=6),
                                 mag_plate.wells(6, length=6)):
        p300.pick_up_tip(tip)
        p300.transfer(182.8, source, dest, new_tip='never')
        p300.return_tip()

    p300.delay(minutes=5)
    robot._driver.run_flag.wait()
    magdeck.engage(height=18)
    p300.delay(minutes=10)

    new_pools = [well for well in mag_plate.wells(0, length=12)]
    # transfer out supernatant
    for tip, well in zip(sample_tips.wells(), new_pools):
        p300.pick_up_tip(tip)
        p300.transfer(182.8,
                      well,
                      p300.trash_container.top(),
                      new_tip='never',
                      blow_out=True)
        p300.return_tip()

    ethanol_tip = sample_tips.wells('H11')
    # 3 ethanol washes
    for _ in range(3):
        # calculate ethanol height to aspirate from and transfer
        p300.pick_up_tip(ethanol_tip)
        for n in new_pools:
            p300.transfer(200,
                          ethanol.top(h_track),
                          n.top(),
                          new_tip='never')
            h_track -= 200/(pi*(r_cyl**2))
        p300.return_tip()

        # incubate for 30 seconds
        p300.delay(seconds=30)

        # transfer out ethanol with corresponding tip
        for tip, well in zip(sample_tips.wells(), new_pools):
            p300.pick_up_tip(tip)
            p300.transfer(200,
                          well,
                          p300.trash_container.top(),
                          new_tip='never',
                          blow_out=True)
            p300.return_tip()

    # dry pellet
    p300.delay(minutes=8)
    robot._driver.run_flag.wait()

    # resuspend in TE
    magdeck.disengage()
    TE_tip = sample_tips.wells('H12')
    p300.pick_up_tip(TE_tip)
    p300.distribute(50.5, TE, [n.top() for n in new_pools], new_tip='never')
    p300.drop_tip()
    p300.delay(minutes=2)
    robot._driver.run_flag.wait()
    magdeck.engage(height=18)
    p300.delay(minutes=5)

    # transfer to new strips
    for tip, source, dest in zip(sample_tips.wells(), new_pools, empty_strips):
        p300.pick_up_tip(tip)
        p300.transfer(50, source, dest, new_tip='never')
        p300.drop_tip()
