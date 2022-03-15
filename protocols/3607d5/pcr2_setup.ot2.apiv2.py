import math

metadata = {
    'protocolName': 'PCR2 Setup',
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
    pcr2_buffer = ctx.load_labware('abgenemidi_96_wellplate_800ul', '1',
                                   'PCR2 buffer tube').wells()[0]
    pcr_plate = ctx.load_labware('eppendorfmetaladapter_96_wellplate_200ul',
                                 '5', 'PCR Plate')
    index_rack = ctx.load_labware('sarstedt_24_tuberack_500ul', '8',
                                  'UDI Tubes')
    tips20m = [ctx.load_labware('opentrons_96_filtertiprack_20ul', '7')]

    # load pipette
    if m300_mount == m20_mount:
        raise Exception('Pipette mounts cannot match.')
    m20 = ctx.load_instrument('p20_multi_gen2', m20_mount, tip_racks=tips20m)

    m20.default_speed = 200

    def _pick_up_single(pip):
        tips_ordered = [
            well for rack in pip.tip_racks[::-1]
            for col in rack.columns()[::-1]
            for well in col[::-1]]
        for tip_well in tips_ordered:
            if tip_well.has_tip:
                pip.pick_up_tip(tip_well)
                return

    num_cols = math.ceil(num_samples/6)
    indices = index_rack.rows()[0]
    sample_columns = [col[:6] for col in pcr_plate.columns()[:num_cols]]
    all_samples = [well for col in sample_columns for well in col]

    # transfer indices
    ctx.max_speeds['Z'] = 40
    ctx.max_speeds['A'] = 40
    for col in sample_columns:
        for source, dest in zip(indices, col):
            _pick_up_single(m20)
            m20.aspirate(index_vol, source)
            m20.dispense(index_vol, dest)
            m20.drop_tip()

    # transfer buffer
    for dest in all_samples:
        _pick_up_single(m20)
        m20.aspirate(pcr2_buffer_vol, pcr2_buffer)
        m20.dispense(pcr2_buffer_vol, dest)
        m20.mix(10, pcr2_buffer_vol, dest)
        m20.drop_tip()
