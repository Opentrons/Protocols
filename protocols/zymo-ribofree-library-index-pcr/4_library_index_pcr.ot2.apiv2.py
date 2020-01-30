import math

metadata = {
    'protocolName': 'Zymo-Seq RiboFree™ Total RNA Library Prep Library Index \
PCR (robot 1)',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.0'
}


def run(ctx):

    [number_of_samples, rna_input, p20_mount,
        p50_mount] = get_values(  # noqa: F821
            'number_of_samples', 'rna_input', 'p20_mount', 'p50_mount')
    # [number_of_samples, rna_input, p20_mount, p50_mount] = [
    #     96, '> 1µg', 'right', 'left']

    # load modules and labware
    tempdeck = ctx.load_module('tempdeck', '1')
    tempdeck.set_temperature(4)
    tempblock = tempdeck.load_labware(
        'opentrons_24_aluminumblock_nest_1.5ml_screwcap')
    tc = ctx.load_module('thermocycler')
    tc.set_lid_temperature(100)
    tc.set_block_temperature(4)
    tc_plate = tc.load_labware('nest_96_wellplate_100ul_pcr_full_skirt')
    reagent_res = ctx.load_labware(
        'nest_12_reservoir_15ml', '2', 'reagent reservoir')
    dna_eb = reagent_res.wells()[1]
    racks20 = [
        ctx.load_labware('opentrons_96_tiprack_20ul', slot)
        for slot in ['3']
    ]
    index_plate = ctx.load_labware(
        'nest_96_wellplate_100ul_pcr_full_skirt', '4', 'UDI primer plate')
    racks50 = [
        ctx.load_labware('opentrons_96_tiprack_300ul', slot)
        for slot in ['6', '9']
    ]

    # pipettes
    if p20_mount == p50_mount:
        raise Exception('Pipette mounts cannot match.')
    p20 = ctx.load_instrument('p20_single_gen2', p20_mount, tip_racks=racks20)
    m50 = ctx.load_instrument('p50_multi', p50_mount, tip_racks=racks50)

    # reagents and sample setup
    if number_of_samples > 96 or number_of_samples < 1:
        raise Exception('Invalid number of samples (must be 1-96).')
    samples = tc_plate.wells()[:number_of_samples]
    udi_primers = index_plate.rows()[0][:math.ceil(number_of_samples/8)]
    samples_multi = tc_plate.rows()[0][:math.ceil(number_of_samples/8)]
    taq_premix = tempblock.rows()[3][0]

    """ Section 2.3: Library Index PCR (Green Caps) """
    if tc.lid_position == 'closed':
        tc.open_lid()

    # transfer UDI primers
    for m in samples_multi:
        m50.pick_up_tip()
        m50.transfer(
            5, udi_primers, m, mix_after=(3, 15), air_gap=5, new_tip='never')
        m50.blow_out(m.top(-2))
        m50.drop_tip()

    # transfer taq premix
    for s in samples:
        p20.pick_up_tip()
        p20.transfer(25, taq_premix, s.top(), new_tip='never')
        p20.mix(3, 15, s)
        p20.blow_out(s.top(-2))
        p20.drop_tip()
    ctx.pause('Briefly spin down sample plate and replace on thermoycler.')

    # run first part of profile 1
    tc.close_lid()
    if rna_input == '> 1µg':
        cycles = 10
    elif rna_input == '250ng-1µg':
        cycles = 11
    elif rna_input == '100ng-250ng':
        cycles = 12
    elif rna_input == '< 100ng':
        cycles = 13
    profile_2_4 = [{'temperature': 95, 'hold_time_minutes': 10}]
    profile_2_5 = [
        {'temperature': 95, 'hold_time_seconds': 30},
        {'temperature': 60, 'hold_time_seconds': 30},
        {'temperature': 72, 'hold_time_minutes': 1}
    ]
    profile_2_6 = [
        {'temperature': 72, 'hold_time_minutes': 7},
        {'temperature': 4, 'hold_time_seconds': 10}
    ]
    tc.execute_profile(steps=profile_2_4, repetitions=1, block_max_volume=50)
    tc.execute_profile(
        steps=profile_2_5, repetitions=cycles, block_max_volume=50)
    tc.execute_profile(steps=profile_2_6, repetitions=1, block_max_volume=50)
    tc.open_lid()

    # transfer elution buffer
    for m in samples_multi:
        m50.pick_up_tip()
        m50.transfer(50, dna_eb, m, new_tip='never')
        m50.mix(5, 40, s)
        m50.blow_out(m.top(-2))
        m50.drop_tip()

    ctx.comment('Carefully remove sample plate from thermocycler and proceed \
with cleanup.')
