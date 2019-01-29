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
trough = containers.load('trough-12row', 'A1')
tipracks = [containers.load('tiprack-200ul', slot)
            for slot in ['A2', 'B2', 'A3', 'B3']]
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
    tip_racks=tipracks)


# reagent setup
wash_buffer = trough.wells('A1')
detection_antibody = trough.wells('A8')

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
    m300.drop_tip()
    for row in plate.rows():
        m300.transfer(300, row, liquid_trash.top())

m300.pause(minutes=2)

# block plate with blocking buffer
m300.pick_up_tip()
for row in plate.rows():
    m300.transfer(100, detection_antibody, row.top(), new_tip='never')
m300.drop_tip()
