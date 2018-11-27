from opentrons import instruments, containers
from otcustomizers import StringSelection

# trough and 384-well plate
trough = containers.load('trough-12row', 'E1', 'trough')
plate = containers.load('384-plate', 'C1', 'plate')

# 8-channel 10uL pipette, with tip rack and trash
trash = containers.load('trash-box', 'B2', 'trash')


def run_custom_protocol(
        well_volume: float=50.0,
        reagent_well: StringSelection(
            'A1', 'A2', 'A3', 'A4', 'A5', 'A6',
            'A7', 'A8', 'A9', 'A10', 'A11', 'A12')='A1',
        plate_starting_row: str=1,
        number_of_rows_to_fill: int=24,
        pipette_type: StringSelection(
            'p300-Single', 'p50-Single', 'p10-Single',
            'p300-Multi', 'p50-Multi', 'p10-Multi')='p50-Multi',
        mix_reagent_before_transfer: StringSelection(
            'True', 'False')='True'):

    if int(plate_starting_row) < 0 or int(plate_starting_row) > 24:
        raise Exception("Plate starting row number must be 1-24.")
    if (int(plate_starting_row) + number_of_rows_to_fill) > 25:
        raise Exception("Number of rows to fill exceeds plate's limit.")

    if mix_reagent_before_transfer == 'False':
            mix_times = 5
    else:
            mix_times = 0

    pip_name = pipette_type.split('-')  # Check which pipette type
    chan = 1  # Number of channels
    if pip_name[1] == 'Multi':
        chan = 8
    vol = int(pip_name[0][1::])
    if vol == 10:
        tiprack = containers.load('tiprack-10ul', 'A1', 'p10rack')
    else:
        tiprack = containers.load('tiprack-200ul', 'A1', 'p200rack')

    pipette = instruments.Pipette(
        axis='b',
        max_volume=vol,
        tip_racks=[tiprack],
        channels=chan,
        trash_container=trash)

    if pip_name[1] == 'Multi':
        alternating_wells = []
        for row in plate.rows(plate_starting_row, to='24'):
            alternating_wells.append(row.wells('A'))
            alternating_wells.append(row.wells('B'))
        dests = alternating_wells[:number_of_rows_to_fill * 2]
    else:
        dests = plate.rows(
            plate_starting_row, length=number_of_rows_to_fill)

    pipette.distribute(
        well_volume,
        trough.wells('A1'),
        dests,
        mix_before=(mix_times, pipette.max_volume))
