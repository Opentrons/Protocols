metadata = {
    'protocolName': 'mock pooling',
    'author': 'Steve <protocols@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.9'
}


def run(ctx):

    ctx.set_rail_lights(True)

    [pool_location, wells_to_be_pooled, tip_rack
     ] = get_values(  # noqa: F821
        "pool_location", "wells_to_be_pooled", "tip_rack")

    # tips and p300 multi
    tipracks = [ctx.load_labware('opentrons_96_tiprack_300ul', '4')]
    p300m = ctx.load_instrument('p300_multi_gen2', 'right')

    # labware
    [ninety_six_2_ml, tube_rack] = [
     ctx.load_labware(labware, slot) for labware, slot in zip(
      ['nest_96_wellplate_2ml_deep',
       'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap'], ['5', '6'])]

    # pool tube
    pool = tube_rack.wells_by_name()[pool_location]

    # use only the rear-most channel of the p300 multi
    num_channels_per_pickup = 1  # (only pickup tips on rear-most channel)
    tips_ordered = [
        tip for rack in tipracks
        for row in rack.rows()[
         len(rack.rows())-num_channels_per_pickup::-1*num_channels_per_pickup]
        for tip in row]

    tip_count = 0

    def pick_up(pip):
        nonlocal tip_count
        pip.pick_up_tip(tips_ordered[tip_count])
        tip_count += 1

    # transfer 20 ul from designated wells to pool
    for well in wells_to_be_pooled.split(','):
        pick_up(p300m)
        p300m.aspirate(20, ninety_six_2_ml.wells_by_name()[well])
        p300m.dispense(20, pool)
        p300m.drop_tip()
