from opentrons import labware, instruments
from otcustomizers import FileInput

example_1 = """
A1,3
A2,5
A3,15
A4,1
A6,4
A7,12
B1,5
B2,20
"""

example_2 = """"""
example_3 = """"""


def csv_to_list(csv_string):
    sources = []
    volumes = []
    info_list = [line.split(',') for line in csv_string.splitlines() if line]
    for line in info_list:
        sources.append(line[0])
        volumes.append(float(line[1]))
    return sources, volumes


def run_custom_protocol(
        plate_csv_1: FileInput=example_1,
        plate_csv_2: FileInput=example_2,
        plate_csv_3: FileInput=example_3):

    number_of_plates = 1
    if plate_csv_2:
        number_of_plates += 1
    if plate_csv_3:
        number_of_plates += 1

    # labware setup
    plates = [labware.load('96-PCR-flat', slot)
              for slot in ['1', '2', '4']][:number_of_plates]
    tuberack = labware.load('opentrons-tuberack-2ml-eppendorf', '5')
    tiprack = [labware.load('tiprack-10ul', slot)
               for slot in ['3', '6', '7', '8', '9', '10', '11']]

    # instrument setup
    p10 = instruments.P10_Single(
        mount='left',
        tip_racks=tiprack)

    csvs = [plate_csv_1, plate_csv_2, plate_csv_3][:number_of_plates]
    tube = tuberack.wells('A1')

    # transfer from each plate to tube
    for plate, csv in zip(plates, csvs):
        sources, volumes = csv_to_list(csv)
        for source, vol in zip(sources, volumes):
            p10.transfer(vol, plate.wells(source), tube, new_tip='once')
