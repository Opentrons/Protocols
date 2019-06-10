from opentrons import labware, instruments, modules, robot
from opentrons.data_storage import database

metadata = {
    'protocolName': 'Custom Cassette Plate Filling',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# custom cassette definition
cassette_name = '24-well-cassette'
database.delete_container(cassette_name)
if cassette_name not in labware.list():
    labware.create(
        cassette_name,
        grid=(12, 2),
        spacing=(8.5, 47.7),
        diameter=3,
        depth=18.8,
        volume=508
    )


def run_custom_protocol(number_of_cassettes_to_fill: int = 9):

    # labware and module load
    cassettes = [labware.load(cassette_name, str(slot))
                 for slot in range(1, 1+number_of_cassettes_to_fill)]
    tempdeck = modules.load('tempdeck', '10')
    if not robot.is_simulating():
        tempdeck.set_temperature()
        tempdeck.wait_for_temp()
    tubes = labware.load(
                'opentrons-aluminum-block-2ml-eppendorf',
                '10',
                share=True)
    tips = labware.load('tiprack-1000ul', '11')

    # pipette
    p1000 = instruments.P1000_Single(mount='right', tip_racks=[tips])

    # source setup
    sources = tubes.wells('A1', length=13)

    # destination setup
    dest_inds = [ind for ind in range(1, 24, 2)] + [10]

    # transfer to each cassette
    for source, dest_ind in zip(sources, dest_inds):
        dests = [cassette.wells(dest_ind).top() for cassette in cassettes]
        p1000.distribute(100, source, dests, disposal_vol=50)
