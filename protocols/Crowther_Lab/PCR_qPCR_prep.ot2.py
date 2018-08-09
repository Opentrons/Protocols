from opentrons import labware, instruments, robot
from otcustomizers import FileInput

trough = labware.load('trough-12row', '4')
MQ = trough.wells('A1')
PCR_masterMix = trough.wells('A2')

dna_plate = labware.load('96-flat', '1')
diluted_plate = labware.load('96-flat', '2')
plate = labware.load('96-flat', '3')
tiprack_10ul = labware.load('tiprack-10ul', '5')
tiprack2_10ul = labware.load('tiprack-10ul', '8')
tiprack_200ul = labware.load('tiprack-200ul', '6')
tiprack2_200ul = labware.load('tiprack-200ul', '7')

p10 = instruments.P10_Single(
	mount='left',
	tip_racks=[tiprack_10ul, tiprack2_10ul])

m50 = instruments.P50_Multi(
	mount='right',
	tip_racks=[tiprack_200ul, tiprack2_200ul])

sample_csv = """
1,2,3,4,5,6,7,8,9,10,11,12
2,2,3,4,5,6,7,8,9,10,11,12
3,2,3,4,5,6,7,8,9,10,11,12
4,2,3,4,5,6,7,8,9,10,11,12
5,2,3,4,5,6,7,8,9,10,11,12
6,2,3,4,5,6,7,8,9,10,11,12
7,2,3,4,5,6,7,8,9,10,11,12
8,2,3,4,5,6,7,8,9,10,11,12
"""

mq_csv = """
1,2,3,4,5,6,7,8,9,10,11,12
1,2,3,4,5,6,7,8,9,10,11,12
1,2,3,4,5,6,7,8,9,10,11,12
1,2,3,4,5,6,7,8,9,10,11,12
1,2,3,4,5,6,7,8,9,10,11,12
1,2,3,4,5,6,7,8,9,10,11,12
1,2,3,4,5,6,7,8,9,10,11,12
1,2,3,4,5,6,7,8,9,10,11,12
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
    sample_vol_csv: FileInput=sample_csv,
    MQ_vol_csv: FileInput=mq_csv):

    sample_vol = well_csv_to_list(sample_vol_csv)

    mq_vol = well_csv_to_list(MQ_vol_csv)

    p10.transfer(sample_vol, dna_plate, diluted_plate, new_tip='always')

    p10.transfer(mq_vol, MQ, diluted_plate)

    m50.transfer(2, diluted_plate.cols(), plate.cols(), new_tip='always')

    m50.transfer(23, PCR_masterMix, plate.cols())
