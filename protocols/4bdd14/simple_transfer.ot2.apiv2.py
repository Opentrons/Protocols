metadata = {
    'ctxName': 'Simple Plate Transfer',
    'author': 'Nick <ndiehl@opentrons.com',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.8'
}


def run(ctx):
    [m300_mount, num_plates] = get_values(  # noqa: F821
     'm300_mount', 'num_plates')

    # load labware
    tips300 = [ctx.load_labware('opentrons_96_tiprack_300ul', '1')]
    source_plate = ctx.load_labware('nest_96_wellplate_2ml_deep', '2',
                                    'source plate')
    dest_plates = [
        ctx.load_labware('greinermicrolon_96_wellplate_340ul', str(slot),
                         f'plate {i+1}')
        for i, slot in enumerate(range(3, 3+num_plates))]

    # load pipettes
    m300 = ctx.load_instrument('p300_multi', m300_mount, tip_racks=tips300)

    for i in range(4):
        m300.pick_up_tip()
        col_inds = [i, i+4, i+8]
        for i in col_inds:
            m300.distribute(50, source_plate.rows()[0][i],
                            [plate.columns()[i] for plate in dest_plates],
                            disposal_vol=0, new_tip='never')
        m300.drop_tip()
