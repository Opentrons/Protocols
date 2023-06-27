metadata = {
    'protocolName': 'ELISA',
    'author': 'Nick Diehl <ndiehl@opentrons.com>',
    'apiLevel': '2.13'
}


def run(ctx):

    [num_samples] = get_values(  # noqa: F821
        'num_samples')

    # labware
    sample_plate = ctx.load_labware('thermo_96_wellplate_400ul', '5',
                                    'sample plate')
    elisa_plates = [
        ctx.load_labware('thermo_96_wellplate_400ul', slot, f'test plate {i+1}')
        for i, slot in enumerate(['1', '2', '3', '4'][:])]
    res12 = ctx.load_labware('starlab_12_reservoir_22000ul', '6')
    res1 = ctx.load_labware('starlab_1_reservoir_240000ul', '7')
    waste = ctx.load_labware(
        'starlab_1_reservoir_240000ul', '9').wells()[0].top()
    tipracks300 = [
        ctx.load_labware('opentrons_96_tiprack_300ul', slot)
        for slot in ['8', '10', '11']]

    # pipettes
    p300 = ctx.load_labware('p300_single_gen2', 'left', tip_racks=tipracks300)
    m300 = ctx.load_labware('p300_multi_gen2', 'right', tip_racks=tipracks300)

    num_cols = math.ceil(num_samples/8)
    samples_s = sample_plate.wells()[:num_samples]
    samples_m = sample_plate.rows()[:num_cols]
    all_test_plate_dests_s = [
        well for plate in elisa_plates for well in plate.wells()]
    all_test_plate_dests_m = [
        well for plate in elisa_plates for well in plate.rows()[0]]
    test_plate_dest_blocks = [
        all_test_plate_dests_s[i*48+8]
        for block in range(8)
    ]

    def slow_withdraw(pip, well, delay_seconds=1.0):
        pip.default_speed /= 10
        if delay_seconds > 0:
            ctx.delay(seconds=delay_seconds)
        pip.move_to(well.top())
        pip.default_speed *= 10

    def slow_descend(pip, well, delay_seconds=1.0, z_offset=0.2):
        pip.default_speed /= 10
        if delay_seconds > 0:
            ctx.delay(seconds=delay_seconds)
        pip.move_to(well.bottom(z_offset))
        pip.default_speed *= 10

    # liquids

    # protocol steps
    samples = []
    destination_sets = []

    ctx.pause(minutes=60, msg='Incubating for 1 hour')

    def remove_supernatant(vol, pip=m300):
        for well in test_plates