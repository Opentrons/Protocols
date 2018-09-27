from opentrons import labware, instruments
from otcustomizers import FileInput

"""
Day 1: Seeding cells
"""

# labware setup
trough = labware.load('trough-12row', '1')
plate = labware.load('96-flat', '3')
tiprack1 = labware.load('tiprack-200ul', '4')

# reagent
media_cell = trough.wells('A1')

# pipette setup
m300 = instruments.P300_Multi(
    mount='left',
    tip_racks=[tiprack1])

example_csv = """
123,106,114,121,111,102,148,128,149,128,105,106
"""


def csv_to_well_list(csv_string):
    return [int(cell)
            for line in csv_string.splitlines() if line
            for cell in line.split(',')]


def run_custom_protocol(
    volume_csv: FileInput=example_csv
        ):

    volume_list = csv_to_well_list(volume_csv)

    well_list = [col for col in plate.cols()]

    m300.pick_up_tip()
    for vol, dest in zip(volume_list, well_list):
        m300.transfer(
            vol,
            media_cell,
            dest,
            mix_before=(5, vol),
            new_tip='never')
    m300.drop_tip()
