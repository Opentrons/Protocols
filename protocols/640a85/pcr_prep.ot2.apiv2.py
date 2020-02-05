# metadata
metadata = {
    'protocolName': 'PCR Prepation',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.0'
}


def run(ctx):

    [number_of_samples, pcr_type, p300_multi_mount,
        p20_single_mount] = get_values(  # noqa: F821
            'number_of_samples', 'pcr_type', 'p300_multi_mount',
            'p20_single_mount')

    # checks
    if p300_multi_mount == p20_single_mount:
        raise Exception('Pipette mounts cannot match.')
    if number_of_samples < 1 or number_of_samples > 32:
        raise Exception('Invalid number of DNA samples (must be 1-32).')

    # load labware
    tc = ctx.load_module('thermocycler')
    tc.open_lid()
    plate = tc.load_labware(pcr_type)
    tips300 = [
        ctx.load_labware('opentrons_96_tiprack_300ul', '1', '300ul tips')]
    tips20 = [
        ctx.load_labware('opentrons_96_tiprack_20ul', '2', '20ul tips')]
    tuberacks = [
        ctx.load_labware(
            'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
            slot,
            'DNA tuberack ' + str(i+1)
        )
        for i, slot in enumerate(['4', '5'])
    ]
    mm = ctx.load_labware(
        'nest_12_reservoir_15ml', '6', 'reservoir for mastermix').wells()[0]

    # pipettes
    m300 = ctx.load_instrument(
        'p300_multi', p300_multi_mount, tip_racks=tips300)
    p20 = ctx.load_instrument(
        'p20_single_gen2', p20_single_mount, tip_racks=tips20)

    # sample setup
    dna_sources = [
        tube
        for rack in tuberacks
        for tube in rack.wells()][:number_of_samples][:number_of_samples]
    mm_dests = plate.rows()[0]
    trip_dests = [
        row[i*3:i*3+3]
        for row in plate.rows() for i in range(4)][:number_of_samples]

    # distribute mastermix
    m300.pick_up_tip()
    for d in mm_dests:
        m300.transfer(24, mm, d.bottom(3), air_gap=10, new_tip='never')
        m300.blow_out(d.top(-2))
    m300.drop_tip()

    # transfer samples in triplicate
    for s, d_set in zip(dna_sources, trip_dests):
        p20.pick_up_tip()
        for d in d_set:
            p20.aspirate(1, s.bottom(2))
            p20.air_gap(2)
            p20.touch_tip(s, v_offset=-3)
            p20.dispense(2, d.top(-2))
            p20.aspirate(9, d.bottom(2))
            p20.dispense(10, d.bottom(2))
            p20.blow_out(d.top(-2))
            p20.touch_tip(d, v_offset=-3)
        p20.drop_tip()

    # setup and execute thermocylcer profile
    tc.close_lid()
    tc.set_lid_temperature(105)
    profile1 = [{'temperature': 95, 'hold_time_minutes': 10}]
    profiles2 = [
        [
            {'temperature': 96, 'hold_time_seconds': 10},
            {'temperature': temp, 'hold_time_seconds': 30},
            {'temperature': 68, 'hold_time_seconds': 60}
        ] for temp in range(62, 46, -1)
    ]
    profile3 = [
        {'temperature': 96, 'hold_time_seconds': 10},
        {'temperature': 46, 'hold_time_seconds': 30},
        {'temperature': 68, 'hold_time_seconds': 60}
    ]
    profile4 = [
        {'temperature': 72, 'hold_time_minutes': 10},
        {'temperature': 4, 'hold_time_seconds': 10}
    ]
    tc.execute_profile(steps=profile1, repetitions=1, block_max_volume=25)
    for prof in profiles2:
        tc.execute_profile(
            steps=prof, repetitions=1, block_max_volume=25)
    tc.execute_profile(steps=profile3, repetitions=25, block_max_volume=25)
    tc.execute_profile(steps=profile4, repetitions=1, block_max_volume=25)
