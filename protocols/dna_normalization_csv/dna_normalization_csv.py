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
