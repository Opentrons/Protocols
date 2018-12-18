from opentrons import labware, instruments
from otcustomizers import StringSelection

metadata = {
    'protocolName': 'ELISA Plate Washing',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
    }

trough_name = 'trough-single-chamber'
if trough_name not in labware.list():
    labware.create(
        trough_name,
        grid=(1, 1),
        spacing=(0, 0),
        diameter=72,
        depth=39)

# labware setup
wash_buffer = labware.load(trough_name, '1').wells('A1')
liquid_trash = labware.load(trough_name, '4').wells('A1')
plates = [labware.load('96-flat', slot)
          for slot in ['2', '3', '5', '6']]
tipracks = [labware.load('opentrons-tiprack-300ul', slot)
            for slot in ['7', '8', '9', '10', '11']]

# instruments setup
m300 = instruments.P300_Multi(
    mount='left',
    tip_racks=tipracks)


def run_custom_protocol(
    wash_solution_volume: float=250,
    tip_change_strategy: StringSelection(
        'use one set of tips only', 'new tip each well')='new tip each well',
    number_of_plates: int=4
        ):

    target_plates = [col for plate in plates[:number_of_plates]
                     for col in plate.cols()]

    m300.transfer(
        wash_solution_volume,
        wash_buffer,
        [col[0].top() for col in target_plates])

    if tip_change_strategy == 'use one set of tips only':
        m300.pick_up_tip()
    for col in target_plates:
        if not m300.tip_attached:
            m300.pick_up_tip()
        m300.transfer(wash_solution_volume, col, liquid_trash, new_tip='never')
        if tip_change_strategy == 'new tip each well':
            m300.drop_tip()
    if m300.tip_attached:
        m300.drop_tip()
