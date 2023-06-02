metadata = {
    'apiLevel': '2.13'
}


def run(ctx):

    plate = ctx.load_labware('biorad_96_wellplate_200ul_pcr', '1')

    p300 = ctx.load_instrument('p300_single_gen2', 'left')