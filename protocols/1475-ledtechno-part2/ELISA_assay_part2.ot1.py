from opentrons import containers, instruments, robot

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
tiprack = containers.load('tiprack-200ul', 'A2')
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
    tip_racks=[tiprack])

p300 = instruments.Pipette(
    axis='b',
    name='p300single',
    max_volume=300,
    min_volume=30,
    channels=1,
    trash_container=trash,
    tip_racks=[tiprack])


def run_custom_protocol():

    # reagent setup
    wash_buffer = trough.wells('A1')
    blocking_buffer = trough.wells('A7')

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

    robot.pause()

    # block plate with blocking buffer
    m300.pick_up_tip()
    for row in plate.rows():
        m300.transfer(200, blocking_buffer, row.top(), new_tip='never')
    m300.drop_tip()
