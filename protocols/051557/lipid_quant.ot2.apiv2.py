from opentrons.types import Point, Mount

metatata = {
    'protocolName': 'Lipid Quantification',
    'author': 'Nick Diehl <ndiehl@opentrons.com>',
    'apiLevel': '2.14'
}


def run(ctx):

    [num_samples] = get_values(  # noqa: F821
        'num_samples')

    plate = ctx.load_labware('abgene_96_wellplate_2200ul', '4')
    tubeblock = ctx.load_labware(
        'opentrons_24_aluminumblock_nest_1.5ml_snapcap', '5')
    reservoir30 = ctx.load_labware('eppendorf_7_reservoir_30000ul', '7')
    reservoir100 = ctx.load_labware('eppendorf_7_reservoir_100000ul', '8')
    tiprack20 = [ctx.load_labware('opentrons_96_tiprack_20ul', '9')]
    tiprack300 = [ctx.load_labware('opentrons_96_tiprack_300ul', '6')]

    sample_columns = plate.columns()[3:6]
    triton_x100 = reservoir30.wells()[0]
    triglyceride = reservoir100.wells()[0]

    standards = tubeblock.wells()[:5]
    standard_dest_sets = [
        row[:3] for row in plate.rows()[1:6]]

    ctx.pause('Remove silicon from plate.')

    single_counts = {m20: 0, m300: 0}

    def pick_up_single(pip=m20):
        tip = [
            well for col in pip.tip_racks[-1].columns()[::-1]
            for well in col[::-1]][single_counts[pip]]
        if not ctx.is_simulating():
            ctx._hw_manager