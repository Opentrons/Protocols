from opentrons import containers, instruments
from otcustomizers import FileInput, StringSelection

metadata = {
    'protocolName': 'Cherrypicking CSV Spreadsheet',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

tiprack_slots = ['D1', 'A2', 'C2', 'E2']
tipracks = [containers.load('tiprack-200ul', slot) for slot in tiprack_slots]
trash = containers.load('trash-box', 'E1')

example_csv = """
A1, 20
A3, 10
B2, 15

"""

# create custom containers
source_name = '96-2ml-rack'
if source_name not in containers.list():
    containers.create(
        source_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=7.42,
        depth=40.27,
        volume=2000
        )

dest_name = '96-deep-custom'
if dest_name not in containers.list():
    containers.create(
        dest_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=7.78,
        depth=35.6,
        volume=2000
        )

source_plate = containers.load(source_name, 'B1')
dest_plate = containers.load(dest_name, 'C1')


def run_custom_protocol(
        volumes_csv: FileInput = example_csv,
        pipette_axis: StringSelection(
            'B (left side)', 'A (right side)') = 'B (left side)',
        pipette_model: StringSelection(
            'p300', 'p50', 'p10', 'p1000') = 'p300',
        tip_reuse: StringSelection(
            'new tip each time', 'reuse tip') = 'new tip each time',
        blow_out_at_destination: StringSelection('yes', 'no') = 'yes'
        ):

    pipette_max_vol = int(pipette_model[1:])

    pipette = instruments.Pipette(
        axis='b' if pipette_axis[0] == 'B' else 'a',
        max_volume=pipette_max_vol,
        min_volume=pipette_max_vol / 10,
        tip_racks=tipracks,
        trash_container=trash
    )

    data = [
        [well, vol]
        for well, vol in
        [row.split(',') for row in volumes_csv.strip().splitlines() if row]
    ]

    if tip_reuse == 'reuse tip':
        pipette.pick_up_tip()
    for well_name, vol in data:
        if well_name and vol:
            vol = float(vol)
            if tip_reuse == 'new tip each time':
                pipette.pick_up_tip()
            pipette.transfer(
                vol,
                source_plate.wells(well_name),
                dest_plate.wells(well_name),
                new_tip='never')
            if blow_out_at_destination == 'yes':
                pipette.blow_out(dest_plate.wells(well_name))
            if tip_reuse == 'new tip each time':
                pipette.drop_tip()
    if tip_reuse == 'reuse tip':
        pipette.drop_tip()
