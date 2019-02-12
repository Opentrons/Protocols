from opentrons import labware, instruments
from otcustomizers import FileInput

metadata = {
    'protocolName': 'Cell Normalization',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
    }

trough_name = 'trough-1row-290ml'
if trough_name not in labware.list():
    labware.create(
        trough_name,
        grid=(1, 1),
        spacing=(0, 0),
        diameter=75,
        depth=39.2)

# labware setup
reservoir = labware.load(trough_name, '1')
source = labware.load('96-flat', '2')
outputs = [labware.load('24-well-plate', slot)
           for slot in ['3', '4', '5', '6']]
tipracks = [labware.load('tiprack-1000ul', slot)
            for slot in ['7', '8']]

# instruments setup
p1000 = instruments.P1000_Single(
    mount='left',
    tip_racks=tipracks)


csv_example = """
Source Well,Dest Plate,Dest Well,Buffer Volume,Culture Volume
A1,1,A1,1591,1870
B1,2,B1,1629,808
C1,3,C1,724,1793
D1,4,D1,1073,1138
E1,1,A2,1320,425
F1,2,B2,715,1642
G1,3,C2,122,106
H1,4,D2,1770,968
A2,1,A3,1619,965
B2,2,B3,1243,228
C2,3,C3,182,1742
D2,4,D3,1002,440
"""


def csv_to_list(csv_string):
    global source, outputs

    info_list = [cell for line in csv_string.splitlines() if line
                 for cell in [line.split(',')]]
    buffer_info = {'dest': [], 'volume': []}
    culture_info = {'source': [], 'dest': [], 'volume': []}

    for line in info_list[1:]:
        source_well = source.wells(line[0])
        dest_well = outputs[int(line[1]) - 1].wells(line[2])
        buffer_vol = float(line[3])
        culture_vol = float(line[4])

        culture_info['source'].append(source_well)
        culture_info['dest'].append(dest_well)
        culture_info['volume'].append(culture_vol)
        buffer_info['dest'].append(dest_well)
        buffer_info['volume'].append(buffer_vol)

    return buffer_info, culture_info


def run_custom_protocol(transfer_csv: FileInput=csv_example):

    buffer_info, culture_info = csv_to_list(transfer_csv)

    # transfer buffer to output plates
    p1000.transfer(
        buffer_info['volume'],
        reservoir.wells('A1'),
        buffer_info['dest'])

    # transfer culture to output plates
    for vol, source, dest in zip(
            culture_info['volume'],
            culture_info['source'],
            culture_info['dest']):

        p1000.pick_up_tip()
        p1000.mix(3, 1000, source)
        p1000.transfer(vol, source, dest, new_tip='never')
        p1000.drop_tip()
