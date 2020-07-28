from opentrons.types import Point

metadata = {
    'protocolName': 'Mass Spec Sample Prep',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.0'
}


def run(ctx):

    num_samples, p20_mount, p300_mount = get_values(  # noqa: F821
        'num_samples', 'p20_mount', 'p300_mount')
    # num_samples, p20_mount, p300_mount = 63, 'left', 'right'

    # load labware
    reagent_rack = ctx.load_labware(
        'opentrons_6_tuberack_falcon_50ml_conical', '1',
        '50ml reagent tuberack')
    slide = ctx.load_labware(
        'custom_72_other_24x330ul_24x330ul_24x330ul', '5', 'slide')
    # slide = ctx.load_labware(
    #     'biorad_96_wellplate_200ul_pcr', '5', 'slide')
    sample_racks = [ctx.load_labware(
        'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', slot,
        '1.5ml Eppendorf tuberacks for samples and antibody')
        for slot in ['9', '6', '3']]
    tiprack20 = [ctx.load_labware('opentrons_96_tiprack_20ul', '2')]
    tiprack300 = [
        ctx.load_labware('opentrons_96_tiprack_300ul', slot)
        for slot in ['7', '8', '10', '11']]
    waste = ctx.load_labware(
        'nest_1_reservoir_195ml', '4',
        'waste reservoir (calibrate to top center)').wells()[0].top()

    # load pipettes
    p20 = ctx.load_instrument(
        'p20_single_gen2', p20_mount, tip_racks=tiprack20)
    p300 = ctx.load_instrument(
        'p300_single_gen2', p300_mount, tip_racks=tiprack300)

    # define wells
    slide_wells = [
        well for col in slide.columns() for well in col[1:]][:num_samples]
    detergent_wash_buffer = reagent_rack.wells()[0].bottom(5)
    bsa_blocking_buffer = reagent_rack.wells()[1].bottom(5)
    pbs = [tube.bottom(2) for tube in reagent_rack.wells()[2:4]]
    water = [tube.bottom(2) for tube in reagent_rack.wells()[4:6]]

    samples = [
        rack.wells() for rack in sample_racks
        for well in rack.wells()][:num_samples]
    antibody = sample_racks[-1].wells()[-1]

    # calculate offset for spots
    y_offset = slide.wells()[0]._width/3/2
    ab_spot_sets = [
        [well.bottom().move(Point(y=side*y_offset)) for side in [1, -1]]
        for well in slide_wells]

    # transfer antibody to slide wells 2x
    p20.pick_up_tip()
    for set in ab_spot_sets:
        for well in set:
            p20.transfer(1.5, antibody, well, new_tip='never')

    p20.drop_tip()

    ctx.home()
    ctx.pause('Remove well module from OT-2 and incubate in humidity chamber \
overnight at 4C to allow antibodies to adhere to slide. After overnight \
incubation, remove the slide from the humidity chamber and place in \
desiccator to dry. Once dry, place slide with attached well module back into \
OT-2')

    def add_reagent(vol, source, drop=True):
        p300.pick_up_tip()
        for well in slide_wells:
            p300.transfer(vol, source, well.top(), air_gap=20, new_tip='never')
        if drop:
            p300.drop_tip()

    def discard_liquid(vol, new_tip=False):
        if not p300.hw_pipette['has_tip']:
            p300.pick_up_tip()
        for well in slide_wells:
            if new_tip and not p300.hw_pipette['has_tip']:
                p300.pick_up_tip()
            p300.transfer(
                vol, well.bottom(0.2), waste, air_gap=20, new_tip='never')
            if new_tip:
                p300.drop_tip()
        if p300.hw_pipette['has_tip']:
            p300.drop_tip()

    def wash(vol, source):
        add_reagent(vol, source)
        discard_liquid(vol)

    wash(250, detergent_wash_buffer)

    add_reagent(250, bsa_blocking_buffer)

    ctx.home()
    ctx.pause('Remove slide from OT-2 and place on benchtop shaker to \
incubate in humidity chamber for 1 hour at room temperature')

    for _ in range(2):
        wash(250, pbs[0])

    wash(250, water[0])

    ctx.home()
    ctx.pause('Remove slide from OT-2 and desiccate dry. Prepare serum \
samples in Eppendorf tubes')

    # add samples
    for s, d in zip(samples, slide_wells):
        p300.pick_up_tip()
        p300.transfer(100, s, d.top(-1), air_gap=20, new_tip='never')
        p300.drop_tip()

    ctx.home()
    ctx.pause('Remove slide from OT-2 and incubate on benchtop shaker in \
humidity box for 2 hours at room temperature')

    discard_liquid(100, new_tip=True)

    for _ in range(2):
        wash(250, pbs[1])

    for _ in range(2):
        wash(250, water[1])
