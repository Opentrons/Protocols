from opentrons import labware, instruments, robot
from otcustomizers import FileInput

"""
Create Pool Libraries
"""

# labware setup
plates = [labware.load('96-flat', slot)
          for slot in ['2', '3', '4', '5', '6', '7', '8', '9']]
tipracks = [labware.load('tiprack-10ul', slot)
            for slot in ['10', '11']]
tuberack = labware.load('opentrons-tuberack-2ml-eppendorf', '1')

# instrument setup
p10 = instruments.P10_Single(
    mount='left',
    tip_racks=tipracks)

pool_scheme_example = """
1,2,5
A_001_BLK: D12,A_002_BLK: A12,D_008_BLK: A3
B_002_BLK: F12,B_002_BLK: A3,
C_001_BLK: B10,C_002_BLK: D4,
D_001_BLK: D10,D_002_BLK: B5,
E_002_BLK: F1,,
F_001_BLK: B11,,
G_001_BLK: D4,,
H_002_BLK: F4,,
A_001_BLK: B12,,
B_001_BLK: D5,,
C_002_BLK: F5,,
D_001_BLK: B6,,
E_001_BLK: D2,,
F_02_BLK: F9,,
A_001_BLK: B10,,
"""

plate_dict = {alpha: plate for alpha, plate in zip(
    ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'], plates)}


def create_pool_libraries(csv_string):
    """
    Parse through each column of the csv to pool components into each
    library
    """
    # transform csv string to list
    info_list = [line.split(',')
                 for line in csv_string.splitlines() if line]

    # go through each column
    for col in range(len(info_list[0])):
        for index, row in enumerate(info_list):
            if index == 0:
                volume = row[col]  # first row is always volume in uL
            elif row[col]:
                source_plate = plate_dict[row[col].split('_')[0].lower()]
                source_well = row[col].split(': ')[1]
                source = source_plate.wells(source_well)
                p10.transfer(volume, source, tuberack.wells(col))
        # prompt user to reset tipracks after each pool library
        robot.pause("Replace tipracks.")
        p10.reset_tip_tracking()


def run_custom_protocol(
        pool_scheme_csv: FileInput=pool_scheme_example):

    create_pool_libraries(pool_scheme_csv)
