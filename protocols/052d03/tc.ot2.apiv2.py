import math
from opentrons import protocol_api
from opentrons.types import Point, Mount

metadata = {
    'apiLevel': '2.13',
    'protocolName': 'Novartis Timing'
}

DO_THERMOCYCLER = True


def run(ctx):
    num_samples = 20
    cp_list = [
        f'{letter}{num}'
        for num in [3, 6, 9]
        for letter in 'ABCDEFGH'
    ]

    num_cols = math.ceil(num_samples/8)
    tc = ctx.load_module('thermocycler')
    tc.open_lid()
    tc_plate = tc.load_labware('nest_96_wellplate_100ul_pcr_full_skirt')
    tipracks300 = [
        ctx.load_labware('opentrons_96_tiprack_300ul', slot)
        for slot in ['3']]
    tipracks20 = [
        ctx.load_labware('opentrons_96_tiprack_20ul', slot)
        for slot in ['6']]
    dil_plate = ctx.load_labware('nest_96_wellplate_100ul_pcr_full_skirt', '5')
    res = ctx.load_labware('nest_12_reservoir_15ml', '2')
    tuberack = ctx.load_labware(
        'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', '4')
    mm_plate = ctx.load_labware('nest_96_wellplate_100ul_pcr_full_skirt', '1')

    m300 = ctx.load_instrument(
        'p300_multi_gen2', 'right', tip_racks=tipracks300)
    p20 = ctx.load_instrument(
        'p20_multi_gen2', 'left', tip_racks=tipracks20)

    samples = tuberack.wells()[:num_samples]
    mm = res.wells()[0]
    rxn_mix_1 = res.wells()[1]
    rxn_mix_2 = res.wells()[2]
    diluent = res.wells()[3]

    def pick_up(pip):
        try:
            pip.pick_up_tip()
        except protocol_api.labware.OutOfTipsError:
            ctx.pause("Replace the tips")
            pip.reset_tipracks()
            pip.pick_up_tip()

    tips_single = tipracks20[-1].wells()
    default_current = 0.6

    # offset tip pickup
    def pick_up_single(pip=p20):
        mount = Mount.LEFT if pip.mount == 'left' else Mount.RIGHT
        ctx._hw_manager.hardware._attached_instruments[
            mount].update_config_item(
                'pick_up_current', default_current/8)
        tip = tips_single.pop()
        pip.pick_up_tip(tip)
        ctx._hw_manager.hardware._attached_instruments[
            mount].update_config_item(
                'pick_up_current', default_current)

    def wick(pip, well, side=1):
        if well.diameter:
            radius = well.diameter/2
        else:
            radius = well.width/2
        pip.move_to(well.bottom().move(Point(x=side*radius*0.7, z=3)))

    def slow_withdraw(pip, well, delay=1.0):
        pip.default_speed /= 16
        ctx.delay(seconds=delay)
        pip.move_to(well.top())
        pip.default_speed *= 16

    # mm
    mm_dests = [
        well
        for i in range(num_cols)
        for well in mm_plate.columns()[i*4]]
    pick_up(p20)
    for d in mm_dests:
        p20.aspirate(16.5, mm)
        slow_withdraw(p20, mm)
        p20.dispense(16.5, d.bottom(1))
        slow_withdraw(p20, d)
    p20.drop_tip()

    # first dilution
    first_dil_dests_m = [tc_plate.rows()[0][i*4] for i in range(num_cols)]
    pick_up(m300)
    for d in first_dil_dests_m:
        m300.aspirate(180, diluent)
        slow_withdraw(m300, diluent)
        m300.dispense(180, d.bottom(5))
        slow_withdraw(m300, d)
    m300.drop_tip()

    rxn_mix_1_dests = [tc_plate.rows()[0][i*4+1] for i in range(num_cols)]
    pick_up(m300)
    for d in rxn_mix_1_dests:
        m300.aspirate(30, rxn_mix_1)
        slow_withdraw(m300, rxn_mix_1)
        m300.dispense(30, d.bottom(2))
        slow_withdraw(m300, d)
    m300.drop_tip()

    # transfer sample
    first_dil_cols = [tc_plate.columns()[i*4] for i in range(num_cols)]
    first_dil_dests_s = [
        well for col in first_dil_cols for well in col][:num_samples]
    for s, d in zip(samples, first_dil_dests_s):
        pick_up(m300)
        m300.aspirate(20, s.bottom(0.5))
        slow_withdraw(m300, s)
        m300.dispense(20, d.top(-5))
        m300.mix(5, 100, d.bottom(d.depth/2))
        slow_withdraw(m300, d)
        m300.drop_tip()

    # add to mix
    for s, d in zip(first_dil_dests_m, rxn_mix_1_dests):
        pick_up(m300)
        m300.aspirate(20, s.bottom(5))
        slow_withdraw(m300, s)
        m300.dispense(20, d.bottom(2))
        m300.mix(5, 20, d.bottom(d.depth/2))
        slow_withdraw(m300, d)
        m300.drop_tip()

    if DO_THERMOCYCLER:
        tc.close_lid()
        tc.set_block_temperature(37, hold_time_minutes=30)
        tc.open_lid()

    # rxn mix 2
    for d in rxn_mix_1_dests:
        pick_up(m300)
        m300.aspirate(50, rxn_mix_2)
        slow_withdraw(m300, rxn_mix_2)
        m300.dispense(50, d.bottom(2))
        m300.mix(5, 20, d.bottom(d.depth/2))
        slow_withdraw(m300, d)
        m300.drop_tip()

    if DO_THERMOCYCLER:
        tc.close_lid()
        tc.set_block_temperature(55, hold_time_minutes=30)
        tc.set_block_temperature(95, hold_time_minutes=15)
        tc.set_block_temperature(4)
        tc.open_lid()

    dil_sets_tc = [
        tc_plate.rows()[0][i*4+2:i*4+4] for i in range(3)
    ]
    dil_sets_dil = [
        dil_plate.rows()[0][i*3:i*3+3] for i in range(3)
    ]
    dil_sets_all = []
    for set_t, set_d in zip(dil_sets_tc, dil_sets_dil):
        dil_set = set_t + set_d
        dil_sets_all.append(dil_set)

    # add diluent to all
    pick_up(m300)
    for d_set in dil_sets_all:
        for d in d_set:
            m300.aspirate(180, diluent)
            slow_withdraw(m300, diluent)
            m300.dispense(180, d.bottom(5))
            slow_withdraw(m300, d)

    # perform dilutions
    for i, dil_set in enumerate(dil_sets_all):
        sources = [rxn_mix_1_dests[i]] + dil_set[:len(dil_sets_all)-1]
        dests = dil_set[1:]
        if not m300.has_tip:
            pick_up(m300)
        for s, d in zip(sources, dests):
            m300.aspirate(20, s.bottom(5))
            slow_withdraw(m300, s)
            m300.dispense(20, d.bottom(d.depth/2))
            m300.mix(5, 50, d.bottom(d.depth/2))
            slow_withdraw(m300, d)
        m300.drop_tip()

    cp_sources = [dil_plate.wells_by_name()[well] for well in cp_list]
    cp_dests = [
        well for col in mm_plate.columns()[::4]
        for well in col]
    for s, d in zip(cp_sources, cp_dests):
        pick_up(p20)
        p20.aspirate(5.5, s.bottom(5))
        slow_withdraw(p20, s)
        p20.dispense(5.5, d.bottom(2))
        p20.mix(5, 10, d.bottom(2))
        slow_withdraw(p20, d)
        p20.drop_tip()

    if DO_THERMOCYCLER:
        tc.close_lid()
        tc.set_block_temperature(95, hold_time_minutes=10)
        profile = [
            {'temperature': 95, 'hold_time_seconds': 30},
            {'temperature': 60, 'hold_time_seconds': 100}
        ]
        tc.execute_profile(steps=profile, repetitions=40, block_max_volume=22)
        tc.set_block_temperature(98, hold_time_minutes=10)
        tc.set_block_temperature(4)
        tc.open_lid()
