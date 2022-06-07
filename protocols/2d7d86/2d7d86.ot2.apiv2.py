metadata = {
    'protocolName': 'UTI Batch qPCR Setup',
    'author': 'Rami Farawi <rami.farawi@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.11'
}


def run(ctx):

    [num_samp, m20_mount] = get_values(  # noqa: F821
        "num_samp", "m20_mount")

    if not 1 <= num_samp <= 14:
        raise Exception("Enter a column number between 1-12")

    # load labware
    source_plate = ctx.load_labware('thermofisherscientificdeepwell_96_wellplate_2000ul', 4)  # noqa: E501
    dest_plate = ctx.load_labware('thermofisher_384_wellplate_50ul', 5)
    tips = ctx.load_labware('opentrons_96_tiprack_20ul', 6)

    # load instrument
    m20 = ctx.load_instrument('p20_multi_gen2', m20_mount, tip_racks=[tips])

    tip_count = 0

    def pick_up(num_tips):
        num_channels_per_pickup = num_tips
        tips_ordered = [
            tip for row in tips.rows()[
                len(tips.rows())-num_channels_per_pickup::-1*num_channels_per_pickup]  # noqa: E501
            for tip in row]
        nonlocal tip_count
        m20.pick_up_tip(tips_ordered[tip_count])
        tip_count += 1

    # mapping
    if num_samp > 7:
        tip_pickup_first_col = 8
        tip_pickup_second_col = num_samp - 6
    if num_samp == 7:
        tip_pickup_first_col = 8
        tip_pickup_second_col = 1
    if num_samp < 7:
        tip_pickup_first_col = num_samp + 1
        tip_pickup_second_col = 1

    tip_pickups_by_col = [tip_pickup_first_col, tip_pickup_second_col]

    for i, pickup in enumerate(tip_pickups_by_col):
        if pickup > 0:
            pick_up(pickup)
            for dest in dest_plate.rows()[i]:
                m20.aspirate(10, source_plate.rows()[0][i])
                m20.dispense(10, dest)
            m20.drop_tip()
            ctx.comment('\n')
