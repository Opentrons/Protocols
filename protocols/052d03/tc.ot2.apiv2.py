import math
from opentrons import protocol_api
from opentrons.types import Point

metadata = {
    'apiLevel': '2.14',
    'protocolName': 'Custom Dilution and PCR',
    'author': 'Nick Diehl <ndiehl@opentrons.com>'
}

DO_THERMOCYCLER = False
DO_FIRST_DILUTION = True

# 101 - 1 enzymatic reaction (no second rxn mix)
# 401 - exactly like this
# pDNA - only second enzymatic rxn
# (10ul sample neat into column 3 with 90ul rxn mix)


def run(ctx):

    [num_samples, cp_list, type_molecule] = get_values(  # noqa: F821
        'num_samples', 'cp_list', 'type_molecule')

    # [num_samples, cp_list, type_molecule] = [24, cp_list_ex, 'pDNA']

    # parse
    data = [
        [val.strip().upper() for val in line.split(',')]
        for line in cp_list.splitlines()
        if line and line.split(',')[0].strip()]

    num_cols = math.ceil((num_samples+1)/8)
    tc = ctx.load_module('thermocycler')
    tc.open_lid()
    tc_plate = tc.load_labware('biorad_96_wellplate_200ul_pcr')
    tipracks300 = [
        ctx.load_labware('opentrons_96_tiprack_300ul', slot)
        for slot in ['3']]
    tipracks20 = [
        ctx.load_labware('opentrons_96_tiprack_20ul', slot)
        for slot in ['6', '9']]
    dil_plate = ctx.load_labware('biorad_96_wellplate_200ul_pcr',
                                 '5', 'dilution plate')
    res = ctx.load_labware('nest_12_reservoir_15ml', '2')
    tuberack = ctx.load_labware(
        'opentrons_24_aluminumblock_nest_1.5ml_snapcap', '4')
    mm_plate = ctx.load_labware('biorad_96_aluminumblock_250ul', '1',
                                'mastermix plate')

    m300 = ctx.load_instrument(
        'p300_multi_gen2', 'left', tip_racks=tipracks300)
    p20 = ctx.load_instrument(
        'p20_single_gen2', 'right', tip_racks=tipracks20)

    samples = tuberack.wells()[:num_samples]
    pc = tuberack.wells()[num_samples]
    rxn_mix_1 = res.wells()[0]
    rxn_mix_2 = res.wells()[1]
    diluent = res.wells()[2:4]
    mm = res.wells()[4]

    # # define liquids
    # rxn_mix_1_liq = ctx.define_liquid(
    #     name="DNAse",
    #     description="DNAse",
    #     display_color="#00FF00",
    # )
    # rxn_mix_2_liq = ctx.define_liquid(
    #     name="PK",
    #     description="PK",
    #     display_color="#0000FF",
    # )
    # diluent_liq = ctx.define_liquid(
    #     name="dilution buffer",
    #     description="dilution buffer",
    #     display_color="#FF0000",
    # )
    # mastermix_liq = ctx.define_liquid(
    #     name="mastermix",
    #     description="mastermix",
    #     display_color="#FBFF00",
    # )
    # sample_liq = ctx.define_liquid(
    #     name="sample",
    #     description="sample, NTC, and DAC",
    #     display_color="#F300FF",
    # )
    # pc_liq = ctx.define_liquid(
    #     name="positive control",
    #     description="positive control",
    #     display_color="#050F5D",
    # )

    # # load liquids
    # [s.load_liquid(sample_liq, volume=200) for s in samples]
    # pc.load_liquid(pc_liq, volume=200)
    # if not type_molecule == 'pDNA':
    #     rxn_mix_1.load_liquid(rxn_mix_1_liq, volume=30*num_cols*8)
    # if not type_molecule == '101':
    #     rxn_mix_2.load_liquid(rxn_mix_2_liq, volume=50*num_cols*8)
    # mm.load_liquid(mastermix_liq, volume=16.5*len(data)*4)
    # [d.load_liquid(diluent_liq, volume=13500) for d in diluent]

    def pick_up(pip):
        try:
            pip.pick_up_tip()
        except protocol_api.labware.OutOfTipsError:
            ctx.pause("Replace the tips")
            pip.reset_tipracks()
            pip.pick_up_tip()

    vol_max_dil = 0.85*diluent[0].max_volume
    vol_current = 0
    dil_tracker = iter(diluent)
    dil_current = next(dil_tracker)

    def track_dilution(vol):
        nonlocal vol_current
        nonlocal dil_current
        if vol + vol_current > vol_max_dil:
            vol_current = 0
            dil_current = next(dil_tracker)
        vol_current += vol
        return dil_current

    def wick(pip, well, side=1):
        if well.diameter:
            radius = well.diameter/2
        else:
            radius = well.width/2
        pip.move_to(well.bottom().move(Point(x=side*radius*0.7, z=3)))

    def slow_withdraw(pip, well, delay=2.0):
        pip.default_speed /= 16
        ctx.delay(seconds=delay)
        pip.move_to(well.top())
        pip.default_speed *= 16

    # first dilution
    first_dil_dests_m = [tc_plate.rows()[0][i*4] for i in range(num_cols)]
    pick_up(m300)
    vol_dil = 180
    for d in first_dil_dests_m:
        source = track_dilution(vol_dil)
        m300.aspirate(vol_dil, source)
        slow_withdraw(m300, source)
        m300.dispense(vol_dil, d.bottom(5))
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
        pick_up(p20)
        p20.aspirate(20, s.bottom(0.5))
        slow_withdraw(p20, s)
        p20.dispense(20, d.top(-5))
        # p20.mix(5, 20, d.bottom(d.depth/2))
        slow_withdraw(p20, d)
        p20.drop_tip()

    # add to mix
    for s, d in zip(first_dil_dests_m, rxn_mix_1_dests):
        pick_up(m300)
        m300.mix(5, 100, s.bottom(s.depth/2))
        m300.aspirate(20, s.bottom(5))
        slow_withdraw(m300, s)
        m300.dispense(20, d.bottom(2))
        m300.mix(5, 20, d.bottom(d.depth/2))
        slow_withdraw(m300, d)
        m300.drop_tip()

    tc.close_lid()
    if DO_THERMOCYCLER:
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

    tc.close_lid()
    if DO_THERMOCYCLER:
        tc.set_block_temperature(55, hold_time_minutes=30)
        tc.set_block_temperature(95, hold_time_minutes=15)
        tc.set_block_temperature(4)
    tc.open_lid()

    dil_sets_tc = [
        tc_plate.rows()[0][i*4+2:i*4+4] for i in range(num_cols)
    ]
    dil_sets_dil = [
        dil_plate.rows()[0][i*4:i*4+4] for i in range(num_cols)
    ]
    dil_sets_all = []
    for set_t, set_d in zip(dil_sets_tc, dil_sets_dil):
        dil_set = set_t + set_d
        dil_sets_all.append(dil_set)

    # add diluent to all
    pick_up(m300)
    vol_dil = 180
    for d_set in dil_sets_all:
        for d in d_set:
            source = track_dilution(vol_dil)
            m300.aspirate(vol_dil, source)
            slow_withdraw(m300, source)
            m300.dispense(vol_dil, d.bottom(5))
            slow_withdraw(m300, d)

    # perform dilutions
    for i, dil_set in enumerate(dil_sets_all):
        sources = [rxn_mix_1_dests[i]] + dil_set[:len(dil_sets_all[0])-1]
        dests = dil_set
        if not m300.has_tip:
            pick_up(m300)
        for s, d in zip(sources, dests):
            m300.aspirate(20, s.bottom(5))
            slow_withdraw(m300, s)
            m300.dispense(20, d.bottom(d.depth/2))
            m300.mix(5, 50, d.bottom(d.depth/2))
            slow_withdraw(m300, d)
        m300.drop_tip()

    # mm
    mm_dest_sets = [
        mm_plate.rows()[i % 8][(i//8)*4:(i//8 + 1)*4]
        for i in range(len(data))]
    pick_up(p20)
    for d_set in mm_dest_sets:
        for d in d_set:
            p20.aspirate(16.5, mm)
            slow_withdraw(p20, mm)
            p20.dispense(16.5, d.bottom(1))
            slow_withdraw(p20, d)
    p20.drop_tip()

    # dilute positive control
    pc_dil_set = dil_sets_all[-1]
    pc_column_indices = [
        dil_plate.rows()[0].index(col)
        for col in pc_dil_set[2:4]]
    pc_dil_wells = [
        dil_plate.columns()[index][-1]
        for index in pc_column_indices]
    pc_dil_sources = [pc, pc_dil_wells[0]]
    pc_mm_dest_set = mm_dest_sets.pop(2)
    pick_up(p20)
    for s, d in zip(pc_dil_sources, pc_dil_wells):
        p20.aspirate(20, s)
        slow_withdraw(p20, s)
        p20.dispense(20, d.bottom(d.depth/2))
        p20.mix(5, 20, d.bottom(d.depth/2))
    for d in pc_mm_dest_set:
        if not p20.has_tip:
            pick_up(p20)
        p20.aspirate(5.5, pc_dil_wells[-1].bottom(5))
        slow_withdraw(p20, pc_dil_wells[-1])
        p20.dispense(5.5, d.bottom(2))
        slow_withdraw(p20, d)
        p20.drop_tip()

    # cherrypick
    cp_lw_map = {
        'T': tc_plate,
        'D': dil_plate
    }
    cp_sources = [
        cp_lw_map[line[1][0]].wells_by_name()[line[0]]
        for line in data]
    for s, d_set in zip(cp_sources, mm_dest_sets):
        for d in d_set:
            pick_up(p20)
            p20.aspirate(5.5, s.bottom(5))
            slow_withdraw(p20, s)
            p20.dispense(5.5, d.bottom(2))
            slow_withdraw(p20, d)
            p20.drop_tip()
