from opentrons import labware, instruments
from otcustomizers import FileInput

metadata = {
    'protocolName': 'CSV Cherrypicking',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# create custom plate
plate_name = 'VWR-PCR-96'
if plate_name not in labware.list():
    labware.create(plate_name,
                   grid=(12, 8),
                   spacing=(9, 9),
                   diameter=6,
                   depth=20,
                   volume=200)

# labware
tube_racks = [labware.load('opentrons-aluminum-block-2ml-eppendorf', slot)
              for slot in ['4', '5', '1', '2']]
plate = labware.load(plate_name, '3')
trough = labware.load('trough-12row', '8')
tips10 = labware.load('tiprack-10ul', '6')
tips300 = labware.load('opentrons-tiprack-300ul', '9')


example_csv = """,,,,,,,,,,,,
rack 1,,,,,,,,,,,,
A1,5,A2,5,A3,5,A4,5,A5,5,A6,5,
B1,3,B2,3,B3,3,B4,3,B5,3,B6,3,
C1,4,C2,4,C3,4,C4,4,C5,4,C6,4,
D1,2,D2,2,D3,2,D4,2,D5,2,D6,2,
,,,,,,,,,,,,
rack 2,,,,,,,,,,,,
A1,6,A2,4,A3,5,A4,4,A5,5,A6,4,
B1,3,B2,5,B3,3,B4,5,B5,3,B6,5,
C1,5,C2,3,C3,4,C4,3,C5,4,C6,3,
D1,1,D2,4,D3,2,D4,4,D5,2,D6,4,
,,,,,,,,,,,,
rack 3,,,,,,,,,,,,
A1,6,A2,5,A3,6,A4,6,A5,5,A6,5,
B1,8,B2,3,B3,8,B4,8,B5,3,B6,3,
C1,2,C2,4,C3,2,C4,2,C5,4,C6,4,
D1,3,D2,2,D3,3,D4,3,D5,2,D6,2,
,,,,,,,,,,,,
rack 4,,,,,,,,,,,,
A1,4,A2,5,A3,5,A4,5,A5,5,A6,5,
B1,5,B2,3,B3,3,B4,3,B5,3,B6,3,
C1,3,C2,4,C3,4,C4,4,C5,4,C6,4,
D1,4,D2,2,D3,2,D4,2,D5,2,D6,2,"""

# pipettes
p10 = instruments.P10_Single(mount='right', tip_racks=[tips10])
p300 = instruments.P300_Single(mount='left', tip_racks=[tips300])


def run_custom_protocol(CSV_file: FileInput = example_csv):
    # initialize wells and volumes lists
    sources = []
    volumes = []
    h2o = trough.wells('A1')

    # set up proper destination order
    dests = [well for block in range(3) for row in 'HGFEDCBA'
             for well in plate.rows(row)[block*4:block*4+4]]

    def csv_parser(file_string):
        nonlocal sources
        nonlocal volumes

        # find start of well information
        trimmed = file_string.splitlines()
        start = 0
        for row in trimmed:
            vals = row.split(',')
            if vals[1].strip().lower():
                break
            else:
                start += 1
        trimmed = trimmed[start:]
        # get racks, ignoring whitespace rows
        rack1 = trimmed[0:4]
        rack2 = trimmed[6:10]
        rack3 = trimmed[12:16]
        rack4 = trimmed[18:22]
        racks_csv = [rack1, rack2, rack3, rack4]

        # extract wells moving down columns, then across rows
        for rack_csv, rack_actual in zip(racks_csv, tube_racks):
            for col in range(6):
                for row in rack_csv:
                    vals = [v for v in row.split(',') if v]
                    well = vals[col*2].strip()
                    volume = float(vals[col*2+1])
                    sources.append(rack_actual.wells(well))
                    volumes.append(volume)

    # obtain data from CSV
    csv_parser(CSV_file)

    # perform transfers
    for volume, source, dest in zip(volumes, sources, dests):
        p10.pick_up_tip()
        p10.transfer(volume, source, dest, new_tip='never').touch_tip()
        p10.blow_out(dest)
        p10.drop_tip()

    # distribute water
    p300.distribute(
        100,
        h2o,
        [well.top() for well in plate.wells()],
        disposal_vol=0
                   )
