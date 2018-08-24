from opentrons import containers, instruments
from otcustomizers import StringSelection

trash = containers.load('trash-box', 'B2')


def tiprack_from_pipette(pipette_vol):
    if pipette_vol <= 10:
        return 'tiprack-10ul'
    if 1000 > pipette_vol > 10:
        return 'tiprack-200ul'
    if pipette_vol == 1000:
        return 'tiprack-1000ul'
    raise ValueError('No known tiprack for a p{} pipette'.format(pipette_vol))



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

    p50.transfer(volumes, plate_loc, target, new_tips='always')
