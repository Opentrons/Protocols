from opentrons import instruments, labware
from otcustomizers import StringSelection

# trough and 384-well plate
trough = labware.load('trough-12row', '4', 'trough')
plate = labware.load('384-plate', '2', 'plate')


def run_custom_protocol(
        well_volume: float=50.0,
        reagent_well: StringSelection(
            'A1', 'A2', 'A3', 'A4', 'A5', 'A6',
            'A7', 'A8', 'A9', 'A10', 'A11', 'A12')='A1',
        plate_starting_column: str=1,
        number_of_columns_to_fill: int=24,
        pipette_type: StringSelection(
            'p300-Single', 'p50-Single', 'p10-Single',
            'p300-Multi', 'p50-Multi', 'p10-Multi')='p50-Multi',
        mix_reagent_before_transfer: StringSelection(
            'True', 'False')='True'):

    if int(plate_starting_column) < 0 or int(plate_starting_column) > 24:
        raise Exception("Plate starting column number must be 1-24.")
    if (int(plate_starting_column) + number_of_columns_to_fill) > 25:
        raise Exception("Number of columns to fill exceeds plate's limit.")

    if mix_reagent_before_transfer == 'False':
        mix_times = 5
    else:
        mix_times = 0

    pip_name = pipette_type.split('-')  # Check which pipette type

    if pip_name[0] == 'p10':
        tiprack = labware.load('tiprack-10ul', '1', 'p10rack')
    else:
        tiprack = labware.load('opentrons-tiprack-300ul', '1', 'p300rack')

    if pipette_type == 'p300-Single':
        pipette = instruments.P300_Single(
            mount='left',
            tip_racks=[tiprack])
    elif pipette_type == 'p50-Single':
        pipette = instruments.P50_Single(
            mount='left',
            tip_racks=[tiprack])
    elif pipette_type == 'p10-Single':
        pipette = instruments.P10_Single(
            mount='left',
            tip_racks=[tiprack])
    elif pipette_type == 'p300-Multi':
        pipette = instruments.P300_Multi(
            mount='left',
            tip_racks=[tiprack])
    elif pipette_type == 'p50-Multi':
        pipette = instruments.P50_Multi(
            mount='left',
            tip_racks=[tiprack])
    elif pipette_type == 'p10-Multi':
        pipette = instruments.P10_Multi(
            mount='left',
            tip_racks=[tiprack])

    if pip_name[1] == 'Multi':
        alternating_wells = []
        for column in plate.cols(plate_starting_column, to='24'):
            alternating_wells.append(column.wells('A'))
            alternating_wells.append(column.wells('B'))
        dests = alternating_wells[:number_of_columns_to_fill * 2]
    else:
        dests = plate.cols(
            plate_starting_column, length=number_of_columns_to_fill)

    pipette.distribute(
        well_volume,
        trough.wells(reagent_well),
        dests,
        mix_before=(mix_times, pipette.max_volume))
