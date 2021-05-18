metadata = {
    'protocolName': 'Temperature Controlled PCR Prep With Tube Strips',
    'author': 'Rami Farawi <rami.farawi@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.7'
}


def run(ctx):

    [num_col, asp_delay, p20_mount, m20_mount] = get_values(  # noqa: F821
        "num_col", "asp_delay", "p20_mount", "m20_mount")

    if not 1 <= num_col <= 12:
        raise Exception("Enter a column number between 1-12")

    # load labware
    temp_mod = ctx.load_module('temperature module gen2', '1')
    sample_plate = temp_mod.load_labware('biorad_96_wellplate_200ul_pcr')
    tip_rack = [ctx.load_labware('opentrons_96_filtertiprack_20ul', slot)
                for slot in ['3', '6']]
    saliva = [ctx.load_labware(
            'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', slot)
            for slot in ['2', '5', '8', '11']]
    reagent_plate = ctx.load_labware('biorad_96_wellplate_200ul_pcr', '4')

    # load instrument
    p20 = ctx.load_instrument('p20_single_gen2', p20_mount, tip_racks=tip_rack)
    m20 = ctx.load_instrument('p20_multi_gen2', m20_mount, tip_racks=tip_rack)

    # reagents, setup
    temp_mod.set_temperature(4)
    mastermix = reagent_plate.rows()[0][:2]
    tubes = [tube for tuberack in saliva for tube in tuberack.wells()]

    # add mastermix
    m20.pick_up_tip()
    for i, col in enumerate(sample_plate.rows()[0][:num_col]):
        m20.aspirate(15, mastermix[0] if i < 6 else mastermix[1])
        m20.dispense(15, col)
    m20.drop_tip()

    # add saliva
    airgap = 5
    for s, d in zip(tubes[:num_col*8], sample_plate.wells()):
        p20.pick_up_tip()
        p20.aspirate(5, s)
        p20.air_gap(airgap)
        ctx.delay(seconds=asp_delay)
        p20.dispense(5+airgap, d)
        p20.mix(3, 18, d)
        p20.blow_out()
        p20.drop_tip()
