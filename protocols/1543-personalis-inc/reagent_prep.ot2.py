from opentrons import labware, instruments
from otcustomizers import StringSelection
import math

metadata = {
    'protocolName': 'Reagent Prep',
    'author': 'Alise <protcols@opentrons.com>',
    'source': 'Custom Protocol Request'
    }


def run_custom_protocol(
        source_tube_type: StringSelection('15-mL', '50-mL')='50-mL',
        starting_stock_volume_in_mL: float=50,
        transfer_volume: float=350,
        number_of_samples: int=50
        ):

    # labware setup
    dest_racks = [labware.load('opentrons-aluminum-block-2ml-screwcap', slot)
                  for slot in ['2', '4', '5']]
    tiprack = labware.load('tiprack-1000ul', '3')

    # instrument setup
    p1000 = instruments.P1000_Single(
        mount='left',
        tip_racks=[tiprack])

    dest_tubes = [well for rack in dest_racks for well in rack]

    # define source tube
    if source_tube_type == '15-mL':
        source_rack = labware.load('opentrons-tuberack-15ml', '1')
        radius = 7.5
        max_vol = 15
    else:
        source_rack = labware.load('opentrons-tuberack-15ml', '1')
        radius = 13.5
        max_vol = 50

    source = source_rack.wells('A1')
    tip_depth = 20 + (max_vol - starting_stock_volume_in_mL) \
        * 1000 / (math.pi * (radius ** 2))
    source_loc = source.top(-tip_depth)
    remaining_volume = starting_stock_volume_in_mL * 1000

    def new_source_depth(volume):
        nonlocal remaining_volume, tip_depth, source, source_loc
        if remaining_volume < volume:
            source = next(source)
            remaining_volume = starting_stock_volume_in_mL * 1000
            tip_depth = 20 + (max_vol - starting_stock_volume_in_mL) \
                * 1000 / (math.pi * (radius ** 2))
        tip_depth += volume / (math.pi * (radius ** 2))
        remaining_volume -= volume
        if tip_depth > 98:
            source_loc = source.bottom(3)
        else:
            source_loc = source.top(-tip_depth)

    p1000.set_flow_rate(aspirate=300, dispense=500)
    p1000.pick_up_tip()
    p1000.aspirate(1000, source_loc)
    p1000.delay(seconds=1)
    p1000.touch_tip()
    for well in dest_tubes[:number_of_samples]:
        repetition = math.ceil(transfer_volume / 1000)
        new_vol = transfer_volume / repetition
        for _ in range(repetition):
            new_source_depth(new_vol)
            if p1000.current_volume < new_vol:
                p1000.aspirate(source_loc)
                p1000.delay(seconds=1)
                p1000.touch_tip()
            p1000.dispense(new_vol, well)
    p1000.dispense(source_loc)
    p1000.drop_tip()
