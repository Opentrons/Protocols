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
    diameter=6.96,
    depth=10.9
    )

# labware setup
plate = containers.load(plate_name, 'A1')
trough = containers.load('trough-12row', 'B1')
tiprack = containers.load('tiprack-200ul', 'A2')
trash = containers.load('trash-box', 'B2')

# instruments setup
m300 = instruments.Pipette(
    axis='a',
    name='p300multi',
    max_volume=300,
    min_volume=30,
    channels=8,
    trash_container=trash,
    tip_racks=[tiprack])

# reagent setup
coating_antibody = trough.wells('A1')


def run_custom_protocol(coating_volume: float=100):

    m300.distribute(
        100, coating_antibody, plate.rows(), blow_out=coating_antibody)
