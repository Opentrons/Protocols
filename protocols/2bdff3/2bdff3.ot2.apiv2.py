metadata = {
    'protocolName': 'Post RC-PCR Pooling of Nimagen SARS CoV-2 Library Prep',
    'author': 'Sakib <sakib.hossain@opentrons.com>',
    'description': 'Custom Protocol Request',
    'apiLevel': '2.9'
}


def run(ctx):

    [step1, step2, quad1_cols, quad2_cols, quad3_cols, quad4_cols, m20_mount,
        p300_mount, donor_384_type, trans_vol1,
        step1_mix_vol] = get_values(  # noqa: F821
        "step1", "step2", "quad1_cols", "quad2_cols", "quad3_cols",
        "quad4_cols", "m20_mount", "p300_mount", "donor_384_type",
        "trans_vol1", "step1_mix_vol")

    # Load Labware
    donor_384_plate = ctx.load_labware(donor_384_type, 1)
    recipient_96_plate = ctx.load_labware(
        'eppendorftwin.tec_96_wellplate_150ul', 2)
    tiprack_20ul = [ctx.load_labware('opentrons_96_filtertiprack_20ul', slot)
                    for slot in [4, 5, 6, 7]]
    tiprack_200ul = [ctx.load_labware('opentrons_96_filtertiprack_200ul', slot)
                     for slot in [8]]
    tuberack = ctx.load_labware(
            'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', 3)['A1']

    # Load Pipettes
    m20 = ctx.load_instrument('p20_multi_gen2', m20_mount,
                              tip_racks=tiprack_20ul)
    p300 = ctx.load_instrument('p300_single_gen2', p300_mount,
                               tip_racks=tiprack_200ul)

    # Get wells by quadrant
    quad1 = [col for col in donor_384_plate.rows()[0][::2]][:quad1_cols]
    quad2 = [col for col in donor_384_plate.rows()[0][1::2]][:quad2_cols]
    quad3 = [col for col in donor_384_plate.rows()[1][::2]][:quad3_cols]
    quad4 = [col for col in donor_384_plate.rows()[1][1::2]][:quad4_cols]

    # Step 1
    if step1 == "True":
        for quad in [quad1, quad2, quad3, quad4]:
            for col in quad:
                m20.pick_up_tip()
                m20.transfer(trans_vol1, col, recipient_96_plate['A1'],
                             new_tip='never', mix_before=(3, step1_mix_vol))
                m20.drop_tip()

    # Step 2
    if step2 == "True":
        # Calculate max volume per well
        max_well_vol = (quad1_cols + quad2_cols + quad3_cols +
                        quad4_cols) * trans_vol1
        source_wells = recipient_96_plate.columns()[0]

        for source in source_wells:
            p300.pick_up_tip()
            p300.transfer(max_well_vol, source, tuberack, new_tip='never',
                          mix_before=(3, max_well_vol/2))
            p300.drop_tip()
