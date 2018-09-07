from opentrons import labware, instruments
from otcustomizers import FileInput
import csv
import io

csv_example1 = """\
source plate,source well,source volume,dest plate,dest well
1,A1,5,5,A1
3,B7,5,5,A1
1,C1,5,5,A1
2,E7,5,5,A1
1,B7,5,5,A2
3,C1,5,5,A2
1,E7,5,5,A2
2,E7,5,5,A3
3,D1,5,5,A3
"""

# Load plate 1-5, make plate[0] an empty list,
# so plate1 = plate[1], plate2 = plate[2], and so on
plates = [
    [],
    labware.load('96-flat', '1'),
    labware.load('96-flat', '2'),
    labware.load('96-flat', '3'),
    labware.load('96-flat', '4'),
    labware.load('96-flat', '5')
]

# Tiprack
tiprack = labware.load('tiprack-10ul', '6')

# Pipette setup
p10 = instruments.P10_Single(
    mount='left',
    tip_racks=[tiprack])


# Change csv file into a list of dictionaries
def csv_to_list(csv_string):
    """
    Takes a csv string and flattens it to a list, that contains:
    {[('source plate', '1'), ('source well', 'A1'), ('source volume', '5'),
        ('dest plate', '5'), ('dest well', 'A1')}
    {[('source plate', '2'), ('source well', 'B1'), ('source volume', '5'),
        ('dest plate', '5'), ('dest well', 'A1')]}
    ...
    Each dictionary contains the all of the information for one liquid transfer
    """
    reader_list = csv.DictReader(io.StringIO(csv_string))
    return [row for row in reader_list]


def run_custom_protocol(csv_file: FileInput=csv_example1):

    csv_list = csv_to_list(csv_file)

    for each_transfer in csv_list:
        # retrieve informations from each dictionary for each transfer
        source_plate = plates[int(each_transfer['source plate'])]
        source_well = each_transfer['source well']
        source_vol = each_transfer['source volume']
        dest_plate = plates[int(each_transfer['dest plate'])]
        dest_well = each_transfer['dest well']
        p10.transfer(source_vol, source_plate.wells(source_well),
                     dest_plate.wells(dest_well))
