from opentrons import labware, instruments
from otcustomizers import StringSelection

metadata = {
    'protocolName': 'Volume Validation Protocol',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Protocol Library'
}


def run_custom_protocol(
    pipette_size: StringSelection(
        'p10-Single', 'p50-Single', 'p300-Single',
        'p1000-Single')='p10-Single',
    pipette_mount: StringSelection('left', 'right')='left',
    tip_rack_type: StringSelection(
        'tiprack-10ul', 'tiprack-200ul', 'opentrons-tiprack-300ul',
        'tiprack-1000ul')='tiprack-10ul',
    test_volume: float=10,
    number_of_test_per_volume: int=10,
    source_labware: StringSelection(
        'trough-12row', 'opentrons-tuberack-2ml-eppendorf',
        'opentrons-tuberack-2ml-screwcap')='trough-12row'
        ):

    if number_of_test_per_volume > 96 or number_of_test_per_volume < 10:
        raise Exception("Number of tests must be 10 - 96.")

    if test_volume > 1000:
        raise Exception("Volume must be less than 1000 uL.")

    source = labware.load(source_labware, '1').wells('A1')
    output = [labware.load('opentrons-2ml-tuberack-eppendorf', str(slot))
              for slot in range(2, 6)]
    tiprack = labware.load(tip_rack_type, '11')

    pipette_arg = {'mount': pipette_mount, 'tip_racks': [tiprack]}

    if pipette_size == 'p10-Single':
        pipette = instruments.P10_Single(**pipette_arg)
    elif pipette_size == 'p50-Single':
        pipette = instruments.P50_Single(**pipette_arg)
    elif pipette_size == 'p300-Single':
        pipette = instruments.P300_Single(**pipette_arg)
    else:
        pipette = instruments.P1000_Single(**pipette_arg)

    targets = [tube
               for rack in output
               for tube in rack.wells()][:number_of_test_per_volume]

    for target in targets:
        pipette.pick_up_tip()
        if pipette_size == 'p300-Single' or pipette_size == 'p1000-Single':
            target = target.top()
        pipette.transfer(test_volume, source, target, new_tip='never')
        pipette.drop_tip()
        pipette.touch_tip()
        pipette.drop_tip()
