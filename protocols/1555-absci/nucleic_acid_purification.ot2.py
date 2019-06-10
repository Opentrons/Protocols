from opentrons import labware, instruments, modules, robot
from otcustomizers import StringSelection

metadata = {
    'protocolName': 'Nucleic Acid Purification',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# create custom labware
plate_name = 'Simport-96-deepwell'
if plate_name not in labware.list():
    labware.create(plate_name,
                   grid=(12, 8),
                   spacing=(9, 9),
                   diameter=8,
                   depth=43,
                   volume=2200)

trough_name = 'Axygen-12-row-trough'
if trough_name not in labware.list():
    labware.create(trough_name,
                   grid=(12, 1),
                   spacing=(9, 0),
                   diameter=8,
                   depth=39,
                   volume=22000)

mag_plate_name = 'PlateOne-96-deepwell'
if mag_plate_name not in labware.list():
    labware.create(mag_plate_name,
                   grid=(12, 8),
                   spacing=(9, 9),
                   diameter=8.2,
                   depth=41.3,
                   volume=2000)

# load labware
trough = labware.load(trough_name, '2')
bacteria_plate = labware.load(plate_name, '3', 'bacteria plate')
pur4_plate = labware.load(plate_name, '1', 'plate for PUR4')
tips300 = [labware.load('opentrons-tiprack-300ul', slot)
           for slot in ['5', '6', '7', '9', '10']]
tips50 = labware.load('opentrons-tiprack-300ul', '11')

# module
magdeck = modules.load('magdeck', '4')
mag_plate = labware.load(mag_plate_name, '4', share=True)

# reagent setup
RE1_1 = trough.wells('A1')
L2 = trough.wells('A2')
N3 = trough.wells('A3')
isopropanol = trough.wells('A4')
EtOH = trough.wells('A5')
RE1_2 = trough.wells('A6')
waste = trough.wells('A12')

PUR4 = pur4_plate.wells('A1')


def run_custom_protocol(
        columns_to_process: StringSelection('1', '2', '3', '4',
                                            '5', '6', '7', '8',
                                            '9', '10', '11',
                                            '12') = '12',
        pipettes_type: StringSelection('single', 'multi') = 'multi'):

    num_columns = int(columns_to_process)
    if pipettes_type == 'single':
        pipette50 = instruments.P50_Single(mount='right', tip_racks=tips50)
        pipette300 = instruments.P300_Single(mount='left', tip_racks=tips300)
        bacteria_samples = bacteria_plate.wells('A1', length=8*num_columns)
        mag_samples = mag_plate.wells('A1', length=8*num_columns)
    else:
        pipette50 = instruments.P50_Multi(mount='right', tip_racks=tips50)
        pipette300 = instruments.P300_Multi(mount='left', tip_racks=tips300)
        bacteria_samples = bacteria_plate.rows['A'][0:num_columns]
        mag_samples = mag_plate.rows['A'][0:num_columns]

    # distribute RE1 and mix
    for s in bacteria_samples:
        pipette300.pick_up_tip()
        pipette300.transfer(100, RE1_1, s, new_tip='never')
        pipette300.mix(20, 80, s)
        pipette300.drop_tip()

    # distribute L2 and mix
    for s in bacteria_samples:
        pipette300.pick_up_tip()
        pipette300.transfer(100, L2, s, new_tip='never')
        pipette300.mix(2, 190, s)
        pipette300.drop_tip()

    # incubate for 3 minutes at room temperature
    pipette300.delay(minutes=3)

    # distribute N3 to top of each well to not contaminate tips
    pipette300.distribute(100, N3, [s.top() for s in bacteria_samples])

    robot.pause('Incubate deep-well plate on orbital shaker for 10 minutes '
                'followed by centrifugation to pellet flocculent. Replace '
                'plate on the deck before resuming.')

    # distribute PUR4
    dests = mag_plate.wells('A1', length=8*num_columns)
    pipette50.pick_up_tip(tips50.wells('H12'))
    pipette50.mix(5, 50, PUR4)
    pipette50.distribute(10, PUR4, [d.top() for d in dests], new_tip='never')
    pipette50.drop_tip()

    # transfer liquid from bacteria plate to magnetic plate
    for bac, mag in zip(bacteria_samples, mag_samples):
        pipette300.transfer(240, bac, mag.top())
        pipette300.pick_up_tip()
        pipette300.transfer(165, isopropanol, mag, new_tip='never')
        pipette300.mix(10, 300, mag)
        pipette300.drop_tip()

    # incubate on engaged magnet for 8 minutes
    magdeck.engage(height=18)
    pipette300.delay(minutes=8)

    # transfer out supernatant
    pipette300.transfer(300, mag_samples, waste, new_tip='always')

    # perform 3 EtOH washes
    for _ in range(3):
        pipette300.distribute(200, EtOH, [s.top() for s in mag_samples])
        pipette300.delay(seconds=30)
        pipette300.transfer(300, mag_samples, waste, new_tip='always')

    # allow to dry for 10 minutes
    pipette300.delay(minutes=10)

    # distribute RE1 to top of each well to not contaminate tips
    pipette300.distribute(40, RE1_2, [s.top() for s in mag_samples])

    magdeck.disengage()

    robot.pause('Incubate elution plate at 37°C for 5 minutes followed by 30 '
                'seconds of vortexing to elute plasmid. Resume to finish.')
