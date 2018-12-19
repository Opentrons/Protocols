from opentrons import labware, instruments
from otcustomizers import FileInput, StringSelection

metadata = {
    'protocolName': 'Cherrypicking CSV',
    'author': 'Opentrons <protocols@opentrons.com>',
    'source': 'Protocol Library'
    }

example_csv = """
A1, 20
A3, 10
B2, 15

"""


def run_custom_protocol(
        volumes_csv: FileInput=example_csv,
        pipette_axis: StringSelection(
            'B (left side)', 'A (right side)')='B (left side)',
        pipette_model: StringSelection(
            'p1000', 'p300', 'p50', 'p10')='p300',
        source_plate_type: StringSelection('96-flat', '384-plate')='96-flat',
        destination_plate_type: StringSelection(
            '96-flat', '384-plate')='96-flat',
        tip_reuse: StringSelection(
            'new tip each time', 'reuse tip')='new tip each time'
        ):

    pipette_max_vol = int(pipette_model[1:])
    mount = 'left'
    if pipette_axis[0] == 'B':
        mount = 'right'

    tiprack_slots = ['1', '4', '7', '10']

    if pipette_max_vol == 300:
        tipracks = [
            labware.load('tiprack-200ul', slot) for slot in tiprack_slots]
        pipette = instruments.P300_Single(mount=mount, tip_racks=tipracks)
    elif pipette_max_vol == 50:
        tipracks = [
            labware.load('tiprack-200ul', slot) for slot in tiprack_slots]
        pipette = instruments.P50_Single(mount=mount, tip_racks=tipracks)
    elif pipette_max_vol == 10:
        tipracks = [
            labware.load('tiprack-200ul', slot) for slot in tiprack_slots]
        pipette = instruments.P10_Single(mount=mount, tip_racks=tipracks)
    elif pipette_max_vol == 1000:
        tipracks = [
            labware.load('tiprack-200ul', slot) for slot in tiprack_slots]
        pipette = instruments.P1000_Single(mount=mount, tip_racks=tipracks)

    data = [
        [well, float(vol)]
        for well, vol in
        [row.split(',') for row in volumes_csv.strip().split('\n') if row]
    ]

    source_plate = labware.load(source_plate_type, '2')
    dest_plate = labware.load(destination_plate_type, '3')

    tip_strategy = 'always' if tip_reuse == 'new tip each time' else 'once'
    for well_idx, (source_well, vol) in enumerate(data):
        pipette.transfer(
            vol,
            source_plate.wells(source_well),
            dest_plate.wells(well_idx),
            new_tip=tip_strategy)
