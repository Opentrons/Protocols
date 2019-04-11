from opentrons import labware, instruments
from otcustomizers import FileInput

metadata = {
    'protocolName': 'CSV Plate Filling',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# example
example_csv = """,Sample in µl,,,,,,,,,,,,,,
,,1,2,3,4,5,6,7,8,9,10,11,12,," "
,A,1,1,1,1,1,1,1,1,1,1,1,1,,
,B,2,2,2,2,2,2,2,2,2,2,2,2,,
,C,3,3,3,3,3,3,3,3,3,3,3,3,,
,D,4,4,4,4,4,4,4,4,4,4,4,4,,
,E,5,5,5,5,5,5,5,5,5,5,5,5,,
,F,6,6,6,6,6,6,6,6,6,6,6,6,,
,G,7,7,7,7,7,7,7,7,7,7,7,7,,
,H,8,8,8,8,8,8,8,8,8,8,8,8,,
"""

# create custom create custom labware
PCR_plate_name = 'FrameStar-96-PCR'
if PCR_plate_name not in labware.list():
    labware.create(
        PCR_plate_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=5.50,
        depth=15.10,
        volume=200
    )

flat_plate_name = '4titude-96-flat'
if flat_plate_name not in labware.list():
    labware.create(
        flat_plate_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=6.3,
        depth=10.8,
        volume=350
    )

# load labware
trough = labware.load('trough-12row', '1')
DNA_plate = labware.load(PCR_plate_name, '2')
destination_plate = labware.load(flat_plate_name, '3')
tips50 = [labware.load('opentrons-tiprack-300ul', slot) for slot in ['4', '5']]

# pipettes
p50 = instruments.P50_Single(mount='right', tip_racks=tips50)

# well setup
H2O = trough.wells('A7')
DNA_sources = [well for row in DNA_plate.rows() for well in row]
destination_wells = [well for row in destination_plate.rows() for well in row]


def extract_csv_transfers(file_string):
    # take in all rows of the file
    whole_file = file_string.splitlines()

    # pick off water transfers
    H2O_rows = whole_file[2:10]
    H2O_transfers = []
    for row in H2O_rows:
        els = row.split(',')
        for el in els[2:14]:
            H2O_transfers.append(el)

    # pick off DNA transfers
    DNA_rows = whole_file[16:24]
    DNA_transfers = []
    for row in DNA_rows:
        els = row.split(',')
        for el in els[2:14]:
            DNA_transfers.append(el)

    return H2O_transfers, DNA_transfers


def run_custom_protocol(file: FileInput = example_csv):
    # extract data from csv
    H2O_t, DNA_t = extract_csv_transfers(file)

    # transfer water using same tip
    p50.pick_up_tip()
    for H2O_vol, dest in zip(H2O_t, destination_wells):
        p50.transfer(H2O_vol, H2O, dest.top(), new_tip='never', blow_out=True)
    p50.drop_tip()

    # transfer DNA to corresponding well
    for DNA_vol, source, dest in zip(DNA_t, DNA_sources, destination_wells):
        p50.transfer(DNA_vol, source, dest, blow_out=True)
