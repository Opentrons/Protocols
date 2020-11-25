metadata = {'apiLevel': '2.0'}

def run(ctx):

    column_count = 12

    p20m = ctx.load_instrument('p20_multi_gen2', 'right', tip_racks=[ctx.load_labware("opentrons_96_filtertiprack_20ul", x) for x in ["1","2"]])
    p1000s = ctx.load_instrument('p1000_single_gen2', 'left', tip_racks=[])

    rna = ctx.load_labware("opentrons_96_aluminumblock_biorad_wellplate_200ul","4")
    cdna = ctx.load_labware("opentrons_96_aluminumblock_biorad_wellplate_200ul","5")

    for source_well, target_well in zip(rna.rows()[0][:column_count], cdna.rows()[0][:column_count]):
        p20m.transfer(6.2, source_well, target_well)
