from opentrons import instruments, containers
from otcustomizers import StringSelection

# trough and 384-well plate
trough = containers.load('trough-12row', 'E1', 'trough')
plate = containers.load('384-plate', 'C1', 'plate')

# 8-channel 10uL pipette, with tip rack and trash
trash = containers.load('trash-box', 'B2', 'trash')


def run_custom_protocol(
        well_volume: float = 1.0,
        reagent_well: StringSelection(
            'A1', 'A2', 'A3', 'A4', 'A5', 'A6',
            'A7', 'A8', 'A9', 'A10', 'A11', 'A12') = 'A1',
        plate_starting_column: str = '1',
        number_of_columns_to_fill: int = 24,
        pipette_type: StringSelection('p300-Single', 'p50-Single',
                                      'p10-Single', 'p300-Multi', 'p50-Multi',
                                      'p10-Multi', 'p200-Single',
                                      'p200-Multi') = 'p50-Multi',
        mix_reagent_before_transfer: StringSelection(
            'True', 'False') = 'True'):

    if int(plate_starting_column) <= 0 or int(plate_starting_column) > 24:
        raise Exception("Plate starting column number must be 1-24.")
    if (int(plate_starting_column) + number_of_columns_to_fill) > 25:
        raise Exception("Number of columns to fill exceeds plate's limit.")

    if mix_reagent_before_transfer == 'False':
        mix_times = 0
    else:
        mix_times = 5

    pip_name = pipette_type.split('-')  # Check which pipette type

    if pip_name[0] == 'p10':
        tiprack = containers.load('tiprack-10ul', 'A1', 'p10rack')
    else:
        tiprack = containers.load('tiprack-200ul', 'A1', 'p300rack')

    if pip_name[0] != 'p10' and well_volume < 5:
        raise Exception("Cannot transfer volume this small without p10.")
    if pip_name[0] == 'p20' and well_volume < 20:
        raise Exception("Cannot transfer volume this small with p200.")
    if pip_name[0] == 'p30' and well_volume < 30:
        raise Exception("Cannot transfer volume this small with p300.")

    # create pipette
    if pip_name[1] == 'Single':
        chan = 1  # Number of channels
    if pip_name[1] == 'Multi':
        chan = 8
    vol = int(pip_name[0][1:])
    pipette = instruments.Pipette(
        axis='b',
        max_volume=vol,
        tip_racks=[tiprack],
        channels=chan,
        trash_container=trash)

    alternating_wells = []
    for row in plate.rows():
        if pip_name[1] == 'Multi':
            alternating_wells.append(row.wells('A'))
            alternating_wells.append(row.wells('B'))
        else:
            alternating_wells.append(row.wells('A', length=8, step=2))
            alternating_wells.append(row.wells('B', length=8, step=2))

    pipette.distribute(
        well_volume,
        trough.wells(reagent_well),
        alternating_wells,
        mix_before=(mix_times, pipette.max_volume))
