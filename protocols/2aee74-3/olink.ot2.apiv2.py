import math

metadata = {
    'protocolName': 'Olink Target 96 Part 3/3: Detection',
    'author': 'Nick <ndiehl@opentrons.com>',
    'description': 'Custom Protocol Request',
    'apiLevel': '2.11'
}


def run(ctx):

    num_samples, p300_mount, m20_mount = get_values(  # noqa: F821
        'num_samples', 'p300_mount', 'm20_mount')

    if not 1 <= num_samples <= 96:
        raise Exception('Invalid number of samples (1-96)')

    det_mix = ctx.load_labware('opentrons_24_tuberack_nest_1.5ml_screwcap',
                               '7',
                               'tuberack for detection mix (A1)').wells()[0]
    inc_plate = ctx.load_labware('generic_96_aluminumblock_350ul', '5',
                                 'incubation plate')
    sample_plate = ctx.load_labware('nest_96_wellplate_100ul_pcr_full_skirt',
                                    '1', 'sample plate')
    strip = ctx.load_labware('genericstrips_96_wellplate_200ul', '4',
                             'strip for distribution (column 1)').columns()[0]
    primer_plate = ctx.load_labware('nest_96_wellplate_100ul_pcr_full_skirt',
                                    '3', 'primer plate')
    fluidigm = ctx.load_labware('fluidigm_192_wellplate_96x10ul_96x10ul', '2',
                                'Fluidigm 96.96 Dynamic Array')
    tipracks300 = [ctx.load_labware('opentrons_96_tiprack_300ul', '10')]
    tipracks20 = [ctx.load_labware('opentrons_96_tiprack_20ul', slot)
                  for slot in ['6', '8', '9', '11']]

    p300 = ctx.load_instrument('p300_single_gen2', p300_mount,
                               tip_racks=tipracks300)
    m20 = ctx.load_instrument('p20_multi_gen2', m20_mount,
                              tip_racks=tipracks20)

    p300.default_speed = 100
    m20.default_speed = 100

    num_cols = math.ceil(num_samples/8)

    ctx.comment('Prepare and prime a 96.96 Dynamic ArrayTM Integrated Fluidic \
Circuit (IFC) according to the manufacturer’s instructions. Briefly, inject \
one control line fluid syringe into each accumulator on the chip, and then \
prime the chip on the IFC Controller for approximately 20 minutes.')
    ctx.comment('Thaw the Primer Plate, vortex and spin briefly.')

    # transfer incubation mix to strip with reverse pipetting
    p300.pick_up_tip()
    p300.aspirate(20, det_mix)
    for well in strip:
        p300.aspirate(95, det_mix)
        p300.dispense(95, well)
    p300.dispense(p300.current_volume, det_mix)
    p300.drop_tip()

    # transfer from strip to plate
    m20.pick_up_tip()
    m20.aspirate(2, strip[0])
    for col in sample_plate.rows()[0][:num_cols]:
        m20.aspirate(7.2, strip[0])
        m20.dispense(7.2, col)
    m20.dispense(m20.current_volume, strip[0])
    m20.drop_tip()

    ctx.comment('Remove the Incubation Plate from the thermal cycler, spin \
down the content. Place on slot 5.')

    # transfer samples
    for s, d in zip(inc_plate.rows()[0][:num_cols],
                    sample_plate.rows()[0][:num_cols]):
        m20.pick_up_tip()
        m20.transfer(2.8, s, d, new_tip='never')
        m20.drop_tip()

    ctx.comment('Seal the plate with an adhesive plastic film, vortex and spin \
at 400 x g, 1 min at room temperature.')

    # transfer primer and sample to fluidigm plate
    sample_destinations = [
        well for row in fluidigm.rows()[:2] for well in row[:6]]
    primer_destinations = [
        well for col in fluidigm.rows()[:2] for well in col[6:]]

    for source, dest in zip(
            primer_plate.rows()[0] + sample_plate.rows()[0][:num_cols],
            primer_destinations + sample_destinations[:num_cols]):
        m20.pick_up_tip()
        m20.aspirate(7, source)
        m20.dispense(5, dest.top(-1))
        m20.dispense(m20.current_volume, source)
        m20.drop_tip()
