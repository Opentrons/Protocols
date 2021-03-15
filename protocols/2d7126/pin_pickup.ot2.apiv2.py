metadata = {
    'protocolName': '8-Pin Pickup',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.9'
}


def run(ctx):

    # [m300_mount] = get_values(  # noqa: F821
    #     'm300_mount')

    m300_mount = 'left'
    # labware
    plate1, plate2 = [
        ctx.load_labware('corning_96_wellplate_360ul_flat', slot,
                         'plate ' + str(i+1))
        for i, slot in enumerate(['1', '2'])]
    pinrack = [
        ctx.load_labware('opentrons_96_tiprack_300ul', '5',
                         'custom pin adapter')]

    # pipette
    m300 = ctx.load_instrument('p300_multi', m300_mount, tip_racks=pinrack)

    m300.pick_up_tip()
    for col1, col2 in zip(plate1.rows()[0], plate2.rows()[0]):
        # plate 1
        m300.default_speed = 40
        for _ in range(3):
            m300.move_to(col1.top(1))
            m300.move_to(col1.bottom(-0.5))
        m300.default_speed = 400

        # plate 2
        m300.default_speed = 40
        for _ in range(3):
            m300.move_to(col1.top(1))
            m300.move_to(col1.bottom(-0.5))
            ctx.delay(seconds=3)
        m300.default_speed = 400

    m300.default_speed = 40
    m300.return_tip()
