from opentrons import labware, instruments
from otcustomizers import StringSelection


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
            'left', 'right')='left',
        pipette_model: StringSelection(
            'p10', 'p50', 'p300', 'p1000')='p300',
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
    tip_rack = labware.load(tiprack_from_pipette(pipette_max_vol), '1')

    source = labware.load(source_container, '2')
    dest = labware.load(destination_container, '3')

    try:
        dest_well = dest.wells(destination_well)
    except ValueError:
        raise RuntimeError(
            'Invalid destination well "{}". Expected well name like A1, H11, '
            .format(destination_well) + 'etc. The destination plate may not ' +
            'have a well of that name (eg a 96-well plate has no well "T18")')

    if pipette_model == 'p10':
        pipette = instruments.P10_Single(
            mount=pipette_axis,
            tip_racks=[tip_rack])
    elif pipette_model == 'p50':
        pipette = instruments.P50_Single(
            mount=pipette_axis,
            tip_racks=[tip_rack])
    elif pipette_model == 'p300':
        pipette = instruments.P300_Single(
            mount=pipette_axis,
            tip_racks=[tip_rack])
    else:
        pipette = instruments.P1000_Single(
            mount=pipette_axis,
            tip_racks=[tip_rack])

    pipette.consolidate(
        consolidate_volume,
        source[:number_of_source_wells],
        dest_well,
        new_tip=new_tip)
