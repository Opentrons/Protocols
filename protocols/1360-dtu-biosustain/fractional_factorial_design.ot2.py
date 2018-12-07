from opentrons import labware, instruments
from otcustomizers import FileInput

# labware setup
compounds = [labware.load('96-deep-well', slot)
             for slot in ['1', '4']]
experiments = labware.load('96-deep-well', '2')
tiprack10 = labware.load('tiprack-10ul', '5')
tiprack300 = labware.load('opentrons-tiprack-300ul', '6')

# instruments setup
p10 = instruments.P10_Single(
    mount='left',
    tip_racks=[tiprack10])

p300 = instruments.P300_Single(
    mount='right',
    tip_racks=[tiprack300])

example = """
Exp,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,\
29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,\
55,56,57,58,59,60,61,62,63,64
Adenine,-1,1,1,1,-1,1,-1,-1,1,1,-1,1,-1,1,-1,-1,1,-1,1,1,1,1,-1,-1,-1,1,1,-1,\
-1,1,1,-1,1,1,1,-1,1,-1,1,1,-1,-1,-1,1,-1,-1,-1,1,1,1,-1,1,1,-1,-1,1,1,-1,-1,\
-1,-1,-1,1,-1
Alanine,-1,-1,-1,1,1,-1,1,-1,1,-1,-1,-1,-1,-1,-1,-1,-1,1,-1,1,1,1,-1,1,-1,-1,\
1,1,1,1,-1,-1,1,-1,1,-1,1,-1,-1,-1,1,-1,1,-1,-1,1,-1,-1,1,1,1,1,1,-1,1,1,-1,1,\
1,1,1,1,1,-1
Ammonium sulfate,-1,-1,1,1,1,-1,1,-1,1,1,1,-1,1,1,-1,1,1,1,1,-1,-1,1,-1,1,-1,\
-1,-1,1,-1,-1,-1,1,-1,-1,1,1,1,1,1,1,1,1,1,1,1,-1,-1,-1,-1,1,-1,1,-1,-1,1,-1,\
-1,-1,-1,-1,-1,-1,1,-1
Arginine,1,1,1,1,1,1,1,-1,1,1,1,1,1,-1,-1,1,-1,1,-1,-1,-1,-1,-1,-1,-1,-1,-1,\
-1,1,1,-1,1,1,-1,-1,-1,1,-1,-1,1,1,-1,-1,1,-1,-1,1,-1,1,-1,1,1,-1,1,-1,1,1,-1,\
-1,1,1,-1,-1,1
"""


def csv_to_list(csv_string):
    info_list = [cell for line in csv_string.splitlines() if line
                 for cell in [line.split(',')]]
    volume_list = []
    for line in info_list[1:]:
        new_vol = []
        for cell in line[1:]:
            new_vol.append(cell)
        volume_list.append(new_vol)
    return volume_list


def run_custom_protocol(
        volume_positive_value: float=100,
        volume_negative_value: float=4,
        CSV_file: FileInput=example
        ):

    vol_list = csv_to_list(CSV_file)
    compounds_wells = [well
                       for plate in compounds
                       for row in plate.rows() for well in row]
    dest_wells = [well for row in experiments.rows() for well in row]

    for index, dest_vol in enumerate(vol_list):
        dest_300 = [dest_wells[index]
                    for index, vol in enumerate(dest_vol) if vol == '1']
        dest_10 = [dest_wells[index]
                   for index, vol in enumerate(dest_vol) if vol == '-1']

        p300.distribute(
            volume_positive_value,
            compounds_wells[index],
            dest_300,
            disposal_vol=0
            )
        p10.distribute(
            volume_negative_value,
            compounds_wells[index],
            dest_10,
            disposal_vol=0
            )
