import math
import json
import os

metadata = {
    'protocolName': 'Zymo-Seq RiboFree™ Total RNA Library Prep P5 Adapter \
Ligation (robot 1)',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.0'
}


def run(ctx):

    [number_of_samples, p20_mount, p50_mount] = get_values(  # noqa: F821
            'number_of_samples', 'p20_mount', 'p50_mount')
    # [number_of_samples, p20_mount, p50_mount] = [96, 'right', 'left']

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
    p20.flow_rate.aspirate = 10
    p20.flow_rate.dispense = 20
    m50 = ctx.load_instrument('p50_multi', p50_mount, tip_racks=racks50)

    file_path = '/data/csv/tip_track.json'
    # file_path = 'protocols/tip_track.json'
    if os.path.isfile(file_path):
        with open(file_path) as json_file:
            data = json.load(json_file)
            if 'tips20' in data:
                tip20_count = data['tips20']
            else:
                tip20_count = 0
            if 'tips50' in data:
                tip50_count = data['tips50']
            else:
                tip50_count = 0
    else:
        tip20_count = 0
        tip50_count = 0

    all_tips20 = [tip for rack in racks20 for tip in rack.wells()]
    all_tips50 = [tip for rack in racks50 for tip in rack.rows()[0]]
    tip20_max = len(all_tips20)
    tip50_max = len(all_tips50)

    def pick_up(pip):
        nonlocal tip20_count
        nonlocal tip50_count
        if pip == p20:
            if tip20_count == tip20_max:
                ctx.pause('Replace tipracks before resuming.')
                tip20_count = 0
                [rack.reset() for rack in racks20]
            pip.pick_up_tip(all_tips20[tip20_count])
            tip20_count += 1
        else:
            if tip50_count == tip50_max:
                ctx.pause('Replace tipracks before resuming.')
                tip50_count = 0
                [rack.reset() for rack in racks50]
            pip.pick_up_tip(all_tips50[tip50_count])
            tip50_count += 1

    # reagents and sample setup
    if number_of_samples > 96 or number_of_samples < 1:
        raise Exception('Invalid number of samples (must be 1-96).')
    samples = tc_plate.wells()[:number_of_samples]
    samples_multi = tc_plate.rows()[0][:math.ceil(number_of_samples/8)]
    l3 = tempblock.rows()[2][2]
    dna_eb = reagent_res.wells()[1]

    """ Section 2.2: P5 Adapter Ligation (Green Caps) """
    if tc.lid_position == 'closed':
        tc.open_lid()

    # transfer L3
    for s in samples:
        pick_up(p20)
        p20.transfer(10, l3, s, mix_after=(3, 15), new_tip='never')
        p20.blow_out(s.top(-2))
        p20.drop_tip()
    ctx.pause('Briefly spin down plate before resuming.')

    # execute P5 ligation reaction
    profile_2_3 = [
        {'temperature': 25, 'hold_time_minutes': 15},
        {'temperature': 4, 'hold_time_seconds': 10}
    ]
    tc.close_lid()
    tc.execute_profile(steps=profile_2_3, repetitions=1, block_max_volume=20)
    tc.open_lid()

    # transer DNA elution buffer
    ctx.pause('Briefly spin down plate before resuming.')
    for m in samples_multi:
        pick_up(m50)
        m50.transfer(80, dna_eb, m.top(), new_tip='never', air_gap=10)
        m50.mix(5, 40, m)
        m50.blow_out(m.top(-2))
        m50.drop_tip()

    ctx.comment('Carefully remove sample plate from thermocycler and proceed \
with cleanup.')

    # track final used tip
    file_path = '/data/csv/tip_track.json'
    data = {
        'tips20': tip20_count,
        'tips50': tip50_count
    }
    with open(file_path, 'w') as outfile:
        json.dump(data, outfile)
