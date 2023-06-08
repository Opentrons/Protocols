import math
from opentrons import protocol_api

metadata = {
    'protocolName': 'Media Refilling',
    'author': 'Nick Diehl <ndiehl@opentrons.com>',
    'apiLevel': '2.13'
}

offset_aspiration_from_bottom = 0.5
offset_dispense_from_top = -1.0


def run(ctx):

    [vol_refill, num_lw, lw_refill, lw_media, type_pip,
     mount_pip] = get_values(  # noqa:F821
     'vol_refill', 'num_lw', 'lw_refill', 'lw_media', 'type_pip',
     'mount_pip')

    tip_vol_map = {
        20: '20',
        300: '200',
        1000: '1000'
    }

    pipette = ctx.load_instrument(type_pip, mount_pip)
    tiprack_type = f'opentrons_96_filtertiprack_\
{tip_vol_map[int(pipette.max_volume)]}ul'

    plates = [
        ctx.load_labware(lw_refill, slot)
        for slot in range(1, 1+num_lw)]
    media = ctx.load_labware(lw_media, '10', 'media reservoir (A1)').wells()[0]
    waste = ctx.load_labware(
        lw_media, '11', 'waste reservoir').wells()[0].top()

    grid_size = len(plates[0].rows()) * len(plates[0].columns())
    if grid_size < 96 and pipette.channels == 8:
        raise Exception('Incompatible labware with 8-channel pipette.')

    tipracks = [
        ctx.load_labware(tiprack_type, slot)
        for slot in range(num_lw+1, 10)]
    pipette.tip_racks = tipracks
    if pipette.channels == 8:
        pipette.starting_tip = pipette.tip_racks[0].rows()[0][1]
    else:
        pipette.starting_tip = pipette.tip_racks[0].wells()[1]
    media_tip = pipette.tip_racks[0].wells()[0]

    def slow_withdraw(well, delay_seconds=2.0, pip=pipette):
        pip.default_speed /= 16
        if delay_seconds > 0:
            ctx.delay(seconds=delay_seconds)
        pip.move_to(well.top())
        pip.default_speed *= 16

    def pick_up(pip=pipette):
        try:
            pip.pick_up_tip()
        except protocol_api.labware.OutOfTipsError:
            ctx.pause("Replace all tipracks")
            pip.reset_tipracks()
            if pip.channels == 8:
                pipette.starting_tip = pip.tip_racks[0].rows()[0][1]
            else:
                pipette.starting_tip = pip.tip_racks[0].wells()[1]
            pip.pick_up_tip()

    if pipette.channels == 8:
        if grid_size == 96:
            plate_locs = [well for plate in plates for well in plate.rows()[0]]
        else:
            plate_locs = [
                well for plate in plates
                for row in plate.rows()[:2]
                for well in row]
    else:
        plate_locs = [well for plate in plates for well in plate.wells()]

    num_trans = math.ceil(
        vol_refill/pipette.tip_racks[0].wells()[0].max_volume)
    vol_per_trans = round(vol_refill/num_trans, 1)

    for i, well in enumerate(plate_locs):
        # remove old volume
        pick_up()
        for _ in range(num_trans):
            pipette.aspirate(
                vol_per_trans, well.bottom(offset_aspiration_from_bottom))
            slow_withdraw(well)
            pipette.dispense(vol_per_trans, waste)
        pipette.drop_tip()

        # add media
        pipette.pick_up_tip(media_tip)
        for _ in range(num_trans):
            pipette.aspirate(vol_per_trans, media.bottom(2))
            slow_withdraw(media)
            pipette.dispense(vol_per_trans, well.top(offset_dispense_from_top))
            slow_withdraw(well)
        pipette.return_tip()
