from opentrons import labware, instruments
from otcustomizers import FileInput

metadata = {
    'protocolName': 'CSV Plate Filling',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# labware
tips10 = labware.load('tiprack-10ul', '1')
source_plate = labware.load('96-deep-well', '2')
dest_plate = labware.load('96-PCR-tall', '3')

# pipettes
p10 = instruments.P10_Single(
    mount='right',
    tip_racks=[tips10]
)

# example file
csv_example = """
A,B,C,D,E,F
8383463-1,Panel1,29,E04,2,A01
8383464-1,Panel1,30,F04,2,B01
8383465-1,Panel1,31,G04,2,C01
8383466-1,Panel1,32,H04,2,D01
8383159-1,Panel2,33,A05,2,A04
8383160-1,Panel2,34,B05,2,B04
8383161-1,Panel2,35,C05,2,C04
8383162-1,Panel2,36,D05,2,D04
8383163-1,Panel2,37,E05,2,E04
8383164-1,Panel2,38,F05,2,F04
8383387-1,Panel3,39,G05,2,A07
8383388-1,Panel3,40,H05,2,B07
8383389-1,Panel3,41,A06,2,C07
8383390-1,Panel3,42,B06,2,D07
8383391-1,Panel3,43,C06,2,E07
8383074-1,Panel4,44,D06,2,A10
8383075-1,Panel4,45,E06,2,B10
8383076-1,Panel4,46,F06,2,C10
8383077-1,Panel4,47,G06,2,D10
8383078-1,Panel4,48,H06,2,E10
"""


# CSV parse
def csv_to_list(file):
    new_list = [cell for line in file.splitlines() if line
                for cell in [line.split(',')]]
    new_list = new_list[1:]
    return new_list


# well parse function
def well_parse(well):
    row = well[0]
    col = str(int(well[1:]))
    return row+col


# perform all transfers
def run_custom_protocol(transfer_csv: FileInput = csv_example):
    transfers = csv_to_list(transfer_csv)
    for t in transfers:
        vol = float(t[4])
        if vol < 1:
            raise Exception("Volume is outside range of p10 pipette.")
        source = source_plate.wells(well_parse(t[3]))
        dest = dest_plate.wells(well_parse(t[5]))
        p10.transfer(vol, source, dest, blow_out=True)
