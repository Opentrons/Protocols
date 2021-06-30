metadata = {
    'protocolName': 'PCR Prep with Frozen Aluminum Block',
    'author': 'Rami Farawi <rami.farawi@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.9'
}


def run(ctx):

    [num_col, sample_vol, mmx_vol, source_asp_height_plate,
     source_asp_height_plate_mmx, source_asp_flow_rate_plate, delay,
     source_asp_flow_rate_mmx, dispense_height, dest_flow_rate_sample,
     dest_flow_rate_mmx, mix_vol, mix_reps,
     p20_mount, m20_mount] = get_values(  # noqa: F821
        "num_col", "sample_vol", "mmx_vol", "source_asp_height_plate",
        "source_asp_height_plate_mmx", "source_asp_flow_rate_plate", "delay",
        "source_asp_flow_rate_mmx", "dispense_height", "dest_flow_rate_sample",
        "dest_flow_rate_mmx", "mix_vol", "mix_reps", "p20_mount", "m20_mount")

    if not 0 <= num_col <= 12:
        raise Exception("Enter a column number between 1 and 12")

    # load labware
    sample_plate = ctx.load_labware(
                'nest_96_wellplate_100ul_pcr_full_skirt', '1')
    dest_plate = ctx.load_labware(
                'nest_96_wellplate_100ul_pcr_full_skirt', '2')
    mastermix = ctx.load_labware(
                'opentrons_24_aluminumblock_nest_1.5ml_snapcap', '3')
    tiprack_single = ctx.load_labware('opentrons_96_filtertiprack_20ul', '4')
    tiprack_multi = ctx.load_labware('opentrons_96_filtertiprack_20ul', '5')

    # load pipette
    p20 = ctx.load_instrument('p20_single_gen2',
                              p20_mount, tip_racks=[tiprack_single])
    m20 = ctx.load_instrument('p20_multi_gen2',
                              m20_mount, tip_racks=[tiprack_multi])

    # load reagents
    mmx = mastermix.wells()[0]

    # PROTOCOL
    p20.flow_rate.aspirate = source_asp_flow_rate_mmx
    p20.flow_rate.dispense = dest_flow_rate_mmx
    m20.flow_rate.aspirate = source_asp_flow_rate_plate
    m20.flow_rate.dispense = dest_flow_rate_sample
    num_samp = num_col*8
    airgap = 3

    # transfer mastermix to plate
    p20.pick_up_tip()
    for i, dest in enumerate(dest_plate.wells()[:num_samp]):
        if not p20.has_tip:
            p20.pick_up_tip()
        p20.aspirate(mmx_vol, mmx.bottom(source_asp_height_plate_mmx))
        ctx.delay(seconds=delay)
        p20.touch_tip()
        p20.dispense(mmx_vol, dest.bottom(dispense_height))
        p20.blow_out()
        if (i+1) % 8 == 0:
            p20.drop_tip()
            ctx.comment('\n')

    # transfer sample to plate
    for s_col, d_col in zip(sample_plate.rows()[0][:num_col],
                            dest_plate.rows()[0]):
        m20.pick_up_tip()
        m20.aspirate(sample_vol, s_col.bottom(source_asp_height_plate))
        m20.air_gap(airgap)
        m20.touch_tip()
        m20.dispense(sample_vol+airgap, d_col.bottom(dispense_height))
        m20.mix(mix_reps, mix_vol, d_col)
        m20.blow_out()
        m20.drop_tip()
