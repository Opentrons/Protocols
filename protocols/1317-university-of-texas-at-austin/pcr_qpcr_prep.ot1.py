from opentrons import containers, instruments
from otcustomizers import FileInput

metadata = {
    'protocolName': 'PCR/qPCR Prep',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
    }

plate = containers.load('PCR-strip-tall', 'B1')
tuberacks = [containers.load('tube-rack-2ml', slot)
             for slot in ['A1', 'A2']]
tiprack_10 = [containers.load('tiprack-10ul', slot)
              for slot in ['C2', 'D2', 'E2']]
trash = containers.load('trash-box', 'B2')

p10 = instruments.Pipette(
    axis='b',
    name='p10',
    channels=1,
    max_volume=10,
    tip_racks=tiprack_10,
    aspirate_speed=1000,
    dispense_speed=1000,
    trash_container=trash)

tuberack_example = """
Slot,Name,Well
A1,Master Mix,A1
A1,Forward 1,B1
A1,Forward 2,C1
A1,Forward 3,D1
A1,Forward 4,A2
A1,Reverse 1,B2
A1,Reverse 2,C2
A2,Reverse 3,D2
A2,Reverse 4,A3
A2,PCR template 1,B3
A2,PCR template 2,C3
"""

pcr_example = """
Well,Reagent 1,Reagent 2,Reagent 3
A1,Forward 1,Reverse 1,PCR template 1
B2,forward 1,Reverse 2,PCR template 1
C1,forward 1,Reverse 3,PCR template 2
D5,Forward 3,Reverse 4,PCR template 2
"""


def get_source_dict(csv_string):
    info_list = [cell for line in csv_string.splitlines() if line
                 for cell in [line.split(',')]]
    new_dict = {}
    for line in info_list[1:]:
        name = line[1].lower().strip().replace(" ", "")
        index = line[2].strip()
        if line[0] == 'A1':
            tuberack = tuberacks[0]
        elif line[0] == 'A2':
            tuberack = tuberacks[1]
        else:
            raise Exception('Source slot does not exist.')
        new_dict[name] = tuberack.wells(index)
    return new_dict


def get_dest_dict(csv_string, source_dict):
    info_list = [cell for line in csv_string.splitlines() if line
                 for cell in [line.split(',')]]
    new_dict = {name: [] for name in source_dict.keys()}
    master_mix_dict = []
    for line in info_list[1:]:
        for cell in line[1:]:
            name = cell.lower().strip().replace(" ", "")
            new_dict[name].append(plate.wells(line[0].strip()))
        master_mix_dict.append(plate.wells(line[0].strip()))
    return new_dict, master_mix_dict


def run_custom_protocol(
        tuberack_csv: FileInput=tuberack_example,
        pcr_setup_csv: FileInput=pcr_example,
        mastermix_vol: float=10.0,
        reagent_vol: float=3.0):

    mastermix = tuberacks[0].wells('A1')

    sources = get_source_dict(tuberack_csv)
    dests, master_mix_dests = get_dest_dict(pcr_setup_csv, sources)

    p10.transfer(mastermix_vol, mastermix, master_mix_dests, blow_out=True)

    for key in sources.keys():
        vol = reagent_vol
        if dests[key]:
            p10.transfer(vol, sources[key], dests[key], new_tip='always',
                         blow_out=True)
