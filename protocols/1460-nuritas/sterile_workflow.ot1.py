from opentrons import containers, instruments
from otcustomizers import FileInput, StringSelection

metadata = {
    'protocolName': 'Sterile Workflow',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Protocol Library'
    }

aluminum_block = 'opentrons-aluminum-block-2ml-eppendorf'
containers.create(
    aluminum_block,
    grid=(4, 6),
    spacing=(17.25, 17.25),
    diameter=9,
    depth=38.5
    )

aluminum_block = 'opentrons-aluminum-block-2ml-screwcap'
containers.create(
    aluminum_block,
    grid=(4, 6),
    spacing=(17.25, 17.25),
    diameter=9,
    depth=42
    )

example_csv = """
979
976
953
966
961
986
"""


def csv_to_list(csv_string):
    info_list = [float(line) for line in csv_string.splitlines() if line]
    return info_list


def run_custom_protocol(
        csv_file: FileInput=example_csv,
        tuberack_type: StringSelection(
            'opentrons-aluminum-block-2ml-eppendorf',
            'opentrons-aluminum-block-2ml-screwcap')=
        'opentrons-aluminum-block-2ml-eppendorf'
        ):

    # container setup
    plates = [containers.load('96-flat', slot)
              for slot in ['A1', 'B1']]
    tuberack = containers.load(tuberack_type, 'A2')
    trough = containers.load('trough-12row', 'B2')
    tiprack_50 = containers.load('tiprack-200ul', 'C2')
    tiprack_1000 = containers.load('tiprack-1000ul', 'D2')

    # instrument setup
    m50 = instruments.Pipette(
        axis='a',
        max_volume=50,
        min_volume=5,
        channels=8,
        tip_racks=[tiprack_50])

    p1000 = instruments.Pipette(
        axis='b',
        max_volume=1000,
        min_volume=100,
        tip_racks=[tiprack_1000])

    # reagent setup
    water = trough.wells('A12')

    volume_list = csv_to_list(csv_file)
    tubes = [well for well in tuberack.wells()][:len(volume_list)]
    trough_wells = [well for well in trough.wells()]
    for vol, dest, new_dest in zip(volume_list, tubes, trough_wells):
        p1000.pick_up_tip()
        p1000.transfer(vol, water, dest, new_tip='never')
        p1000.mix(5, 500, dest)
        p1000.transfer(1000, dest, new_dest, new_tip='never')
        p1000.drop_tip()

    rows = [row[0].top() for plate in plates for row in plate.rows()]
    for index, source in zip(range(0, 24, 4), tubes):
        dests = rows[index:index+4]
        m50.distribute(32, source, dests)

    for well, tube in zip(trough_wells, tubes):
        p1000.transfer(1000, well, tube)
