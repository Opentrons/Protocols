import math

metadata = {
    'protocolName': 'Standard Curve Creation',
    'author': 'Nick <ndiehl@opentrons.com>',
    'apiLevel': '2.13',
    'description': ''
}

num_curves = 1
flow_rate_modulator = 0.25  # 25% of default flow rates
reps_mix = 5
vol_mix = 100.0


def run(ctx):

    # labware
    plate = ctx.load_labware('nest_96_wellplate_2ml_deep', '1')
    tuberack = ctx.load_labware(
        'opentrons_24_aluminumblock_nest_1.5ml_snapcap', '4')
    tiprack20 = [ctx.load_labware('opentrons_96_filtertiprack_20ul', '3')]
    tiprack200 = [ctx.load_labware('opentrons_96_filtertiprack_200ul', '6')]

    # pipettes
    p20 = ctx.load_instrument('p20_single_gen2', 'left', tip_racks=tiprack20)
    p300 = ctx.load_instrument(
        'p300_single_gen2', 'right', tip_racks=tiprack200)

    # slow flow rates for blood
    p20.flow_rate.aspirate *= flow_rate_modulator
    p300.flow_rate.aspirate *= flow_rate_modulator
    p20.flow_rate.dispense *= flow_rate_modulator
    p300.flow_rate.dispense *= flow_rate_modulator

    vol_stock = 4.0
    vols_dilution = [50, 50, 50, 50, 50, 50, 50, 50, 50, 50]

    # liquids
    stocks_b = tuberack.wells()[:num_curves]

    def slow_withdraw(pip, well, delay_seconds=2.0):
        pip.default_speed /= 16
        if delay_seconds > 0:
            ctx.delay(seconds=delay_seconds)
        pip.move_to(well.top())
        pip.default_speed *= 16

    def mix_high_low(pip,
                     reps,
                     vol,
                     well,
                     z_offset_low=2.0,
                     z_offset_high=5.0):
        for _ in range(reps):
            pip.aspirate(vol, well.bottom(z_offset_low))
            pip.dispense(vol, well.bottom(z_offset_high))

    """ PROTOCOL STEPS"""
    for n in range(num_curves):

        # initial stock transfer to plate
        stock_source = stocks_b[n]
        p20.pick_up_tip()
        p20.aspirate(2, stock_source.top())  # pre-airgap
        p20.aspirate(vol_stock, stock_source.bottom(3))
        slow_withdraw(p20, stock_source)
        p20.dispense(p20.current_volume, plate.rows()[n][0].bottom(5))
        slow_withdraw(p20, plate.rows()[n][0])
        p20.drop_tip()

        # serial dilution
        sources = plate.rows()[n][:10]
        destinations = plate.rows()[n][1:11]

        vol_reverse_pipette = 20.0

        for i, (vol_dilution, s, d) in enumerate(
                zip(vols_dilution, sources, destinations)):
            p300.pick_up_tip()
            mix_high_low(p300, reps_mix, vol_mix, s)
            p300.aspirate(vol_reverse_pipette, s.bottom(2))
            p300.aspirate(vol_dilution, s.bottom(2))
            slow_withdraw(p300, s)
            p300.dispense(vol_dilution, d.bottom(2))
            slow_withdraw(p300, d)
            if i == len(sources) - 1:
                p300.drop_tip()
                p300.pick_up_tip()
                mix_high_low(p300, reps_mix, vol_mix, d)
            p300.drop_tip()
