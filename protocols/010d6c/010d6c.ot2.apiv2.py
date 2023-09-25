metadata = {
    'protocolName': 'Ribogreen Assay',
    'author': 'Rami Farawi <rami.farawi@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.14'
}


def run(ctx):

    [csv_samp, plate_standard, diluent_buff_col,
        duplicate_plating, m300_mount, p300_mount] = get_values(  # noqa: F821
        "csv_samp", "plate_standard", "diluent_buff_col",
            "duplicate_plating", "m300_mount", "p300_mount")

    # p300_mount = 'left'
    # m300_mount = 'right'
    # plate_standard = True
    # diluent_buff_col = 4
    # duplicate_plating = False
    # csv_samp = """
    #
    # source slot, source well, dest well
    # 7, A1, A1
    # 8, A1, A2
    # 7, A3, A3
    #
    # """

    # labware
    reservoir = ctx.load_labware('corning_12_reservoir', 2)
    try:
        heater_shaker = ctx.load_module('heaterShakerModuleV1', 6)
        heater_shaker.close_labware_latch()
        hs_plate = heater_shaker.load_labware('nunc_96_wellplate_400ul')
    except ModuleNotFoundError:
        hs_plate = heater_shaker.load_labware('nunc_96_wellplate_400ul')

    deep_plate = ctx.load_labware('pyramid_96_wellplate_2000ul', 4)
    tuberack_15 = ctx.load_labware('opentrons_15_tuberack_5000ul', 7)
    tuberack_24 = ctx.load_labware('opentrons_24_tuberack_nest_2ml_snapcap', 8)
    tuberack_24 = tuberack_24

    tips = [ctx.load_labware('opentrons_96_tiprack_300ul', slot)
            for slot in [1]]

    # pipettes
    p300 = ctx.load_instrument('p300_single_gen2', p300_mount, tip_racks=tips)
    m300 = ctx.load_instrument('p300_multi_gen2', m300_mount, tip_racks=tips)

    csv_lines = [[val.strip() for val in line.split(',')]
                 for line in csv_samp.splitlines()
                 if line.split(',')[0].strip()][1:]

    # mapping
    matrix_buff = reservoir.wells_by_name()['A1']
    triton = reservoir.wells_by_name()['A3']
    te = reservoir.wells_by_name()['A5']
    dye = reservoir.wells_by_name()['A7']
    calibration_solution = tuberack_15.wells()[0]

    # protocol
    diluent_buff_col = deep_plate.columns()[diluent_buff_col-1]
    if plate_standard:
        ctx.comment('\n------------ADDING BUFFER TO PLATE------------\n\n')
        buffer_vols = [0, 250, 500, 750, 900, 950, 980, 1000]
        p300.pick_up_tip()
        p300.mix(1, 300, matrix_buff)
        for vol, well in zip(buffer_vols, diluent_buff_col):
            if vol == 0:
                continue
            p300.transfer(vol, matrix_buff, well, new_tip='never')
        p300.drop_tip()

        ctx.comment('\n------------ADDING CALIBRATION------------\n\n')
        calibration_vols = [1000, 750, 500, 250, 100, 50, 20, 0]

        for vol, well in zip(calibration_vols, diluent_buff_col):
            if vol == 0:
                continue
            p300.pick_up_tip()
            p300.mix(1, 300, matrix_buff)
            p300.transfer(vol, calibration_solution, well.top(),
                          new_tip='never')
            p300.drop_tip()

    if duplicate_plating:
        ctx.comment('\n------------DUPLICATE PLATING------------\n\n')
        dispense_wells = [hs_plate.wells_by_name()[well]
                          for well in ['A1', 'A2', 'A11', 'A12']]
        source_col = diluent_buff_col[0]
        m300.pick_up_tip()
        m300.aspirate(220, source_col)
        for well in dispense_wells:
            m300.dispense(50, well)
        m300.drop_tip()

    else:
        ctx.comment('\n------------TRIPLICATE PLATING------------\n\n')
        dispense_wells = [hs_plate.wells_by_name()[well]
                          for well in ['A1', 'A2', 'A3', 'A10', 'A11', 'A12']]
        source_col = diluent_buff_col[0]
        m300.pick_up_tip()
        m300.aspirate(300, source_col)
        for well in dispense_wells:
            m300.dispense(50, well)
        m300.drop_tip()

    ctx.comment('\n------------ADDING SAMPLE------------\n\n')
    for line in csv_lines:
        csv_slot = int(line[0])

        csv_well = line[1]
        source_well = ctx.loaded_labwares[csv_slot].wells_by_name()[csv_well]
        dest_well = line[2]
        p300.pick_up_tip()
        p300.aspirate(50, source_well)
        p300.dispense(50, hs_plate.wells_by_name()[dest_well])
        p300.drop_tip()

    ctx.comment('\n------------PLATING TRITON------------\n\n')
    m300.flow_rate.dispense = 200
    dispense_wells = hs_plate.rows()[0][:6]
    m300.pick_up_tip()
    m300.mix(1, 300, triton)
    m300.aspirate(300, triton)
    for well in dispense_wells:
        m300.dispense(50, well.top())
    m300.drop_tip()

    ctx.comment('\n------------PLATING TE------------\n\n')
    dispense_wells = hs_plate.rows()[0][6:]
    m300.pick_up_tip()
    m300.mix(1, 300, te)
    m300.aspirate(300, te)
    for well in dispense_wells:
        m300.dispense(50, well.top())
    m300.drop_tip()

    try:
        heater_shaker.set_and_wait_for_temperature(37)
        ctx.delay(minutes=10)
        heater_shaker.deactivate_heater()
    except ModuleNotFoundError:
        ctx.delay(minutes=10)

    ctx.comment('\n------------PLATING DYE------------\n\n')

    m300.pick_up_tip()
    m300.mix(1, 300, te)

    for _ in range(2):
        m300.distribute(50, dye, [well.top() for well in hs_plate.rows()[0]],
                        new_tip='never')

    m300.drop_tip()

    ctx.pause('''
    Plate is ready! Please remove, seal and transport to the plate reader for
    analysis. Please remember to tidy the robot deck and dispose of any waste.
    ''')
