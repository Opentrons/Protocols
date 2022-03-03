from opentrons.types import Point

metadata = {
    'protocolName': 'Cell Culture',
    'author': 'Nick Diehl <ndiehl@opentrons.com>',
    'description': 'Custom Protocol Request',
    'apiLevel': '2.11'
}


def run(ctx):

    num_plates, p300_mount, p20_mount = get_values(  # noqa: F821
        'num_plates', 'p300_mount', 'p20_mount')

    plates = [
        ctx.load_labware('corning_96_wellplate_360ul_flat', f'{slot}',
                         f'plate {slot}')
        for slot in range(1, 1+num_plates)]
    tipracks200 = [ctx.load_labware('opentrons_96_filtertiprack_200ul', '9')]
    tipracks20 = [ctx.load_labware('opentrons_96_filtertiprack_20ul', '10')]
    tuberack = ctx.load_labware(
        'opentrons_10_tuberack_falcon_4x50ml_6x15ml_conical', '11')

    p300 = ctx.load_instrument('p300_single_gen2', p300_mount,
                               tip_racks=tipracks200)
    p20 = ctx.load_instrument('p20_single_gen2', p20_mount,
                              tip_racks=tipracks20)

    volumes = [50, 25, 12.5, 6.25, 3.125, 1.5625, 0.78125]

    # transfer
    p300.pick_up_tip()
    p20.pick_up_tip()
    for vol, col_ind in zip(volumes[:6], range(6)):
        pip = p300 if vol >= 20 else p20
        for plate in plates:
            for well in plate.columns()[col_ind]:
                pip.transfer(vol, tuberack.wells_by_name()['A1'], well,
                             new_tip='never')
    p300.drop_tip()
    p20.drop_tip()

    p300.pick_up_tip()
    p20.pick_up_tip()
    for vol, col_ind in zip(volumes[:5], range(6, 11)):
        pip = p300 if vol >= 20 else p20
        for plate in plates:
            for well in plate.columns()[col_ind]:
                pip.aspirate(vol, tuberack.wells_by_name()['A2'])
                pip.move_to(well.top(-1))
                pip.dispense(vol, well.move(Point(x=well.diameter/2, z=-1)))
    p300.drop_tip()
    p20.drop_tip()

    p300.pick_up_tip()
    p20.pick_up_tip()
    for vol, row_ind in zip(volumes, range(7)):
        pip = p300 if vol >= 20 else p20
        for plate in plates:
            for well in plate.rows()[row_ind]:
                pip.aspirate(vol, tuberack.wells_by_name()['B1'])
                pip.move_to(well.top(-1))
                pip.dispense(vol, well.move(Point(x=well.diameter/2, z=-1)))
    p300.drop_tip()
    p20.drop_tip()
