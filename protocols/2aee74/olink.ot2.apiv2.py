import math

metadata = {
    'protocolName': 'Olink Target 96 Part 1/3: Incubation',
    'author': 'Nick <ndiehl@opentrons.com>',
    'description': 'Custom Protocol Request',
    'apiLevel': '2.11'
}


def run(ctx):

    num_samples, p300_mount, m20_mount = get_values(  # noqa: F821
        'num_samples', 'p300_mount', 'm20_mount')

    if not 1 <= num_samples <= 96:
        raise Exception('Invalid number of samples (1-96)')

    inc_mix = ctx.load_labware('opentrons_24_tuberack_nest_1.5ml_screwcap',
                               '8',
                               'tuberack for incubation mix (A1)').wells()[0]
    inc_plate = ctx.load_labware('generic_96_aluminumblock_350ul', '10',
                                 'incubation plate')
    sample_plate = ctx.load_labware('nest_96_wellplate_100ul_pcr_full_skirt',
                                    '7', 'sample plate')
    strip = ctx.load_labware('genericstrips_96_wellplate_200ul', '11',
                             'strip for distribution (column 1)').columns()[0]
    tipracks300 = [ctx.load_labware('opentrons_96_filtertiprack_200ul', '9')]
    tipracks20 = [
        ctx.load_labware('opentrons_96_filtertiprack_20ul', slot)
        for slot in ['3', '6']]

    p300 = ctx.load_instrument('p300_single_gen2', p300_mount,
                               tip_racks=tipracks300)
    m20 = ctx.load_instrument('p20_multi_gen2', m20_mount,
                              tip_racks=tipracks20)

    p300.default_speed = 100
    m20.default_speed = 100

    num_cols = math.ceil(num_samples/8)

    # transfer incubation mix to strip with reverse pipetting
    p300.pick_up_tip()
    p300.aspirate(20, inc_mix)
    for well in strip:
        p300.aspirate(47, inc_mix)
        p300.dispense(47, well)
    p300.dispense(p300.current_volume, inc_mix)
    p300.drop_tip()

    # transfer from strip to plate
    m20.pick_up_tip()
    m20.aspirate(2, strip[0])
    for col in inc_plate.rows()[0][:num_cols]:
        m20.aspirate(3, strip[0])
        m20.dispense(3, col)
    m20.dispense(m20.current_volume, strip[0])
    m20.drop_tip()

    # transfer samples
    for s, d in zip(sample_plate.rows()[0][:num_samples],
                    inc_plate.rows()[0][:num_samples]):
        m20.pick_up_tip()
        m20.transfer(1, s, d, new_tip='never')
        m20.drop_tip()

    ctx.comment('Seal the plate with an adhesive plastic film, spin at 400 x \
g, 1 min at room temperature. Incubate overnight at +4°C.')
