import math

metadata = {
    'protocolName': 'Verogen ForenSeq DNA Signature Prep Kit Part 2/5: \
PCR2 Setup',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.10'
}


def run(ctx):

    [num_samples, m20_mount, m300_mount, index_vol,
     pcr2_buffer_vol] = get_values(  # noqa: F821
        'num_samples', 'm20_mount', 'm300_mount', 'index_vol',
        'pcr2_buffer_vol')
    # num_samples = 96
    # m20_mount = 'left'
    # m300_mount = 'right'
    # index_vol = 8.0
    # pcr2_buffer_vol = 27.0

    # load labware
    pcr2_buffer = ctx.load_labware('abgenemidi_96_wellplate_800ul', '10',
                                   'PCR2 buffer tubes\
 (strip column 1)').rows()[0][:2]
    pcr_plate = ctx.load_labware('amplifyt_96_wellplate_200ul', '11',
                                 'pcr plate')
    index_plate = ctx.load_labware('amplifyt_96_wellplate_200ul', '8',
                                   'index plate')
    tips20m = [ctx.load_labware('opentrons_96_filtertiprack_20ul', '1')]
    tips300m = [ctx.load_labware('opentrons_96_filtertiprack_200ul', '5')]

    # load pipette
    if m300_mount == m20_mount:
        raise Exception('Pipette mounts cannot match.')
    m20 = ctx.load_instrument('p20_multi_gen2', m20_mount, tip_racks=tips20m)
    m300 = ctx.load_instrument('p300_multi_gen2', m300_mount,
                               tip_racks=tips300m)

    m300.default_speed = 200
    m20.default_speed = 200

    num_cols = math.ceil(num_samples/8)
    indices = index_plate.rows()[0][:num_cols]
    samples = pcr_plate.rows()[0][:num_cols]

    # transfer indices
    for source, dest in zip(indices, samples):
        m20.transfer(index_vol, source, dest)

    # transfer buffer
    for i, dest in enumerate(samples):
        m300.transfer(pcr2_buffer_vol, pcr2_buffer[i//6], dest,
                      mix_after=(10, pcr2_buffer_vol))
