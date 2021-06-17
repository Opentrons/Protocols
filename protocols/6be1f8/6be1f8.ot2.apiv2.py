metadata = {
    'protocolName': 'Sample Prep for ELISA Test',
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
    master_block = ctx.load_labware('greiner_96_wellplate_2000ul', '4')
    tiprack20 = [ctx.load_labware('opentrons_96_tiprack_20ul', '2')]
    tiprack1000 = [ctx.load_labware('opentrons_96_tiprack_1000ul', '1')]

    # load instrument
    p20 = ctx.load_instrument('p20_single_gen2', p20_mount,
                              tip_racks=tiprack20)
    p1000 = ctx.load_instrument('p1000_single_gen2', p1000_mount,
                                tip_racks=tiprack1000)

    # load reagents
    diluent = diluent_tubes.wells()[0]
    mab207 = reagent.rows()[0][1]
    mab210_stock = reagent.rows()[0][0]
    mab210_100_conc = reagent.rows()[1][0]
    mab210_20_conc = reagent.rows()[1][1]
    mab210_2_conc = reagent.rows()[1][2]
    ctrl_plates_one_two = ctrl_plates[:2]
    ctrl_plates_three = ctrl_plates[2]

    # STEP DOWN STOCK
    airgap = 5
    p20.pick_up_tip()
    p20.transfer(55.4, diluent, mab210_100_conc, new_tip='never')
    p20.drop_tip()
    p20.pick_up_tip()
    p20.aspirate(4.6, mab210_stock)
    p20.air_gap(airgap)
    p20.dispense(4.6+airgap, mab210_100_conc)
    p20.blow_out()
    p20.mix(25, 20, mab210_100_conc)  # mixing extra b/c only mixing 1/3 totvol
    p20.drop_tip()

    p1000.pick_up_tip()
    p1000.aspirate(160, diluent)
    p1000.dispense(160, mab210_20_conc)
    p20.pick_up_tip()
    p20.transfer(40, mab210_100_conc, mab210_20_conc, new_tip='never')
    p20.drop_tip()
    p1000.mix(15, 180, mab210_20_conc)
    p1000.blow_out()
    p1000.drop_tip()

    p1000.pick_up_tip()
    p1000.transfer(720, diluent, mab210_2_conc, new_tip='never')
    p20.pick_up_tip()
    p20.transfer(80, mab210_20_conc, mab210_2_conc, new_tip='never')
    p20.drop_tip()
    p1000.mix(15, 700, mab210_2_conc)
    p1000.blow_out()
    p1000.drop_tip()

    # CREATE MASTERBLOCK - 207 PREP

    # add diluent
    volumes = [900, 925, 950, 960, 980,
               980, 990, 990, 995, 995,
               992.5, 987.5, 985, 1000, 1000,
               1000]
    dest_wells = ['A1', 'A2', 'B1', 'B2', 'C1',
                  'G1', 'C2', 'E2', 'D1', 'D2',
                  'E1', 'F1', 'G1', 'G2', 'H1',
                  'H2']

    p1000.pick_up_tip()
    for vols, wellname in zip(volumes, dest_wells):
        p1000.transfer(vols, diluent,
                       master_block.wells_by_name()[wellname].top(),
                       new_tip='never')
    p1000.drop_tip()

    # add 207f
    volumes = [100, 75, 50, 40, 20,
               20, 10, 10, 5, 5,
               7.5, 12.5, 15]
    dest_wells = ['A1', 'A2', 'B1', 'B2', 'C1',
                  'G1', 'C2', 'E2', 'D1', 'D2',
                  'E1', 'F1', 'G1']

    for vols, wellname in zip(volumes, dest_wells):
        if vols < 100:
            pip = p20
        else:
            pip = p1000
        if not pip.has_tip:
            pip.pick_up_tip()
        pip.transfer(vols, mab207,
                     master_block.wells_by_name()[wellname].top(),
                     new_tip='never')

    p1000.drop_tip()
    p20.drop_tip()

    for well in master_block.wells()[:16]:
        p1000.pick_up_tip()
        p1000.mix(15, 800, well)
        p1000.drop_tip()

    # CREATE MASTERBLOCK - 210 PREP
    p1000.pick_up_tip()
    vols_dil = [1700, 1850, 1900, 1920, 1940, 1970, 1985, 1990]
    for wells, vol in zip(master_block.columns()[2], vols_dil):
        p1000.transfer(vol, diluent,
                       wells.top(), new_tip='never')
    p1000.drop_tip()

    p1000.pick_up_tip()
    vols_mab = [300, 150, 100, 80, 60, 30, 15, 10]
    for wells, vol in zip(master_block.columns()[2], vols_mab):
        p1000.transfer(vol, mab210_2_conc,
                       wells.top(), new_tip='never')
    p1000.drop_tip()
    for wells in master_block.columns()[2]:
        p1000.pick_up_tip()
        p1000.mix(15, 1000, well)
        p1000.drop_tip()

    # TRANSFER TO 384
    row_start = 0
    for i in range(4):
        for plate in ctrl_plates_one_two:
            for s, d in zip(master_block.columns()[i if i <= 2 else 2],
                            plate.wells()[row_start
                            if i < 2 else row_start+16:32:2]):
                p1000.pick_up_tip()
                p1000.transfer(180, s, d.top(z=3), new_tip='never')
                p1000.drop_tip()
        ctx.comment('\n\n')

        for s, d in zip(master_block.columns()[i if i <= 2 else 2],
                        ctrl_plates_three.wells()[row_start
                        if i < 2 else row_start+16:32:2]):
            p20.pick_up_tip()
            p20.transfer(80, s, d.top(z=3), new_tip='never')
            p20.drop_tip()
        row_start += 1 if row_start == 0 else -1
        ctx.comment('\n\n\n\n\n')
