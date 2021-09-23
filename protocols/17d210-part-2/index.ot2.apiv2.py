import math

metadata = {
    'protocolName': 'Verogen ForenSeq DNA Signature Prep Kit Part 2/5: \
Indexing',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.10'
}


def run(ctx):

    [num_samples, m20_mount, m300_mount, index_vol,
     pcr2_buffer_vol] = get_values(  # noqa: F821
        'num_samples', 'm20_mount', 'm300_mount', 'index_vol',
        'pcr2_buffer_vol')

    # load labware
    pcr2_buffer = ctx.load_labware('abgenemidi_96_wellplate_800ul', '10',
                                   'PCR2 buffer tubes\
 (strip column 1)').wells()[0]
    pcr_plate = ctx.load_labware('amplifyt_96_wellplate_200ul', '11',
                                 'pcr plate')
    index_plate = ctx.load_labware('amplifyt_96_wellplate_200ul', '8',
                                   'index plate')
    tips20m = [ctx.load_labware('opentrons_96_tiprack_20ul', '1')]
    tips300m = [ctx.load_labware('opentrons_96_tiprack_300ul', '5')]

    # load pipette
    if m300_mount == m20_mount:
        raise Exception('Pipette mounts cannot match.')
    m20 = ctx.load_instrument('p20_multi_gen2', m20_mount, tip_racks=tips20m)
    m300 = ctx.load_instrument('p300_multi_gen2', m300_mount,
                               tip_racks=tips300m)

    num_cols = math.ceil(num_samples/8)
    indices = index_plate.rows()[0][:num_cols]
    samples = pcr_plate.rows()[0][:num_cols]

    # transfer indices
    for source, dest in zip(indices, samples):
        m20.transfer(index_vol, source, dest)

    # transfer buffer
    for dest in samples:
        m300.transfer(pcr2_buffer_vol, pcr2_buffer, dest,
                      mix_after=(10, pcr2_buffer_vol))
