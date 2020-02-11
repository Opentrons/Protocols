import math
import json

metadata = {
    'protocolName': 'Zymo-Seq RiboFree™ Total RNA Library Prep First-Strand \
cDNA Synthesis and RiboFreeTM Universal Depletion (robot 1)',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.0'
}


def run(ctx):

    [number_of_samples, starting_vol, rna_input, p20_mount,
        p50_mount] = get_values(  # noqa: F821
            'number_of_samples', 'starting_vol', 'rna_input', 'p20_mount',
            'p50_mount')
    # [number_of_samples, starting_vol, rna_input, p20_mount, p50_mount] = [
    #     96, 5, '> 1µg', 'right', 'left']

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
    racks20 = [
        ctx.load_labware('opentrons_96_tiprack_20ul', slot)
        for slot in ['3', '4', '5', '6']
    ]
    racks50 = [ctx.load_labware('opentrons_96_tiprack_300ul', '9')]

    # pipettes
    if p20_mount == p50_mount:
        raise Exception('Pipette mounts cannot match.')
    p20 = ctx.load_instrument('p20_single_gen2', p20_mount, tip_racks=racks20)
    m50 = ctx.load_instrument('p50_multi', p50_mount, tip_racks=racks50)

    # reagents and sample setup
    if number_of_samples > 96 or number_of_samples < 1:
        raise Exception('Invalid number of samples (must be 1-96).')
    samples = tc_plate.wells()[:number_of_samples]
    samples_multi = tc_plate.rows()[0][:math.ceil(number_of_samples/8)]
    r1, r2, h2o = tempblock.rows()[0][:3]
    d1, d2, d3 = tempblock.rows()[1][:3]
    etoh = reagent_res.wells()[0]

    tip20_count = 0
    tip20_max = len(racks20*96)

    def pick_up():
        nonlocal tip20_count
        if tip20_count == tip20_max:
            ctx.pause('Replace 20µl tipracks in slots 3 and 4 before \
resuming.')
            p20.reset_tipracks()
            tip20_count = 0
        tip20_count += 1
        p20.pick_up_tip()

    """ Section 1.1: First-Strand cDNA Synthesis (Yellow Caps) """
    if tc.lid_position == 'closed':
        tc.open_lid()

    # bring samples up to 8µl with H2O if necessary
    vol_h2o = 9 - starting_vol if rna_input != '< 100ng' else 8 - starting_vol
    for s in samples:
        pick_up()
        p20.transfer(vol_h2o, h2o, s, new_tip='never')
        p20.blow_out(s.top(-2))
        p20.drop_tip()

    # transfer R1
    vol_r1 = 1 if rna_input != '< 100ng' else 2
    for s in samples:
        pick_up()
        p20.transfer(vol_r1, r1, s, mix_after=(3, 5), new_tip='never')
        p20.blow_out(s.top(-2))
        p20.drop_tip()
    ctx.pause('Briefly spin down plate before resuming.')

    # execute primer annealing
    profile_1_1 = [
        {'temperature': 98, 'hold_time_minutes': 3},
        {'temperature': 4, 'hold_time_seconds': 10}
    ]
    tc.close_lid()
    tc.execute_profile(steps=profile_1_1, repetitions=1, block_max_volume=10)
    tc.open_lid()

    # transfer R2
    for s in samples:
        pick_up()
        p20.transfer(10, r2, s, mix_after=(3, 15), new_tip='never')
        p20.blow_out(s.top(-2))
        p20.drop_tip()

    # execute reverse transcription
    profile_1_2 = [
        {'temperature': 25, 'hold_time_minutes': 5},
        {'temperature': 48, 'hold_time_minutes': 15},
        {'temperature': 4, 'hold_time_seconds': 10}
    ]
    tc.close_lid()
    tc.execute_profile(steps=profile_1_2, repetitions=1, block_max_volume=20)
    tc.open_lid()

    """ Section 1.2: RiboFreeTM Universal Depletion (Red Caps) """

    # transfer D1
    for s in samples:
        pick_up()
        p20.transfer(10, d1, s, mix_after=(3, 15), new_tip='never')
        p20.blow_out(s.top(-2))
        p20.drop_tip()
    ctx.pause('Briefly spin down plate before resuming.')

    # execute pre-depletion incubation
    profile_1_3 = [
        {'temperature': 98, 'hold_time_minutes': 3},
        {'temperature': 68, 'hold_time_minutes': 5}
    ]
    tc.close_lid()
    tc.execute_profile(steps=profile_1_3, repetitions=1, block_max_volume=30)
    tc.open_lid()

    # transfer D2
    for s in samples:
        pick_up()
        p20.transfer(10, d2, s, mix_after=(3, 15), new_tip='never')
        p20.blow_out(s.top(-2))
        p20.drop_tip()

    # exeute depletion reaction
    if rna_input == '> 1µg':
        inc_time = 30
    elif rna_input == '250ng-1µg':
        inc_time = 60
    else:
        inc_time = 120
    profile_1_4 = [
        {'temperature': 68, 'hold_time_minutes': inc_time}
    ]
    tc.close_lid()
    tc.execute_profile(steps=profile_1_4, repetitions=1, block_max_volume=40)
    tc.open_lid()

    # transfer D3
    for s in samples:
        pick_up()
        p20.transfer(10, d3, s, mix_after=(3, 15), new_tip='never')
        p20.blow_out(s.top(-2))
        p20.drop_tip()

    # execute stop depletion
    profile_1_5 = [
        {'temperature': 98, 'hold_time_minutes': 2},
        {'temperature': 25, 'hold_time_seconds': 10}
    ]
    tc.close_lid()
    tc.execute_profile(steps=profile_1_5, repetitions=1, block_max_volume=50)
    tc.open_lid()

    # transfer EtOH
    for m in samples_multi:
        m50.pick_up_tip()
        m50.transfer(
            25, etoh, m, mix_after=(5, 40), air_gap=10, new_tip='never')
        m50.blow_out(m.top(-2))
        m50.air_gap(10)
        m50.drop_tip()

    ctx.comment('Carefully remove sample plate from thermocycler and proceed \
with cleanup.')

    # track final used tip
    if not ctx.is_simulating():
        file_path = '/data/csv/tip_track.json'
        # file_path = '/protocols/tip_track.json'
        data = {
            'tips20': tip20_count
        }
        with open(file_path, 'w') as outfile:
            json.dump(data, outfile)
