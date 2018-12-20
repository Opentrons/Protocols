from opentrons import labware, instruments, robot
from otcustomizers import StringSelection, FileInput

metadata = {
    'protocolName': 'Cherrypicking Using CSV Input',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
    }

if '24-deep-well' not in labware.list():
    labware.create(
        '24-deep-well',
        grid=(6, 4),
        spacing=(18, 18),
        depth=1.59,
        diameter=17.2
        )

if 'biotix-tiprack-300ul' not in labware.list():
    labware.create(
        'biotix-tiprack-300ul',
        grid=(12, 8),
        spacing=(8, 8),
        depth=60,
        diameter=3.5
        )

if 'biotix-tiprack-1000ul' not in labware.list():
    labware.create(
        'biotix-tiprack-1000ul',
        grid=(12, 8),
        spacing=(9, 9),
        depth=85,
        diameter=6.4
        )

transfer_info_example = """
source slot,source well,volume,destination slot,destination well,mix,discard \
tip
1,A1,30,4,A1,No,No
1,A2,100,4,A2,No,Yes
2,A3,40,5,A3,Yes,Yes
3,A12,1000,6,D6,No,No
"""

container_csv_example = """
slot,container
1,96-flat
2,24-well-plate
3,trough-12row
4,384-plate
5,96-deep-well
6,24-deep-well
"""


def load_containers(csv_string, pipette_spec):
    info_list = [cell for line in csv_string.splitlines() if line
                 for cell in [line.split(',')]]
    new_containers = {}
    for line in info_list[1:]:
        slot = line[0]
        plate_type = line[1]
        if not robot.deck[slot].has_children():
            new_containers[slot] = labware.load(plate_type, slot)
        else:
            raise Exception('Slot ' + slot + ' has already been occupied. \
Modify your CSV file.')
        if pipette_spec == 'Multi' and '24' in plate_type:
            raise Exception('You cannot use the multi-channel pipette with \
a 24-well plate. Pick a different pipette.')
    return new_containers


def get_transfer_info(csv_string, container_list):
    info_list = [cell for line in csv_string.splitlines() if line
                 for cell in [line.split(',')]]
    source_wells = []
    vols = []
    dest_wells = []
    mixes = []
    discard_tips = []
    for line in info_list[1:]:
        source_wells.append(container_list[line[0]].wells(line[1]))
        vols.append(float(line[2]))
        dest_wells.append(container_list[line[3]].wells(line[4]))
        mixes.append(line[5].lower())
        discard_tips.append(line[6].lower())
    return source_wells, vols, dest_wells, mixes, discard_tips


def run_custom_protocol(
    pipette_size: StringSelection(
        'p10-Single', 'p300-Single', 'p10-Multi', 'p300-Multi')='p300-Single',
    pipette_mount: StringSelection('left', 'right')='left',
    tip_types: StringSelection(
        'tiprack-10ul', 'tiprack-200ul',
        'opentrons-tiprack-300ul', 'biotix-tiprack-300ul',
        'biotix-tiprack-1000ul')='biotix-tiprack-300ul',
    container_csv: FileInput=container_csv_example,
    transfer_csv: FileInput=transfer_info_example
        ):

    tipracks = [labware.load('opentrons-tiprack-300ul', slot)
                for slot in ['7', '8', '9', '10', '11']]

    pipette_spec = pipette_size.split('-')

    pipette_args = {'mount': pipette_mount, 'tip_racks': tipracks}

    if pipette_size == 'p10-Single':
        pipette = instruments.P10_Single(**pipette_args)
    elif pipette_size == 'p300-Single':
        pipette = instruments.P300_Single(**pipette_args)
    elif pipette_size == 'p1000-Single':
        pipette = instruments.P1000_Single(**pipette_args)
    elif pipette_size == 'p10-Multi':
        pipette = instruments.P10_Multi(**pipette_args)
    elif pipette_size == 'p300-Multi':
        pipette = instruments.P300_Multi(**pipette_args)

    container_list = load_containers(container_csv, pipette_spec[1])

    sources, volumes, dests, mixes, discard_tips = get_transfer_info(
        transfer_csv, container_list)

    for source, volume, dest, mix, discard_tip in zip(
            sources, volumes, dests, mixes, discard_tips):
        if not pipette.tip_attached:
            pipette.pick_up_tip()
        pipette.transfer(volume, source, dest, new_tip='never')
        if mix == 'yes':
            if volume > pipette.max_volume:
                mix_vol = pipette.max_volume
            else:
                mix_vol = volume
            pipette.mix(3, mix_vol, dest)
        if discard_tip == 'yes':
            pipette.drop_tip()
    if pipette.tip_attached:
        pipette.drop_tip()
