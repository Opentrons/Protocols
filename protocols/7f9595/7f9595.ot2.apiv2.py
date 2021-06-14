metadata = {
    'protocolName': 'Sample Serial Dilution (1:10)',
    'author': 'Sakib <sakib.hossain@opentrons.com>',
    'description': 'Custom Protocol Request',
    'apiLevel': '2.10'
}


def run(ctx):

    [m300_mount, reservoir_type] = get_values(  # noqa: F821
        "m300_mount", "reservoir_type")

    # Load Labware
    tiprack = ctx.load_labware('opentrons_96_tiprack_300ul', 1)
    reservoir = ctx.load_labware(reservoir_type, 2)
    plate = ctx.load_labware('corning_96_wellplate_360ul_flat', 3)

    # Load Pipettes
    m300 = ctx.load_instrument('p300_multi_gen2', m300_mount,
                               tip_racks=[tiprack])

    # Reagents
    pbs = reservoir['A1']

    # Wells
    sample_cols = plate.rows()[0]
    sample_cols1 = plate.rows()[0][:6]
    sample_cols2 = plate.rows()[0][6:12]
    pbs_cols = [plate.rows()[0][i] for i in range(12) if i not in [0, 6]]

    # Protocol Steps
    # Add 180 uL of PBS
    m300.pick_up_tip()
    for col in pbs_cols:
        m300.transfer(180, pbs, col.top(z=-5), new_tip='never')
    m300.drop_tip()

    # Dilution (Columns 1-6)
    # for i, col in enumerate(sample_cols[:5]):
    #     m300.pick_up_tip()
    #     m300.mix(6, 200, col)
    #     m300.transfer(20, col, sample_cols[i+1], mix_after=(10, 20),
    #                   new_tip='never')
    #     m300.drop_tip()

    # # Dilution (Columns 7-12)
    # for i, col in enumerate(sample_cols[6:11], 6):
    #     m300.pick_up_tip()
    #     m300.mix(6, 200, col)
    #     m300.transfer(20, col, sample_cols[i+1], mix_after=(10, 20),
    #                   new_tip='never')
    #     m300.drop_tip()

    p1 = sample_cols[:5]
    p2 = sample_cols[6:11]

    # Alternating Dilution
    for i, (col1, col2) in enumerate(zip(p1, p2)):
        m300.pick_up_tip()
        m300.mix(6, 200, col1)
        m300.transfer(20, col1, sample_cols1[i+1], mix_after=(10, 20),
                      touch_tip=True, blow_out=True,
                      blowout_location='destination well',
                      new_tip='never')
        m300.drop_tip()

        m300.pick_up_tip()
        m300.mix(6, 200, col2)
        m300.transfer(20, col2, sample_cols2[i+1], mix_after=(10, 20),
                      touch_tip=True, blow_out=True,
                      blowout_location='destination well',
                      new_tip='never')
        m300.drop_tip()
