from opentrons import labware, instruments
from otcustomizers import StringSelection, FileInput

metadata = {
    'protocolName': 'Cherry Picking to Multiple Plates',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# create custom labware
deep_name = 'custom-96-deep'
if deep_name not in labware.list():
    labware.create(
        deep_name,
        grid=(12, 8),
        spacing=(9, 9),
        depth=33.5,
        diameter=7.5,
        volume=2000
    )

plate_96_name = 'custom-96-standard'
if plate_96_name not in labware.list():
    labware.create(
        plate_96_name,
        grid=(12, 8),
        spacing=(9, 9),
        depth=10.4,
        diameter=6.4,
        volume=300
    )

plate_384_name = 'custom-384-standard'
if plate_384_name not in labware.list():
    labware.create(
        plate_384_name,
        grid=(24, 16),
        spacing=(9, 9),
        depth=14.5,
        diameter=3.8,
        volume=55
    )

# labware
source_plate = labware.load('96-deep-well', '1')
tips50 = labware.load('opentrons-tiprack-300ul', '11')

example_csv = """,,,,,,,,,,,
,"Source plate
(Always the same order)",,,Output,,,,,,,
,,,,,,,,,,,
,,,,Plate 1,,,Plate 2,,,Plate 3,
,Well,Sample ID,,Well,Sample ID,,Well,Sample ID,,Well,Sample ID
,A1,Sample 1,,A1,Sample 11,,A2,Sample 1,,A2,Sample 1
,A2,Sample 2,,A10,Sample 2,,A3,Sample 2,,A3,Sample 2
,A3,Sample 3,,A11,Sample 13,,A6,Sample 4,,A6,Sample 4
,A4,Sample 4,,A12,Sample 14,,A4,Sample 7,,A4,Sample 7
,A5,Sample 5,,A2,Sample 14,,A8,Sample 9,,A8,Sample 9
,A6,Sample 6,,A3,Sample 2,,A1,Sample 5,,A1,Sample 5
,A7,Sample 7,,A4,Sample 3,,A12,Sample 6,,A12,Sample 6
,A8,Sample 8,,A5,Sample 4,,,,,,
"""


def run_custom_protocol(
        pipette_mount: StringSelection('right', 'left') = 'right',
        distribution_volume: float = 30,
        number_of_destination_plates: int = 9,
        destination_plate_type: StringSelection('96-well',
                                                '384-well') = '96-well',
        CSV_file: FileInput = example_csv):

    # pipette
    p50 = instruments.P50_Single(mount=pipette_mount, tip_racks=[tips50])

    # load appropriate number of destination wells
    if number_of_destination_plates > 9:
        raise Exception('Too many plates specified.')

    # choose destination plate based on user input
    if destination_plate_type == '96-well':
        dest_plates = [labware.load(plate_96_name, str(slot))
                       for slot in range(2, 2+number_of_destination_plates)]
    else:
        dest_plates = [labware.load(plate_384_name, str(slot))
                       for slot in range(2, 2+number_of_destination_plates)]

    # initialize lists for sources and destinations
    source_wells = []
    dest_wells = []

    # function to establish sources and destinations from input CSV
    def csv_parse(file_string):
        nonlocal source_wells
        nonlocal dest_wells

        # find start of well information
        trimmed = file_string.splitlines()
        start = 0
        for row in trimmed:
            vals = row.split(',')
            if vals[1].strip().lower() == 'well':
                start += 1
                break
            else:
                start += 1
        trimmed = trimmed[start:]

        # pull transfer wells from CSV
        for row in trimmed:
            vals = [x for x in row.split(',') if x]
            source_wells.append(vals[0].strip())
            num_dest_wells = len(vals)//2 - 1
            dests = []
            for i in range(1, num_dest_wells+1):
                dest = vals[i*2]
                dests.append(dest.strip())
            dest_wells.append(dests)

    # parse CSV for transfer information
    csv_parse(CSV_file)

    # loop through sources and destinations and transfer
    for source, dest_set in zip(source_wells, dest_wells):
        source_well = source_plate.wells(source)
        dest_full = []
        for dest, plate in zip(dest_set, dest_plates):
            dest_full.append(plate.wells(dest))
        p50.transfer(
            distribution_volume,
            source_well,
            [d.top() for d in dest_full]
            )
