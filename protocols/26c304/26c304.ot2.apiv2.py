metadata = {
    'protocolName': 'Sample Prep for ELISA Test of Monoclonal Antibodies',
    'author': 'Rami Farawi <rami.farawi@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.7'
}


def run(ctx):

    # load labware
    [p20_mount, p1000_mount] = get_values(  # noqa: F821
        'p20_mount', 'p1000_mount')

    ctrl_plates = [ctx.load_labware('greiner_384_wellplate_200ul', slot)
                   for slot in ['9', '6', '3']]
    diluent_tubes = ctx.load_labware(
                    'appleton_6_tuberack_50000ul', '7')
    reagent = ctx.load_labware('axygen_24_tuberack_1700ul', '8')
    master_block = ctx.load_labware('nest_96_wellplate_2ml_deep', '4')
    tiprack20 = [ctx.load_labware('opentrons_96_tiprack_20ul', '2')]
    tiprack1000 = [ctx.load_labware('opentrons_96_tiprack_1000ul', '1')]

    # load instrument
    p20 = ctx.load_instrument('p20_single_gen2', p20_mount,
                              tip_racks=tiprack20)
    p1000 = ctx.load_instrument('p1000_single_gen2', p1000_mount,
                                tip_racks=tiprack1000)

    # load reagents
    diluent_tubes = diluent_tubes.rows()[0][:2]
    diluent = diluent_tubes[0]
    conc_300 = reagent.rows()[0][::2]
    conc_100 = reagent.rows()[0][1::2]
    cr3022 = reagent.rows()[2][0]
    mab45 = reagent.rows()[2][1]
    mab269 = reagent.rows()[2][2]
    ab = [cr3022, mab45, mab269]
    tf = reagent.rows()[3][3:5]
    negative = reagent.rows()[3][5]

    # 300 ug/ml distribution of diluent
    p20.pick_up_tip()
    for d in conc_300:
        p20.aspirate(17.5, diluent)
        p20.dispense(17.5, d)
    p20.drop_tip()

    # 100 ug/ml distribution of diluent
    p20.pick_up_tip()
    for d in conc_100:
        p20.transfer(36, diluent, d, new_tip='never')
    p20.drop_tip()

    # 300 ug/ml distribution of antibody
    for s, d in zip(ab, conc_300):
        p20.pick_up_tip()
        p20.aspirate(7.5, s)
        p20.dispense(7.5, d)
        p20.blow_out()
        p20.drop_tip()

    # 100 ug/ml distribution of antibody
    for s, d in zip(ab, conc_100):
        p20.pick_up_tip()
        p20.aspirate(4, s)
        p20.dispense(4, d)
        p20.blow_out()
        p20.drop_tip()

    # distribute diluent to second stepped down row
    p1000.pick_up_tip()
    for d in reagent.rows()[1]:
        p1000.aspirate(180, diluent)
        p1000.dispense(180, d.top())
    p1000.drop_tip()

    # step down
    for conc_well, dilute_well in zip(
            reagent.rows()[0], reagent.rows()[1]):
        p20.pick_up_tip()
        p20.mix(10, 17, conc_well)
        p20.aspirate(20, conc_well)
        p20.dispense(20, dilute_well)
        p20.mix(15, 17, dilute_well)
        p20.drop_tip()
    ctx.comment('\n\n\n')

    # distibute diluent to master block
    map1 = [well for row in master_block.rows()[:3] for well in row[:6]]
    p1000.pick_up_tip()
    for d in map1:
        p1000.transfer(1350, diluent, d, new_tip='never')
    p1000.transfer(1350, diluent, [master_block.wells()[3],
                   master_block.rows()[3][1]], new_tip='never')

    diluent = diluent_tubes[1]  # switch diluent tubes
    p1000.transfer(1470, diluent,
                   master_block.wells_by_name()['D6'], new_tip='never')
    p1000.transfer(400, diluent,
                   [master_block.wells()[4:7:2]], new_tip='never')  # E1, G1
    p1000.transfer(1840, diluent,
                   [master_block.wells()[5:8:2]], new_tip='never')  # F1, H1

    map2 = [well for row in master_block.rows()[4:8] for well in row[1:5]]
    for d in map2:
        p1000.transfer(1000, diluent, d, new_tip='never')
    p1000.drop_tip()

    # add ab to master block
    for tube, well in zip(reagent.rows()[1], master_block.rows()[0]):
        p1000.pick_up_tip()
        p1000.aspirate(150, tube)
        p1000.dispense(150, well)
        p1000.mix(10, 1000, well)
        p1000.drop_tip()

    # dilute ab down two rows
    ctx.comment('fff')
    row_start = 0
    for _ in range(2):
        for conc_well, dilut_well in zip(
                            master_block.rows()[row_start][:6],
                            master_block.rows()[row_start+1]):
            p1000.pick_up_tip()
            p1000.aspirate(150, conc_well)
            p1000.dispense(150, dilut_well)
            p1000.mix(10, 1000, dilut_well)
            p1000.drop_tip()
        row_start += 1

    for conc_well, dilut_well in zip(master_block.rows()[2][:2],
                                     master_block.rows()[3][:2]):  # C1C2->D1D2
        p1000.pick_up_tip()
        p1000.aspirate(150, conc_well)
        p1000.dispense(150, dilut_well)
        p1000.mix(10, 1000, dilut_well)
        p1000.drop_tip()

    # transfer negative
    p1000.pick_up_tip()
    p1000.aspirate(300, negative)
    p1000.dispense(300, master_block.wells_by_name()['D6'])
    p1000.drop_tip()

    # transfer postive control
    for tube, well in zip(tf, master_block.wells()[4:7:2]):
        p1000.pick_up_tip()
        p1000.transfer(1600, tube, well.top(), new_tip='never')
        p1000.mix(10, 1000, well)
        p1000.drop_tip()
    for tube, well in zip(tf, master_block.wells()[5:8:2]):
        p1000.pick_up_tip()
        p1000.transfer(160, tube, well.top(), new_tip='never')
        p1000.mix(10, 1000, well)
        p1000.drop_tip()

    # dilute E1 - H1 across 5 columns
    col_start = 0
    for _ in range(4):
        for conc_well, dilut_well in zip(
                            master_block.columns()[col_start][4:8],
                            master_block.columns()[col_start+1][4:8]):
            p1000.pick_up_tip()
            p1000.aspirate(1000, conc_well)
            p1000.dispense(1000, dilut_well)
            p1000.mix(10, 1000, dilut_well)
            p1000.drop_tip()
        col_start += 1

    # transfer 3022 (300 conc) to 384 well plate
    map_384_A1 = [well for plate in ctrl_plates
                  for well in plate.columns()[0][:8:2]]
    map_384_I23 = [well for plate in ctrl_plates
                   for well in plate.columns()[22][8::2]]
    p1000.pick_up_tip()
    for s, d1, d2 in zip(master_block.wells()[:4]*3, map_384_A1, map_384_I23):
        p1000.distribute(180, s, [d1, d2], new_tip='never')

    # transfer 3022 (100 conc)
    map_384_B1 = [well for plate in ctrl_plates
                  for well in plate.columns()[0][1:8:2]]
    map_384_J23 = [well for plate in ctrl_plates
                   for well in plate.columns()[22][9::2]]
    for s, d1, d2 in zip(master_block.columns()[1][:4]*3,
                         map_384_B1, map_384_J23):
        p1000.distribute(180, s, [d1, d2], new_tip='never')
    p1000.drop_tip()

    # transfer mAb45 (300 & 100 conc)
    map_384_A2 = [well for plate in ctrl_plates
                  for well in plate.columns()[1][0:4:2]]
    map_384_L24 = [well for plate in ctrl_plates
                   for well in plate.columns()[23][11:15:2]]
    p1000.pick_up_tip()
    for s, d1, d2 in zip(master_block.columns()[2][:2]*3,
                         map_384_A2, map_384_L24):
        p1000.distribute(180, s, [d1, d2], new_tip='never')
