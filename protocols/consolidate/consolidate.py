from opentrons import containers, instruments
from otcustomizers import StringSelection

trash = containers.load('trash-box', 'B2')


def tiprack_from_pipette(pipette_vol):
    if pipette_vol <= 10:
        return 'tiprack-10ul'
    if 1000 > pipette_vol > 10:
        return 'tiprack-200ul'
    if pipette_vol == 1000:
        return 'tiprack-1000ul'
    raise ValueError('No known tiprack for a p{} pipette'.format(pipette_vol))


def run_custom_protocol(
        pipette_axis: StringSelection(
            'B (left side)', 'A (right side)')='B (left side)',
        pipette_model: StringSelection(
            'p200', 'p100', 'p50', 'p20', 'p10', 'p1000')='p200',
        consolidate_volume: float=20.0,
        source_container: StringSelection(
            '96-flat', 'tube-rack-2ml')='96-flat',
        number_of_source_wells: int=4,
        destination_container: StringSelection(
            '96-flat', 'tube-rack-2ml')='96-flat',
        destination_well: str='A1',
        tip_reuse_strategy: StringSelection(
            'reuse one tip', 'new tip each time')='reuse one tip'):

    pipette_max_vol = int(pipette_model[1:])
    new_tip = 'always' if tip_reuse_strategy == 'new tip each time' else 'once'
    tip_rack = containers.load(tiprack_from_pipette(pipette_max_vol), 'A1')

    source = containers.load(source_container, 'D1')
    dest = containers.load(destination_container, 'B1')

    try:
        dest_well = dest.wells(destination_well)
    except ValueError:
        raise RuntimeError(
            'Invalid destination well "{}". Expected well name like A1, H11, '
            .format(destination_well) + 'etc. The destination plate may not ' +
            'have a well of that name (eg a 96-well plate has no well "T18")')

    pipette = instruments.Pipette(
        axis=pipette_axis[0].lower(),
        max_volume=pipette_max_vol,
        min_volume=pipette_max_vol / 10,
        tip_racks=[tip_rack],
        trash_container=trash
    )

    pipette.consolidate(
        consolidate_volume,
        source[:number_of_source_wells],
        dest_well,
        new_tip=new_tip)
