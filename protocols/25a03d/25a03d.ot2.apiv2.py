metadata = {
    'protocolName': 'qPCR Prep in Triplicates',
    'author': 'Rami Farawi <rami.farawi@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.11'
}


def run(ctx):

    [num_samp, final_plate_slot4, control_plate,
     p20_mount, p300_mount] = get_values(  # noqa: F821
        "num_samp", "final_plate_slot4",
        "control_plate", "p20_mount", "p300_mount")

    num_samp = int(num_samp)

    # load labware
    final_plate = ctx.load_labware(final_plate_slot4, '4')
    mastermix_rack = ctx.load_labware(
                    'usalowbind_24_aluminumblock_2000ul', '1')
    dna_samples = ctx.load_labware(
                  'usastrips_96_aluminumblock_200ul', '7')
    control_plate = ctx.load_labware(control_plate, '9')

    tiprack200 = [ctx.load_labware('opentrons_96_tiprack_300ul', '10')]
    tiprack20 = [ctx.load_labware('opentrons_96_tiprack_20ul', '11')]

    # load instrument
    m20 = ctx.load_instrument('p20_multi_gen2', p20_mount,
                              tip_racks=tiprack20)
    p300 = ctx.load_instrument('p300_multi_gen2', p300_mount,
                               tip_racks=tiprack200)

    # PROTOCOL
    num_cols = int(num_samp/8)
    final_wells = final_plate.rows()[0][::3]
    final_wells_single_chan = [well for col in final_plate.columns()[::3]
                               for well in col]

    # distribute mastermix
    mastermix = mastermix_rack.wells()[0]
    p300.pick_up_tip()
    for i, well in enumerate(final_wells_single_chan[:num_samp+8]):
        p300.aspirate(48, mastermix, rate=0.75)
        ctx.delay(4)
        p300.dispense(24, mastermix, rate=0.75)
        p300.aspirate(24, mastermix, rate=0.75)
        ctx.delay(4)
        p300.dispense(48, well, rate=0.75)
        ctx.delay(1)
        p300.blow_out()
        if i % 7 == 0 and i > 0:
            p300.drop_tip()
            p300.pick_up_tip()
            ctx.comment('\n')
    ctx.comment('\n\n\n')

    # distribute sample to mastermix
    airgap = 3
    for s_col, d_col in zip(dna_samples.rows()[0][:num_cols], final_wells):
        m20.pick_up_tip()
        m20.aspirate(12, s_col)
        m20.touch_tip()
        m20.air_gap(airgap)
        m20.dispense(12+airgap, d_col)
        m20.touch_tip()
        m20.blow_out()
        m20.drop_tip()
    ctx.comment('\n\n\n')

    # add control
    control = control_plate.rows()[0][-1]
    m20.pick_up_tip()
    m20.aspirate(12, control)
    m20.dispense(12, final_wells[3])
    m20.drop_tip()
    ctx.comment('\n\n\n')

    for i, column in enumerate(final_wells[:num_cols+1]):
        m20.pick_up_tip()
        m20.mix(5, 20, column)
        m20.blow_out()
        m20.aspirate(20, column)
        m20.dispense(20, final_plate.rows()[0][i*3+1])
        m20.blow_out()
        m20.aspirate(20, column)
        m20.dispense(20, final_plate.rows()[0][i*3+2])
        m20.blow_out()
        m20.drop_tip()
