from opentrons import labware, instruments
from otcustomizers import StringSelection

"""
Step 3: PCR Lysis
"""

tiprack_dict = {'p10': 'tiprack-10ul',
                'p50': 'tiprack-200ul',
                'p300': 'opentrons-tiprack-300ul'}


def run_custom_protocol(
        cell_container: StringSelection(
            '24-well-plate', '96-flat')='96-flat',
        pipette_model: StringSelection(
            'p10-Single', 'p50-Single', 'p300-Single', 'p10-Multi',
            'p50-Multi', 'p300-Multi')='p300-Single',
        pipette_mount: StringSelection(
            'left', 'right')='right',
        reagent_container: StringSelection(
            'trough-12row', 'opentrons-tuberack-50ml',
            'opentrons-tuberack-15_50ml')='trough-12row',
        sample_num: int=96,
        discard_media_volume: int=200,
        buffer_volume: int=100,
        delay_minutes: int=15):

    old_plates = [labware.load(cell_container, '2')]
    trough = labware.load('trough-12row', '3')

    # reagent setup
    reagents = labware.load(reagent_container, '5')
    buffer = reagents.wells('A1')
    liquid_trash = trough.wells('A1')

    pipette_name = pipette_model.split('-')[0]
    channel = pipette_model.split('-')[1]

    tipracks = [labware.load(tiprack_dict[pipette_name], slot)
                for slot in ['4', '6']]

    if pipette_model == 'p10-Single':
        pipette = instruments.P10_Single(
            mount=pipette_mount,
            tip_racks=tipracks)
    elif pipette_model == 'p50-Single':
        pipette = instruments.P50_Single(
            mount=pipette_mount,
            tip_rakcs=tipracks)
    elif pipette_model == 'p300-Single':
        pipette = instruments.P300_Single(
            mount=pipette_mount,
            tip_racks=tipracks)
    elif pipette_model == 'p10-Multi':
        pipette = instruments.P10_Multi(
            mount=pipette_mount,
            tip_racks=tipracks)
    elif pipette_model == 'p50-Multi':
        pipette = instruments.P50_Multi(
            mount=pipette_mount,
            tip_racks=tipracks)
    elif pipette_model == 'p300-Multi':
        pipette = instruments.P300_Multi(
            mount=pipette_mount,
            tip_racks=tipracks)

    if channel == 'Multi':
        col_num = sample_num // 8 + (1 if sample_num % 8 > 0 else 0)
        old_locs = [col for plate in old_plates for col in plate.cols()][
            :col_num]
        multiplier = 8
    else:
        old_locs = [well for plate in old_plates for well in plate.wells()][
            :sample_num]
        multiplier = 1

    volume = 21000
    # discard media from plate
    for loc in old_locs:
        if volume < discard_media_volume * multiplier:
            liquid_trash = next(liquid_trash)
            volume = 21000
        print(liquid_trash.top())
        pipette.transfer(discard_media_volume, loc, liquid_trash.top())
        volume -= discard_media_volume * multiplier

    # add pre-made buffer
    pipette.pick_up_tip()
    for loc in old_locs:
        pipette.transfer(buffer_volume, buffer, loc.top(), new_tip='never')
    pipette.drop_tip()

    # delay
    pipette.delay(minutes=delay_minutes)
