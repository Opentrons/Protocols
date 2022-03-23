import math

metadata = {
    'protocolName': 'PCR Prep',
    'author': 'Nick <ndiehl@opentrons.com>',
    'description': 'Custom Protocol Request',
    'apiLevel': '2.10'
}


def run(ctx):

    [num_samples, num_primers, res_type, tip_type,
     p20_multi_mount, height_dispense] = get_values(  # noqa: F821
     'num_samples', 'num_primers', 'res_type', 'tip_type', 'p20_multi_mount',
     'height_dispense')

    # labware
    pcr_plate = ctx.load_labware('thermofishermicroamp_96_aluminumblock_200ul',
                                 '1', 'destination PCR plate')
    sample_plate = ctx.load_labware(
        'thermofishermicroamp_96_aluminumblock_200ul', '4',
        'source sample plate')
    res = ctx.load_labware(res_type, '5', 'reagent reservoir')
    tipracks20m = [
        ctx.load_labware('opentrons_96_tiprack_20ul', slot)
        for slot in ['6', '8', '9']]

    # pipettes
    m20 = ctx.load_instrument('p20_multi_gen2', p20_multi_mount,
                              tip_racks=tipracks20m)

    # check
    num_cols = math.ceil(num_samples/8)
    if num_cols*num_primers > 12:
        raise Exception(f'Can only accommodate up to {math.floor(12/num_cols)} \
primers with {num_samples} samples or {math.floor(12/num_primers)} samples \
with {num_primers} primers.')

    # reagents
    sample_sources = sample_plate.rows()[0][:num_cols]
    sample_dests_sets_m = [
        [pcr_plate.rows()[0][p*num_cols+s] for p in range(num_primers)]
        for s in range(num_cols)]
    primer_sources = res.wells()[:num_primers]
    primer_dest_sets = [
        pcr_plate.rows()[0][p*num_cols:(p+1)*num_cols]
        for p in range(num_primers)]

    # transfer primers, BigDye + water mix
    for primer, dest_set in zip(primer_sources, primer_dest_sets):
        m20.pick_up_tip()
        for d in dest_set:
            m20.transfer(17, primer, d.bottom(height_dispense),
                         new_tip='never')
        m20.drop_tip()

    # transfer samples
    for s, d_set in zip(sample_sources, sample_dests_sets_m):
        for d in d_set:
            m20.pick_up_tip()
            m20.transfer(3, s, d.bottom(height_dispense), new_tip='never')
            m20.drop_tip()
