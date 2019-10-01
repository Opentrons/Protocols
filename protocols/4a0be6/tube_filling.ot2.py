import math
from opentrons import labware, instruments, robot
from otcustomizers import StringSelection

metadata = {
    'protocolName': 'Tube Filling',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
    }

tube_vars = ['0.5', '1.5', '2.0']
depth_vars = [24.6, 42.2, 43.4]
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

# create definition for BC trough
trough_name = 'beckman-coulter-trough-1-well-150ml'
if trough_name not in labware.list():
    labware.create(
        trough_name,
        grid=(1, 1),
        spacing=(0, 0),
        depth=35.74,
        diameter=9.67)


def run_custom_protocol(
        transfer_volume: float=105,
        tube_rack_type: StringSelection('48-well', '24-well')='48-well',
        tube_type: StringSelection('0.5-ml', '1.5-ml', '2.0-ml')='0.5-ml',
        number_of_racks: int=2,
        source_container_type: StringSelection(
            '15-ml', '50-ml', 'trough')='15-ml',
        starting_stock_volume_in_mL: float=15,
        pipette_type: StringSelection(
            'P10_Single', 'P50_Single', 'P300_Single',
            'P1000_Single')='P300_Single',
        pipette_mount: StringSelection('left', 'right')='left',
        starting_tip: str='A1',
        dispense_mode: StringSelection('Transfer', 'Distribute')='Transfer'
        ):

    def track_source_loc(volume):
        """update height to aspirate at source tube before each transfer
        """
        nonlocal tip_depth, source
        tip_depth += volume / (math.pi * (radius ** 2))
        if tip_depth > 98:
            return source.bottom(3)
        else:
            return source.top(-tip_depth)

    def yield_groups(list, num):
            """yield lists based on number of items
            """
            for i in range(0, len(list), num):
                yield list[i:i+num]

    # labware setup
    if number_of_racks > 9:
        raise Exception('The max number of racks to be filled 9. '
                        'Please try again.')

    # define source container
    if source_container_type == 'trough':
        source = labware.load(
            'beckman-coulter-trough-1-well-150ml', '1')[0]
    else:
        # source aspirate height will need to be determined if using
        # 15 or 50 mL tubes
        if source_container_type == '15-ml':
            source = labware.load(
                'opentrons_15_tuberack_falcon_15ml_conical', '1')[0]
            radius = 7.5
            max_vol = 15
        else:
            source = labware.load(
                'opentrons_6_tuberack_falcon_50ml_conical', '1')[0]
            radius = 13.5
            max_vol = 50
        tip_depth = 20 + (max_vol - starting_stock_volume_in_mL) \
            * 1000 / (math.pi * (radius ** 2))

    # select tuberack
    select_tuberack = list(filter(
        lambda x: tube_rack_type in x and tube_type in x, tuberack_names))[0]
    tube_racks = [labware.load(select_tuberack, str(slot))
                  for slot in range(2, 2+number_of_racks)]

    # pipette setup
    if pipette_type in ['P50_Single', 'P300_Single']:
        tiprack_name = 'opentrons_96_tiprack_300ul'
    elif pipette_type == 'P10_Single':
        tiprack_name = 'opentrons_96_tiprack_10ul'
    else:
        tiprack_name = 'opentrons_96_tiprack_1000ul'
    tiprack = labware.load(tiprack_name, '11')

    # make sure starting tip exists
    if starting_tip not in tiprack.children_by_name:
        raise Exception('Starting well does not exist. Pick between A1-H12.')

    pip = getattr(instruments, pipette_type)(
        mount=pipette_mount, tip_racks=[tiprack])

    # get number of distributes pipette can handle
    distribute_num = pip.max_volume // transfer_volume
    if distribute_num < 1:
        # if transfer volume is greater than pipette max volume,
        # use Transfer mode
        dispense_mode = 'Transfer'

    pip.start_at_tip(tiprack.wells(starting_tip))
    pip.pick_up_tip()
    all_wells = [well for tuberack in tube_racks for well in tuberack.wells()]
    if dispense_mode == 'Transfer':
        for dest in all_wells:
            # get source location (height varies if using conical tubes)
            source_loc = source if source_container_type == 'trough' else \
                track_source_loc(transfer_volume)
            pip.transfer(
                transfer_volume, source_loc, dest, new_tip='never')
    else:
        well_groups = list(yield_groups(all_wells, int(distribute_num)))
        for wells in well_groups:
            source_loc = source if source_container_type == 'trough' else \
                track_source_loc(transfer_volume * distribute_num)
            pip.distribute(
                transfer_volume, source_loc, wells, blow_out=source,
                new_tip='never')
    pip.drop_tip()
