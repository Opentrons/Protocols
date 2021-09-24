import math

metadata = {
    'protocolName': 'Verogen ForenSeq DNA Signature Prep Kit Part 5/5: \
Pooling',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.10'
}


def run(ctx):

    [num_samples, m20_mount, sample_vol] = get_values(  # noqa: F821
     'num_samples', 'm20_mount', 'sample_vol')

    # load labware
    tips20m = [ctx.load_labware('opentrons_96_tiprack_20ul', '3')]
    pcr_plate = ctx.load_labware('amplifyt_96_wellplate_200ul', '6',
                                 'library plate')
    pool_strip = ctx.load_labware(
        'opentrons_96_aluminumblock_generic_pcr_strip_200ul', '9',
        'pool strip (column 1)').wells()[0]

    # load pipette
    m20 = ctx.load_instrument('p20_multi_gen2', m20_mount, tip_racks=tips20m)

    num_cols = math.ceil(num_samples/8)
    samples = pcr_plate.rows()[0][:num_cols]

    # transfer indices
    for source in samples:
        m20.transfer(sample_vol, source, pool_strip)
