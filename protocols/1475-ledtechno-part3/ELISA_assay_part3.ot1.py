from opentrons import containers, instruments

metadata = {
    'protocolName': 'ELISA Assay',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
    }

plate_name = 'greiner-bio-one-96-flat'
containers.create(
    plate_name,
    grid=(8, 12),
    spacing=(9, 9),
    diameter=7,
    depth=10.9)

sample_plate = 'greiner-bio-one-24-well-plate'
containers.create(
    sample_plate,
    grid=(4, 6),
    spacing=(13.5, 19.5),
    diameter=16.3,
    depth=16.5)

# labware setup
plate = containers.load(plate_name, 'C2')
sample_plates = [containers.load(sample_plate, slot, 'Samples')
                 for slot in ['A2', 'A3', 'B2', 'B3']]
standards = containers.load(sample_plate, 'B1', 'Standards')
trough = containers.load('trough-12row', 'A1')
tiprack_300 = containers.load('tiprack-200ul', 'A2')
tiprack_100 = containers.load('tiprack-200ul', 'C1')
liquid_trash = containers.load('trash-box', 'D2')
trash = containers.load('trash-box', 'D3')


# instruments setup
m300 = instruments.Pipette(
    axis='a',
    name='p300multi',
    max_volume=300,
    min_volume=30,
    channels=8,
    trash_container=trash,
    tip_racks=[tiprack_300])

p100 = instruments.Pipette(
    axis='b',
    name='p100single',
    max_volume=100,
    min_volume=10,
    channels=1,
    trash_container=trash,
    tip_racks=[tiprack_100])

# reagent setup
wash_buffer = trough.wells('A1')

# wash plate 3 times with wash buffer
wash_buffer_tracker = wash_buffer.max_volume()
for cycle in range(3):
    m300.pick_up_tip()
    for row in plate.rows():
        if wash_buffer_tracker < 300 * 8:
            wash_buffer = next(wash_buffer)
            wash_buffer_tracker = wash_buffer.max_volume()
        m300.transfer(300, wash_buffer, row.top(), new_tip='never')
        wash_buffer_tracker -= 300 * 8
    for row in plate.rows():
        m300.transfer(300, row, liquid_trash.top(), new_tip='never')
    m300.drop_tip()

m300.delay(minutes=2)

plate_layout = []
for index1, index2 in zip(range(0, 12, 2), range(1, 13, 2)):
    for col in plate.cols():
        plate_layout.append(col.wells(index1))
        plate_layout.append(col.wells(index2))

"""
Transfer standard samples
"""
standard_sources = [well for well in standards.wells()][:18]

for source, dest in zip(standard_sources, plate_layout[:18]):
    p100.transfer(100, source, dest)

"""
Transfer test samples
"""
sample_sources = [well for plate in sample_plates
                  for well in plate.wells()][:78]
sample_dests = plate_layout[18:]

for source, dest in zip(sample_sources, sample_dests):
    p100.transfer(100, source, dest)
