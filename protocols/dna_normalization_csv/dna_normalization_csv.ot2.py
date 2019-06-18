from opentrons import labware, instruments, robot
from otcustomizers import FileInput, StringSelection

metadata = {
    'protocolName': 'DNA Normalization using CSV',
    'author': 'Opentrons <protocols@opentrons.com>',
    'source': 'Protocol Library'
    }


reservoir_name = 'biotix-resevoir'
if reservoir_name not in labware.list():
    labware.create(
        reservoir_name,
        grid=(1, 1),
        spacing=(0, 0),
        diameter=72,
        depth=23
        )

tiprack_slots = ['1', '4', '7', '10']
resevoir = labware.load(reservoir_name, '2')
source = resevoir.wells('A1')
trash = robot.fixed_trash[0]

example_csv = """
90,168,187,13,70,189,196,93
56,197,147,139,74,61,44,157
106,198,45,6,46,113,111,33
28,143,185,17,199,155,78,93
185,96,60,105,143,151,18,102
139,48,111,68,179,126,59,172
111,25,84,12,63,31,34,8
24,128,106,88,124,65,133,26
61,71,109,84,85,62,89,168
58,101,121,5,122,88,27,59
43,16,156,175,190,41,78,8
66,60,164,129,106,7,198,195

"""


def transpose_matrix(m):
    return [[r[i] for r in reversed(m)] for i in range(len(m[0]))]


def flatten_matrix(m):
    return [cell for row in m for cell in row]


def well_csv_to_list(csv_string):
    """
    Takes a csv string and flattens it to a list, re-ordering to match
    Opentrons well order convention (A1, B1, C1, ..., A2, B2, B2, ...)
    """
    data = [
        line.split(',')
        for line in reversed(csv_string.split('\n')) if line.strip()
        if line
    ]
    if len(data[0]) > len(data):
        # row length > column length ==> "landscape", so transpose
        return flatten_matrix(transpose_matrix(data))
    # "portrait"
    return flatten_matrix(data)


def run_custom_protocol(
        volumes_csv: FileInput=example_csv,
        pipette_mount: StringSelection(
            'right', 'left')='right',
        pipette_model: StringSelection(
            'p300-Single', 'p50-Single', 'p10-Single')='p300-Single',
        plate_type: StringSelection('96-flat', '384-plate')='96-flat',
        tip_reuse: StringSelection(
            'new tip each time', 'reuse tip')='new tip each time'):
    tipracks = [
        labware.load('opentrons-tiprack-300ul', slot)
        for slot in tiprack_slots]

    if pipette_model == 'p300-Single':
        pipette = instruments.P300_Single(
            mount=pipette_mount,
            tip_racks=tipracks)
    elif pipette_model == 'p50-Single':
        pipette = instruments.P50_Single(
            mount=pipette_mount,
            tip_racks=tipracks)
    elif pipette_model == 'p10-Single':
        tipracks = [
            labware.load('tiprack-10ul', slot)
            for slot in tiprack_slots]
        pipette = instruments.P10_Single(
            mount=pipette_mount,
            tip_racks=tipracks)

    plate = labware.load(plate_type, '3')

    volumes = [float(cell) for cell in well_csv_to_list(volumes_csv)]

    for vol in volumes:
        if 0 < vol < pipette.min_volume:
            robot.comment(
                'WARNING: volume {} is below pipette\'s minimum volume.'
                .format(vol))

    tip_strategy = 'always' if tip_reuse == 'new tip each time' else 'once'
    pipette.transfer(volumes, source, plate, new_tip=tip_strategy)
