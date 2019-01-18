from opentrons import labware, instruments

metadata = {
    'protocolName': 'Multiple Sample Transfer',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
    }

plate_name = 'greiner-bio-one-96-well-u-bottom'
if plate_name not in labware.list():
    labware.create(
        plate_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=6.94,
        depth=10.3
        )

# labware setup
sample_plates = [labware.load('24-well-plate', slot)
                 for slot in ['4', '5']]
plate = labware.load(plate_name, '2')
reagents = labware.load('opentrons-tuberack-2ml-eppendorf', '1')
diluent = labware.load('opentrons-tuberack-50ml', '3')
tiprack = labware.load('tiprack-10ul', '6')
tiprack_300 = labware.load('opentrons-tiprack-300ul', '7')

# instrument setup
p10 = instruments.P10_Single(
    mount='left',
    tip_racks=[tiprack])

p300 = instruments.P300_Single(
    mount='right',
    tip_racks=[tiprack_300])

# reagent setup
reagent_1 = reagents.wells('A1')
reagent_2 = reagents.wells('A2')
reagent_3 = reagents.wells('A3')

samples = [well for plate in sample_plates for well in plate.wells()][:32]
dests = [well for row in plate.rows() for well in row]

# transfer samples in triplicate
for index, sample in enumerate(samples):
    dest = [dests[index + (cycle * len(samples))] for cycle in range(3)]
    p10.distribute(2.5, sample, dest)

# add reagent 1
p10.distribute(
    3,
    reagent_1,
    [well.top() for well in plate.wells()],
    blow_out=reagent_1
    )

p10.delay(minutes=10)

# add reagent 2
p10.distribute(
    3,
    reagent_2,
    [well.top() for well in plate.wells()],
    blow_out=reagent_2
    )

p10.delay(minutes=10)

# add reagent 3
p10.distribute(
    3,
    reagent_3,
    [well.top() for well in plate.wells()],
    blow_out=reagent_1
    )

p10.delay(minutes=30)

# add diluent
p300.transfer(238.5, diluent, [well.top() for well in plate.wells()])
