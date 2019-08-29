import math
from itertools import takewhile
from opentrons import labware, instruments, robot
from otcustomizers import StringSelection

metadata = {
    'protocolName': 'Tube Filling',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
    }

tube_vars = ['0.5', '1.5', '2']
depth_vars = [24.6, 42.2, 42.2]
tuberack_names = []

# create definitions for 48-well rack
for var, depth in zip(tube_vars, depth_vars):
    tuberack_name = 'x-capper-rack-48-well-'+var+'-ml'
    if tuberack_name not in labware.list():
        labware.create(
            tuberack_name,
            grid=(8, 6),
            spacing=(13.42, 13.42),
            depth=depth,
            diameter=8.41)
    tuberack_names.append(tuberack_name)

# create definitions for 24-well rack
for var, depth in zip(tube_vars, depth_vars):
    tuberack_name = 'custom-24-well-'+var+'-ml'
    if tuberack_name not in labware.list():
        labware.create(
            tuberack_name,
            grid=(6, 4),
            spacing=(18, 18),
            depth=depth,
            diameter=8.41)
    tuberack_names.append(tuberack_name)


def run_custom_protocol(
        transfer_volume: float=105,
        tube_rack_type: StringSelection('48-well', '24-well')='48-well',
        tube_type: StringSelection('0.5-ml', '1.5-ml', '2-ml')='0.5-ml',
        number_of_racks: int=2,
        falcon_tube_type: StringSelection('15-ml', '50-ml')='15-ml',
        starting_stock_volume_in_mL: float=15,
        pipette_type: StringSelection(
            'P10_Single', 'P50_Single', 'P300_Single',
            'P1000_Single')='P300_Single',
        pipette_mount: StringSelection('left', 'right')='left',
        starting_tip: str='A1'):

    # labware setup
    if number_of_racks > 9:
        raise Exception('The max numnber of racks to be filled 9. '
                        'Please try again.')
    # define source tube
    if falcon_tube_type == '15-ml':
        source = labware.load(
            'opentrons_6_tuberack_falcon_50ml_conical', '1')[0]
        radius = 7.5
        max_vol = 15
    else:
        source = labware.load(
            'opentrons_15_tuberack_falcon_15ml_conical', '1')[0]
        radius = 13.5
        max_vol = 50

    select_tiprack = list(takewhile(
        lambda x: tube_rack_type in x and tube_type in x, tuberack_names))[0]
    tube_racks = [labware.load(select_tiprack, str(slot))
                  for slot in range(2, 2+number_of_racks)]

    # pipette setup
    if pipette_type in ['P50_Single', 'P300_Single']:
        tiprack_name = 'opentrons_96_tiprack_300ul'
    elif pipette_type == 'P10_Single':
        tiprack_name = 'opentrons_96_tiprack_10ul'
    else:
        tiprack_name = 'opentrons_96_tiprack_1000ul'
    tiprack = labware.load(tiprack_name, '11')

    if starting_tip not in tiprack.children_by_name:
        raise Exception('Starting well does not exist. Pick between A1-H12.')

    pip = getattr(instruments, pipette_type)(
        mount=pipette_mount, tip_racks=[tiprack])

    tip_depth = 20 + (max_vol - starting_stock_volume_in_mL) \
        * 1000 / (math.pi * (radius ** 2))

    def track_source_loc(volume):
        # update height to aspirate at source tube before each transfer
        nonlocal tip_depth, source
        tip_depth += volume / (math.pi * (radius ** 2))
        if tip_depth > 98:
            return source.bottom(3)
        else:
            return source.top(-tip_depth)

    # transfer solution to each tube, allow to recap after every 2 racks
    pip.start_at_tip(tiprack.wells(starting_tip))
    pip.pick_up_tip()
    for index, rack in enumerate(tube_racks):
        for dest in rack.wells():
            pip.transfer(transfer_volume,
                         track_source_loc(transfer_volume),
                         dest,
                         new_tip='never')
            if index % 2 == 0 and index != 0:
                robot.pause('Pausing the protocol for capping the tubes. '
                            'Resume when ready.')
    pip.drop_tip()
