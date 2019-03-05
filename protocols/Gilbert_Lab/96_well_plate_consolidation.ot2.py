from opentrons import labware, instruments
from otcustomizers import FileInput, StringSelection

# labware setup
tuberack = labware.load('tube-rack-2ml', '2')

tiprack = labware.load('tiprack-200ul', '4')

# pipette setup
p50 = instruments.P50_Single(
    mount='left',
    tip_racks=[tiprack]
    )


def well_csv_to_list(csv_string):
    """
    Takes a csv string and flattens it to a list
    """
    return [
        cell
        for line in (csv_string.split('\n')) if line.strip()
        for cell in line.split(',') if cell
    ]


example_csv = """
1,2,3,4,5,6,7,8,9,10,11,12
2,2,3,4,5,6,7,8,9,10,11,12
3,2,3,4,5,6,7,8,9,10,11,12
4,2,3,4,5,6,7,8,9,10,11,12
5,2,3,4,5,6,7,8,9,10,11,12
6,2,3,4,5,6,7,8,9,10,11,12
7,2,3,4,5,6,7,8,9,10,11,12
8,2,3,4,5,6,7,8,9,10,11,12
"""


def run_custom_protocol(
    volumes_csv: FileInput=example_csv,
    plate_type: StringSelection(
            '96-flat', '96-deep-well')='96-flat',
        destination_well: str='A1'):

    plate = labware.load(plate_type, '1')
    # parse string using helper csv function
    volumes_list = well_csv_to_list(volumes_csv)
    # target 2 mL tube
    target = tuberack.wells(destination_well)

    # convert the cells contents from strings to integers
    volumes = [float(cell) for cell in volumes_list]

    # create a list of plate wells in order of rows to match the volumes_list
    # order convention
    plate_loc = [well for row in plate.rows() for well in row]

    for vol, loc in zip(volumes, plate_loc):
        p50.transfer(vol, loc, target)
