metadata = {
    'protocolName': '384 Well Plate PCR Plate with Triplicates',
    'author': 'Rami Farawi <rami.farawi@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.8'
}
def get_values(*names):
    import json
    _all_values = json.loads("""{"num_gene":5,"num_mastermix":24,"p20_mount":"left"}""")
    return [_all_values[n] for n in names]

def run(ctx):

    [num_gene, num_mastermix, p20_mount] = get_values(  # noqa: F821
        "num_gene", "num_mastermix", "p20_mount")

    if not 1 <= num_mastermix <= 24:
        raise Exception("Enter a number of mastermixes between 1-24")
    if not 1 <= num_gene <= 5:
        raise Exception("Enter a number of cDNA 1-5")

    # load labware
    plate = ctx.load_labware('100ul_384_wellplate_100ul', '1')
    mastermix = ctx.load_labware(
                'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', '2')
    cDNA = ctx.load_labware(
                'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', '3')
    tiprack = [ctx.load_labware('thermofisherart_96_tiprack_10ul', '4')]

    # load instrument
    p20 = ctx.load_instrument('p20_single_gen2',
                              p20_mount, tip_racks=tiprack)

    # ctx
    cDNA_tubes = cDNA.rows()[0][:num_gene]
    well_map = [[well for col in plate.columns()[:num_mastermix]
                for well in col[i:i+3]] for i in range(0, num_gene*3, 3)]
    airgap = 5
    for tube, chunk in zip(cDNA_tubes, well_map):
        p20.pick_up_tip()
        for well in chunk:
            p20.aspirate(4, tube)
            p20.air_gap(airgap)
            p20.dispense(4, well)
            p20.blow_out()
        ctx.comment('\n')
        p20.drop_tip()

    for tube, column in zip(mastermix.wells(),
                            plate.columns()[:num_mastermix]):
        p20.pick_up_tip()
        for i, well in enumerate(column[:num_gene*3]):
            p20.transfer(16, tube, well.top(), new_tip='never')
            p20.blow_out()
        p20.drop_tip()
