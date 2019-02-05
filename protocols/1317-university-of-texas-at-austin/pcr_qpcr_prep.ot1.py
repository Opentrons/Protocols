from opentrons import containers, instruments
from otcustomizers import FileInput

plate = containers.load('96-flat', 'B1')
tuberacks = [containers.load('tube-rack-2ml', slot)
             for slot in ['A1', 'A2']]
tiprack_10 = [containers.load('tiprack-10ul', slot)
              for slot in ['C2', 'D2', 'E2']]
tiprack_50 = [containers.load('tiprack-200ul', slot)
              for slot in ['C1', 'D1', 'E1']]
trash = containers.load('trash-box', 'B2')

p10 = instruments.Pipette(
    axis='b',
    name='p10',
    channels=1,
    max_volume=10,
    tip_racks=tiprack_10,
    trash_container=trash)

p50 = instruments.Pipette(
    axis='a',
    name='p50',
    channels=1,
    max_volume=50,
    tip_racks=tiprack_50,
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
    new_dict['mastermix'] = tuberacks[0].wells('A1')
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
    new_dict['mastermix'] = []
    for line in info_list[1:]:
        for cell in line[1:]:
            name = cell.lower().strip().replace(" ", "")
            new_dict[name].append(plate.wells(line[0].strip()))
        new_dict['mastermix'].append(plate.wells(line[0].strip()))
    return new_dict


def run_custom_protocol(
        tuberack_csv: FileInput=tuberack_example,
        pcr_setup_csv: FileInput=pcr_example,
        total_volume: float=50.0):

    sources = get_source_dict(tuberack_csv)
    dests = get_dest_dict(pcr_setup_csv, sources)

    master_mix_vol = round(total_volume * 47 / 50, 1)
    reagent_vol = round(total_volume * 1 / 50, 1)

    for key in sources.keys():
        if key == 'mastermix':
            vol = master_mix_vol
            p50.distribute(
                vol, sources[key], [well.top() for well in dests[key]],
                disposal_vol=0)
        else:
            vol = reagent_vol
            if dests[key]:
                p10.transfer(vol, sources[key], dests[key], new_tip='always')
