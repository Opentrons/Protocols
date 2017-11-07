from opentrons import containers, instruments

trough = containers.load('trash-box', 'C1')
source = trough.wells(0)

tiprack = containers.load('tiprack-200ul', 'A2')
trash = containers.load('trash-box', 'C2')

plate = containers.load('96-flat', 'A1')

# you may also want to change min and max volume of the pipette
pipette = instruments.Pipette(
    max_volume=200,
    min_volume=20,
    axis='a',
    channels=8,
    tip_racks=[tiprack],
    trash_container=trash)

example_csv = """
1,2,3,4,5,6,7,8
1,2,3,4,5,6,7,8
1,2,3,4,5,6,7,8
1,2,3,4,5,6,7,8
1,2,3,4,5,6,7,8
1,2,3,4,5,6,7,8
11,22,33,12,23,24,26,27
11,22,33,12,23,24,26,27
11,22,33,12,23,24,26,27
11,22,33,12,23,24,26,27
11,22,33,12,23,24,26,27
11,22,33,12,23,24,26,27
"""


class FileInput(object):
    def get_json(self):
        return {
            'type': 'FileInput'
        }


def well_csv_to_list(csv_string):
    """
    Takes a csv string and flattens it to a list, re-ordering to match
    Opentrons well order convention (A1, B1, C1, ..., A2, B2, B2, ...)
    """
    return [
        cell
        for line in reversed(csv_string.split('\n')) if line.strip()
        for cell in line.split(',') if cell
    ]


def run_custom_protocol(volumes_csv: FileInput=example_csv):
    volumes = [float(cell) for cell in well_csv_to_list(volumes_csv)]
    pipette.transfer(volumes, source, plate)
