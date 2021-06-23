import math

metadata = {
    'protocolName': 'Sample Prep for ELISA Test of Monoclonal Antibodies',
    'author': 'Rami Farawi <rami.farawi@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.7'
}


def run(ctx):

    # load labware
    [mix_reps, mix_vol, v_0_tube1, v_0_tube2, clearance, mix_clearance,
     p20_mount, p1000_mount] = get_values(  # noqa: F821
        'mix_reps', 'mix_vol', 'v_0_tube1', 'v_0_tube2', 'clearance',
        'mix_clearance', 'p20_mount', 'p1000_mount')

    ctrl_plates = [ctx.load_labware('greiner_384_wellplate_200ul', slot)
                   for slot in ['9', '6', '3']]
    diluent_tubes = ctx.load_labware(
                    'appleton_6_tuberack_50000ul', '7')
    reagent = ctx.load_labware('axygen_24_tuberack_1700ul', '8')
    master_block = ctx.load_labware('nest_96_wellplate_2ml_deep', '4')
    tiprack20 = [ctx.load_labware('opentrons_96_tiprack_20ul', '2')]
    tiprack1000 = [ctx.load_labware('opentrons_96_tiprack_1000ul', slot)
                   for slot in ['1', '5']]

    # load instrument
    p20 = ctx.load_instrument('p20_single_gen2', p20_mount,
                              tip_racks=tiprack20)
    p1000 = ctx.load_instrument('p1000_single_gen2', p1000_mount,
                                tip_racks=tiprack1000)

    p1000.well_bottom_clearance.aspirate = clearance
    p1000.well_bottom_clearance.dispense = clearance

    def move_384(source, dest1, dest2):
        p1000.aspirate(400, s)
        p1000.dispense(180, dest1.top(z=-8))
        p1000.touch_tip()
        p1000.dispense(180, dest2.top(z=-8))
        p1000.touch_tip()
        p1000.dispense(40, source.top(z=-5))

    def adjust_height(vol, diluent_tube):
        nonlocal h1
        nonlocal h2
        dh = vol/(math.pi*radius**2)
        if diluent_tube == 1:
            h1 -= dh
            if h1 < 20:
                h1 = 1
            else:
                return h1 - 10
        else:
            h2 -= dh
            if h2 < 10:
                h2 = 1
            else:
                return h2 - 10

    # load reagents
    diluent_tubes = diluent_tubes.rows()[0][:2]
    diluent = diluent_tubes[0]
    conc_300 = reagent.rows()[0][::2]
    conc_100 = reagent.rows()[0][1::2]
    cr3022 = reagent.rows()[2][0]
    mab45 = reagent.rows()[2][1]
    mab269 = reagent.rows()[2][2]
    ab = [cr3022, mab45, mab269]
    tf = reagent.rows()[3][4:5]
    negative = reagent.rows()[3][5]

    # liquid height tracking
    v_naught1 = v_0_tube1
    v_naught2 = v_0_tube2
    radius = diluent_tubes[0].diameter/2
    h_naught1 = v_naught1/(math.pi*radius**2)
    h_naught2 = v_naught2/(math.pi*radius**2)
    h1 = h_naught1
    h2 = h_naught2

    # 300 ug/ml distribution of diluent
    p20.pick_up_tip()
    for d in conc_300:
        p20.aspirate(17.5, diluent.bottom(z=h1))
        adjust_height(17.5, 1)
        p20.dispense(17.5, d)
        p20.blow_out()
        p20.touch_tip()
    p20.drop_tip()
    ctx.comment('\n\n\n')

    # 100 ug/ml distribution of diluent
    p20.pick_up_tip()
    for d in conc_100:
        for _ in range(2):
            p20.aspirate(18, diluent.bottom(z=h1))
            adjust_height(18, 1)
            p20.dispense(18, d)
            p20.blow_out()
            p20.touch_tip()
    p20.drop_tip()
    ctx.comment('\n\n\n')

    # 300 ug/ml distribution of antibody
    for s, d in zip(ab, conc_300):
        p20.pick_up_tip()
        p20.aspirate(7.5, s)
        p20.dispense(7.5, d)
        p20.blow_out()
        p20.touch_tip()
        p20.drop_tip()
    ctx.comment('\n\n\n')

    # 100 ug/ml distribution of antibody
    for s, d in zip(ab, conc_100):
        p20.pick_up_tip()
        p20.aspirate(4, s)
        p20.dispense(4, d)
        p20.blow_out()
        p20.touch_tip()
        p20.drop_tip()
    ctx.comment('\n\n\n')

    # distribute diluent to second stepped down row

    for d in reagent.rows()[1]:
        p1000.pick_up_tip()
        p1000.aspirate(180, diluent.bottom(z=h1))
        adjust_height(180, 1)
        p1000.dispense(180, d.top(z=-5))
        p1000.blow_out()
        p1000.touch_tip()
        p1000.drop_tip()
    ctx.comment('\n\n\n')

    # step down
    for conc_well, dilute_well in zip(
            reagent.rows()[0], reagent.rows()[1]):
        p20.pick_up_tip()
        p20.mix(5, 17, conc_well.bottom(z=3))
        p20.aspirate(20, conc_well)
        p20.dispense(20, dilute_well)
        p20.blow_out()
        p20.touch_tip()
        p20.drop_tip()
        p1000.pick_up_tip()
        p1000.mix(5, 180, dilute_well.bottom(z=3))
        p1000.drop_tip()
    ctx.comment('\n\n\n')

    # distibute diluent to master block
    map1 = [well for row in master_block.rows()[:3] for well in row[:6]]
    p1000.pick_up_tip()
    for d in map1:
        p1000.transfer(1350, diluent, d, new_tip='never')
        adjust_height(1350, 1)
    p1000.transfer(1350, diluent, [master_block.wells()[3],
                   master_block.rows()[3][1]], new_tip='never')
    adjust_height(1350, 1)

    diluent = diluent_tubes[1]  # switch diluent tubes
    p1000.transfer(1470, diluent,
                   master_block.wells_by_name()['D6'], new_tip='never')
    adjust_height(1470, 2)
    p1000.transfer(400, diluent,
                   [master_block.wells()[4:7:2]], new_tip='never')  # E1, G1
    adjust_height(400, 2)
    p1000.transfer(1840, diluent,
                   [master_block.wells()[5:8:2]], new_tip='never')  # F1, H1
    adjust_height(1840, 2)

    map2 = [well for row in master_block.rows()[4:8] for well in row[1:5]]
    for d in map2:
        p1000.transfer(1000, diluent, d, new_tip='never')
        adjust_height(1000, 2)
    p1000.drop_tip()
    ctx.comment('\n\n\n')

    # add ab to master block
    for tube, well in zip(reagent.rows()[1], master_block.rows()[0]):
        p1000.pick_up_tip()
        p1000.aspirate(150, tube)
        p1000.dispense(150, well)
        p1000.mix(mix_reps, mix_vol, well.bottom(z=mix_clearance))
        p1000.blow_out()
        p1000.touch_tip()
        p1000.drop_tip()
    ctx.comment('\n\n\n')

    # dilute ab down two rows
    row_start = 0
    for _ in range(2):
        for conc_well, dilut_well in zip(
                            master_block.rows()[row_start][:6],
                            master_block.rows()[row_start+1]):
            p1000.pick_up_tip()
            p1000.aspirate(150, conc_well)
            p1000.dispense(150, dilut_well)
            p1000.mix(mix_reps, mix_vol, dilut_well.bottom(z=mix_clearance))
            p1000.blow_out()
            p1000.touch_tip()
            p1000.drop_tip()
        row_start += 1
    ctx.comment('\n\n\n')

    for conc_well, dilut_well in zip(master_block.rows()[2][:2],
                                     master_block.rows()[3][:2]):  # C1C2->D1D2
        p1000.pick_up_tip()
        p1000.aspirate(150, conc_well)
        p1000.dispense(150, dilut_well)
        p1000.blow_out()
        p1000.touch_tip()
        p1000.mix(mix_reps, mix_vol, dilut_well.bottom(z=mix_clearance))
        p1000.drop_tip()
    ctx.comment('\n\n\n')

    # transfer negative
    p1000.pick_up_tip()
    p1000.aspirate(300, negative)
    p1000.dispense(300, master_block.wells_by_name()['D6'])
    p1000.blow_out()
    p1000.touch_tip()
    p1000.drop_tip()
    ctx.comment('\n\n\n')

    # transfer postive control
    for tube, well in zip(tf, master_block.wells()[4:7:2]):
        p1000.pick_up_tip()
        p1000.transfer(1600, tube, well.top(z=-5), new_tip='never')
        p1000.mix(mix_reps, mix_vol, well.bottom(z=mix_clearance))
        p1000.blow_out()
        p1000.touch_tip()
        p1000.drop_tip()
    for tube, well in zip(tf, master_block.wells()[5:8:2]):
        p1000.pick_up_tip()
        p1000.transfer(160, tube, well.top(z=-5), new_tip='never')
        p1000.mix(mix_reps, mix_vol, well.bottom(z=mix_clearance))
        p1000.blow_out()
        p1000.touch_tip()
        p1000.drop_tip()
    ctx.comment('\n\n\n')

    # dilute E1 - H1 across 5 columns
    col_start = 0
    for _ in range(4):
        for conc_well, dilut_well in zip(
                            master_block.columns()[col_start][4:8],
                            master_block.columns()[col_start+1][4:8]):
            p1000.pick_up_tip()
            p1000.aspirate(1000, conc_well)
            p1000.dispense(1000, dilut_well)
            p1000.mix(mix_reps, mix_vol, dilut_well.bottom(z=mix_clearance))
            p1000.blow_out()
            p1000.touch_tip()
            p1000.drop_tip()
        col_start += 1
    ctx.comment('\n\n\n')

    # transfer 3022 (300 conc) to 384 well plate
    map_384_A1 = [well for plate in ctrl_plates
                  for well in plate.columns()[0][:8:2]]
    map_384_I23 = [well for plate in ctrl_plates
                   for well in plate.columns()[22][8::2]]

    for s, d1, d2 in zip(master_block.wells()[:4]*3, map_384_A1, map_384_I23):
        p1000.pick_up_tip()
        p1000.aspirate(400, s)
        p1000.dispense(180, d1.top(z=-8))
        p1000.touch_tip()
        p1000.dispense(180, d2.top(z=-8))
        p1000.touch_tip()
        p1000.dispense(40, s.top(z=-5))
        p1000.drop_tip()
    ctx.comment('\n\n\n')

    # transfer 3022 (100 conc)
    map_384_B1 = [well for plate in ctrl_plates
                  for well in plate.columns()[0][1:8:2]]
    map_384_J23 = [well for plate in ctrl_plates
                   for well in plate.columns()[22][9::2]]

    for s, d1, d2 in zip(master_block.columns()[1][:4]*3,
                         map_384_B1, map_384_J23):
        p1000.pick_up_tip()
        move_384(s, d1, d2)
        p1000.drop_tip()
    ctx.comment('\n\n\n')

    # transfer mAb45 (300 & 100 conc)
    map_384_A2 = [well for plate in ctrl_plates
                  for well in plate.columns()[1][0:4:2]]
    map_384_L24 = [well for plate in ctrl_plates
                   for well in plate.columns()[23][11:15:2]]
    # step 3

    for s, d1, d2 in zip(master_block.columns()[2][1:3]*3,
                         map_384_A2, map_384_L24):
        p1000.pick_up_tip()
        move_384(s, d1, d2)
        p1000.drop_tip()
    ctx.comment('\n\n\n')

    # step 4
    map_384_B2 = [well for plate in ctrl_plates
                  for well in plate.columns()[1][1:5:2]]
    map_384_M24 = [well for plate in ctrl_plates
                   for well in plate.columns()[23][12:16:2]]

    for s, d1, d2 in zip(master_block.columns()[3][1:3]*3,
                         map_384_B2, map_384_M24):
        p1000.pick_up_tip()
        move_384(s, d1, d2)
        p1000.drop_tip()
    ctx.comment('\n\n\n')

    # step 5-8

    sources = ['B5', 'C5', 'B5', 'C5', 'B6', 'C6', 'B6', 'C6']
    dests = ['A23', 'C23', 'E23', 'G23', 'B23', 'D23', 'F23', 'H23']

    for s, d in zip(sources, dests):
        p1000.pick_up_tip()
        p1000.aspirate(600, master_block.wells_by_name()[s])
        for i in range(3):
            p1000.dispense(180, ctrl_plates[i].wells_by_name()[d].top(z=-8))
            p1000.touch_tip()
        p1000.dispense(60, master_block.wells_by_name()[s].top(z=-5))
        p1000.drop_tip()
    ctx.comment('\n\n\n')

    # steps 9 - 23

    sources = ['E1', 'E2', 'E3', 'E4', 'E5',
               'E1', 'E2', 'E3', 'E4', 'E5',
               'F1', 'F2', 'F3', 'F4', 'F5',
               'F1', 'F2', 'F3', 'F4', 'F5']
    dests = ['E2', 'G2', 'I2', 'K2', 'M2',
             'A24', 'C24', 'E24', 'G24', 'I24',
             'F2', 'H2', 'J2', 'L2', 'N2',
             'B24', 'D24', 'F24', 'H24', 'J24']
    for s, d in zip(sources, dests):
        p1000.pick_up_tip()
        p1000.aspirate(400, master_block.wells_by_name()[s])
        for i in range(2):
            p1000.dispense(180, ctrl_plates[i].wells_by_name()[d].top(z=-8))
            p1000.touch_tip()
        p1000.dispense(40, master_block.wells_by_name()[s].top(z=-5))
        p1000.drop_tip()
    ctx.comment('\n\n\n')

    # steps 29 - 38
    map_384_E2 = [well for well in ctrl_plates[2].columns()[1][4:14:2]]
    map_384_A24 = [well for well in ctrl_plates[2].columns()[23][:10:2]]

    for s, d1, d2 in zip(master_block.rows()[6][:5]*2,
                         map_384_E2, map_384_A24):
        p1000.pick_up_tip()
        p1000.aspirate(400, s)
        p1000.dispense(180, d1.top(z=-8))
        p1000.touch_tip()
        p1000.dispense(180, d2.top(z=-8))
        p1000.touch_tip()
        p1000.dispense(40, s.top(z=-5))
        p1000.drop_tip()
    ctx.comment('\n\n\n')

    map_384_F2 = [well for well in ctrl_plates[2].columns()[1][5:15:2]]
    map_384_B24 = [well for well in ctrl_plates[2].columns()[23][1:11:2]]

    for s, d1, d2 in zip(master_block.rows()[6][:5]*2,
                         map_384_F2, map_384_B24):
        p1000.pick_up_tip()
        p1000.aspirate(400, s)
        p1000.dispense(180, d1.top(z=-8))
        p1000.touch_tip()
        p1000.dispense(180, d2.top(z=-8))
        p1000.touch_tip()
        p1000.dispense(40, s.top(z=-5))
        p1000.drop_tip()
    ctx.comment('\n\n\n')

    # steps 49-50
    i24 = [plate.wells_by_name()['I1'] for plate in ctrl_plates]
    k24 = [plate.wells_by_name()['K24'] for plate in ctrl_plates]

    p1000.pick_up_tip()
    p1000.aspirate(600, master_block.wells_by_name()['D6'])
    for dest in i24:
        p1000.dispense(180, dest)
        p1000.touch_tip()
    p1000.drop_tip()

    ctx.comment('\n\n\n')

    p1000.pick_up_tip()
    p1000.aspirate(600, master_block.wells_by_name()['D6'])
    for dest in k24:
        p1000.dispense(180, dest)
        p1000.touch_tip()
    p1000.drop_tip()
    ctx.comment('\n\n\n')

    # step 50
    dests = ['J1', 'K1', 'L1', 'M1', 'N1',
             'O1', 'P1', 'O2', 'P2', 'P24']

    for plate in ctrl_plates:
        p1000.pick_up_tip()
        for dest in dests:
            p1000.aspirate(1000, diluent)
            adjust_height(1000, 2)
            p1000.dispense(1000, plate.wells_by_name()[dest])
            p1000.blow_out()
            p1000.touch_tip()
        p1000.drop_tip()
