from opentrons import labware, instruments
from otcustomizers import FileInput, StringSelection

example_csv = """
Block Start,Well Start ,ul to add,Block End,Well End
A,A1,3.95,B,A1
A,A2,2.97,B,A2
A,A3,2.85,B,A3
A,A4,3.56,B,A4
A,A5,2.87,B,A5
A,A6,2.48,B,A6
A,A7,1.84,B,H7
A,B5,2.27,B,B8
A,B8,1.93,B,B1
A,B9,0.99,B,B2
"""


def csv_to_lists(csv_string, plate_A, plate_B):
    """
    decipher the CSV file and return 3 lists
    1) source - list of source wells
    2) dest - list of destination wells
    3) vol - list of volumes of liquid transfer
    """

    string = [line.split(',') for line in csv_string.splitlines() if line]
    source = []
    dest = []
    vol = []
    for line in string[1:]:
        source_plate = (plate_A if line[0].lower() == 'a' else plate_B)
        source_well = source_plate.wells(int(line[1])-1)
        dest_plate = (plate_B if line[3].lower() == 'b' else plate_A)
        dest_well = dest_plate.wells(int(line[4])-1)
        source.append(source_well)
        dest.append(dest_well)
        vol.append(float(line[2]))

    return source, dest, vol


def run_custom_protocol(
        transfer_csv: FileInput=example_csv,
        block_a_container: StringSelection(
            '96-flat', '96-deep-well', '96-PCR-tall', '384-well')='96-flat',
        block_b_container: StringSelection(
            '96-flat', '96-deep-well', '96-PCR-tall', '384-well')='96-flat'):

    # labware setup
    plate_A = labware.load(block_a_container, '1', 'plate_A')
    plate_B = labware.load(block_b_container, '2', 'plate_B')

    source_list, dest_list, vol_list = csv_to_lists(
        transfer_csv, plate_A, plate_B)

    # determine number of tipracks needed
    total_tips = len(source_list)
    total_tipracks = total_tips // 96 + (1 if total_tips % 96 > 0 else 1)
    tipracks = [labware.load('tiprack-10ul', slot)
                for slot in ['4', '5', '3', '6', '7'][:total_tipracks]]

    # pipette setup
    p10 = instruments.P10_Single(
        mount='left',
        tip_racks=tipracks)

    # transfer solution according to the csv
    for source, dest, vol in zip(source_list, dest_list, vol_list):
        p10.transfer(vol, source, dest)
