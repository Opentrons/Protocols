from opentrons import labware, instruments
from otcustomizers import StringSelection

"""
Step 1: Feeding Cells
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
        media_container: StringSelection(
            'trough-12row', 'opentrons-tuberack-50ml',
            'opentrons-tuberack-15_50ml')='trough-12row',
        sample_num: int=96,
        media_volume: float=200,
        tip_reuse_strategy: StringSelection(
            'reuse one tip', 'new tip each time')='reuse one tip'):

    plates = [labware.load(cell_container, '2')]

    media = labware.load(media_container, '5').wells('A1')

    pipette_name = pipette_model.split('-')[0]
    channel = pipette_model.split('-')[1]

    new_tip = 'once' if tip_reuse_strategy == 'new tip each time' else 'never'
    tipracks = [labware.load(tiprack_dict[pipette_name], '4')]

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
        locs = [col for plate in plates for col in plate.cols()][:col_num]
    else:
        locs = [well for plate in plates for well in plate.wells()][
            :sample_num]

    media_source = media
    volume_tracker = media_source.max_volume()

    if new_tip == 'never':
        pipette.pick_up_tip()

    for loc in locs:
        if volume_tracker < media_volume:
            media_source = next(media_source)
            volume_tracker = media_source.max_volume()
        pipette.transfer(media_volume, media_source, loc, new_tip=new_tip)
        volume_tracker = volume_tracker - media_volume * (
            8 if channel == 'Multi' else 1)
    if new_tip == 'never':
        pipette.drop_tip()
