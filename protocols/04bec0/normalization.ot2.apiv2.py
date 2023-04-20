metadata = {
    'protocolName': 'Normalization',
    'author': 'Trevor Ray <trevor.ray@opentrons.com>',
    'apiLevel': '2.14'
}


def run(ctx):

    input_csv = get_values(  # noqa: F821
    )

    sample_plate = ctx.load_labware('beckman_48_wellplate_1800ul', '7',
                                    'sample plate')
    sample_racks = [
        ctx.load_labware(
            'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
            slot, f'sample rack {i+1}')
            for i, slot in enumerate(['4', '1'])]
    normalization_racks = [
        ctx.load_labware(
            'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
            slot, f'normalization rack {i+1}')
        for i, slot in enumerate(['5', '2'])]
    final_racks = [
        ctx.load_labware(
            'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
            slot, f'final rack {i+1}')
        for i, slot in enumerate(['6', '3'])]

    tiprack1000 = [ctx.load_labware('opentrons_96_filtertiprack_1000ul', '11')]
    tiprack200 = [ctx.load_labware('opentrons_96_filtertiprack_200ul', '10')]

    p1000 = ctx.load_instrument(
        'p1000_single_gen2', 'right', tip_racks=tiprack1000)
    p300 = ctx.load_instrument(
        'p300_single_gen2', 'left', tip_racks=tiprack200)

    input_csv = """,1,2,3,4,5,6,7,8
A,None,None,None,None,None,None,None,None
B,None,None,None,None,None,None,None,None
C,80,60.72,82.79,207.23,370.24,265.78,270.34,342.88
D,70,56.65,99.74,249.64,340.56,285.08,294,366.09
E,117.17,162.28,88.7,135.69,322.46,321,285.73,375.51
F,130.01,172.35,93.48,136.36,326.26,285.79,316.29,344.37"""

    def slow_withdraw(pip, well, delay=1.0):
        pip.default_speed = 25
        pip.move_to(well.top())
        if delay > 0:
            ctx.delay(seconds=delay)
        pip.default_speed = 400

    # parse
    biomass_data = [
        [float(val) for val in line.split(',')]
        for line in input_csv.splitlines()[1:]
        if line and line.split(',')[0].strip()
    ]
    biomass_data_flat = [val for row in biomass_data for val in row]
    mask = [1 if val > 0 else 0 for val in biomass_data_flat]


    # steps 1 - 2
    vol = 800.0
    sources = sample_plate.wells()
    destinations = [
        well for rack in sample_racks for row in rack.rows() for well in row]
    p1000.flow_rate.aspirate = 100
    p1000.flow_rate.dispense = 1000
    for do, s, d in zip(mask, sources, destinations):
        if do:
            p1000.pick_up_tip()
            p1000.mix(10, 300, s.bottom(2))
            p1000.aspirate(vol, s.bottom(2))
            p1000.air_gap(100)
            slow_withdraw(p1000, s)
            p1000.dispense(p1000.current_volume, d.bottom(10.5))
            p1000.drop_tip()
            # calculation

    # steps 3-4


    target_conc = 54.0
    vol_sample_normalization = 100.0
    destinations = [
        well for rack in normalization_racks
        for row in rack.rows() for well in row]
    for do, biomass, d in zip(mask, biomass_data_flat, destionations):
        # calculation
        biomass/target - 1 * 100