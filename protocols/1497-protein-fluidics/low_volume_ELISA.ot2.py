from opentrons import labware, instruments
from otcustomizers import FileInput

metadata = {
    'protocolName': 'ELISA',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
    }

chip_name = 'microfluidic-chip-384-layout'
if chip_name not in labware.list():
    labware.create(
        chip_name,
        grid=(24, 16),
        spacing=(4.5, 4.5),
        diameter=3,
        depth=6)

plate_name = '96-well-v-bottom'
if plate_name not in labware.list():
    labware.create(
        plate_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=6.94,
        depth=11.65)

# labware setup
plate = labware.load(plate_name, '1')
chip = labware.load(chip_name, '2')
tuberack = labware.load('opentrons-tuberack-2ml-eppendorf', '4')
tipracks = [labware.load('tiprack-200ul', slot)
            for slot in ['5', '6']]


# instruments setup
p50 = instruments.P50_Single(
    mount='left',
    tip_racks=tipracks)

reagent_csv_example = """
R-A1;20,R-A1;20,P-A1;20,P-A2;20,,R-D2;200,,,,,,,,,,,,,R-A1;20,R-A1;20,P-A1;20,\
P-A2;20,,R-D2;200
,,,,,,,,,,,,,,,,,,,,,,,
R-A2;20,R-B2;20,P-B1;20,P-B2;20,,P-H12;10,,,,,,,,,,,,,R-A2;20,R-B2;20,P-B1;20,\
P-B2;20,,P-H12;10
"""


def csv_to_dict(csv_string):
    global plate, chip, tuberack
    info_list = [cell for line in csv_string.splitlines()
                 for cell in [line.split(',')]]
    new_dict = {}
    for line, row in zip(info_list, chip.rows()):
        for cell, well in zip(line, row):
            if cell:
                info = [item.strip() for item in cell.split(';')]
                source_info = info[0].split('-')
                if source_info[0] == 'R':
                    source = tuberack.wells(source_info[1])
                elif source_info[0] == 'P':
                    source = plate.wells(source_info[1])
                else:
                    raise Exception("This CSV does not follow the guidelines \
in the Additional Notes section of your protocol. Please review your CSV and \
try again.")
                if source not in new_dict.keys():
                    new_dict[source] = {'dests': [], 'vols': []}
                new_dict[source]['dests'].append(well)
                new_dict[source]['vols'].append(float(info[1]))
    return new_dict


def run_custom_protocol(reagent_csv: FileInput=reagent_csv_example):

    reagent_dict = csv_to_dict(reagent_csv)

    for reagent in reagent_dict.keys():
        vols = reagent_dict[reagent]['vols']
        dests = reagent_dict[reagent]['dests']
        p50.transfer(vols, reagent, dests)
