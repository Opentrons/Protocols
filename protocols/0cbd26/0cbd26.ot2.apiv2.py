metadata = {
    'protocolName': 'CGE Buffer Load',
    'author': 'Rami Farawi <rami.farawi@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.13'
}


def run(ctx):

    [csv_samp, num_source_racks,
        num_dest_racks, p1000_mount] = get_values(  # noqa: F821
        "csv_samp", "num_source_racks",
            "num_dest_racks", "p1000_mount")

    # labware
    dest_racks = [ctx.load_labware('cgev2_36_tuberack_2000ul', slot)
                  for slot in [4, 5, 6][:num_dest_racks]]
    source_racks = [
                    ctx.load_labware(
                                    'opentrons_6_tuberack_falcon_50ml_conical',
                                    slot)
                    for slot in [1, 2, 3][:num_source_racks]]

    print(dest_racks, source_racks)
    tips = [ctx.load_labware('opentrons_96_tiprack_1000ul', slot)
            for slot in [10]]

    # pipettes
    p1000 = ctx.load_instrument(
                    'p1000_single_gen2', p1000_mount, tip_racks=tips)

    # mapping
    csv_rows = [[val.strip() for val in line.split(',')]
                for line in csv_samp.splitlines()
                if line.split(',')[0].strip()][1:]

    # protocol
    ctx.pause('''Make sure there is not more than a 35mL in the reagent tubes.
    Select resume in the app to continue.''')

    for i, row in enumerate(csv_rows):
        # ctx.comment(f'Row {i+2} in csv')
        change_tip_TF = True if row[1].lower() == 'y' else False
        transfer_vol = int(row[2])
        source_slot = ctx.loaded_labwares[int(row[4])]
        source_well = source_slot.wells_by_name()[row[5]]
        dest_slot = ctx.loaded_labwares[int(row[7])]
        dest_well = dest_slot.wells_by_name()[row[8]]

        # aspirate handling
        asp_flow_rate = int(row[9])
        asp_height = int(row[10])
        asp_delay_TF = True if row[11].lower() == 'y' else False
        asp_delay_time = int(row[12]) if asp_delay_TF else 0
        tip_pos_after_asp_delay_TF = True if len(row[13]) > 0 else False
        asp_touch_tip_TF = True if row[14].lower() == 'y' else False
        asp_airgap_TF = True if row[16].lower() == 'y' else False

        # dispense handling
        disp_flow_rate = int(row[17])
        disp_height = int(row[18])
        disp_delay_TF = True if row[19].lower() == 'y' else False
        disp_delay_time = int(row[20]) if disp_delay_TF else 0
        tip_pos_after_disp_delay_TF = True if len(row[21]) > 0 else False
        disp_touch_tip_TF = True if row[22].lower() == 'y' else False
        disp_blow_out_TF = True if row[24].lower() == 'y' else False
        # disp_airgap_TF = True if row[25].lower() == 'y' else False

        # ------------------------ LIQUID COMMANDS -------------------------

        # set flow rate
        p1000.flow_rate.aspirate = asp_flow_rate
        p1000.flow_rate.dispense = disp_flow_rate

        if transfer_vol <= 900:

            # pick up tip
            if change_tip_TF and p1000.has_tip:
                p1000.drop_tip()
            if change_tip_TF:
                p1000.pick_up_tip()

            # Aspirate
            p1000.aspirate(transfer_vol, source_well.bottom(asp_height))
            if asp_delay_TF:
                ctx.delay(seconds=asp_delay_time)
            if tip_pos_after_asp_delay_TF:
                tip_pos_after_asp_delay = int(row[13])
                p1000.move_to(source_well.bottom(tip_pos_after_asp_delay))
            if asp_touch_tip_TF:
                asp_touch_tip_height = int(row[15])
                p1000.touch_tip(v_offset=-source_well.depth-asp_touch_tip_height)  # noqa: E501
            if asp_airgap_TF:
                p1000.air_gap(100)

            # Dispense
            if asp_airgap_TF:
                p1000.dispense(transfer_vol+100, dest_well.bottom(disp_height))
            else:
                p1000.dispense(transfer_vol, dest_well.bottom(disp_height))
            if disp_delay_TF:
                ctx.delay(seconds=disp_delay_time)
            if tip_pos_after_disp_delay_TF:
                tip_pos_after_disp_delay = int(row[21])
                p1000.move_to(dest_well.bottom(tip_pos_after_disp_delay))
            if disp_touch_tip_TF:
                disp_touch_tip_height = int(row[23])
                p1000.touch_tip(v_offset=-dest_well.depth-disp_touch_tip_height)  # noqa: E501
            if disp_blow_out_TF:
                p1000.blow_out()
            # if disp_airgap_TF:
            #     p1000.air_gap(99)
            ctx.comment('\n\n')

        else:

            transfer_vol_ctr = transfer_vol
            max_aspirate_vol = 900

            # pick up tip
            if change_tip_TF and p1000.has_tip:
                p1000.drop_tip()
            if change_tip_TF:
                p1000.pick_up_tip()

            while transfer_vol_ctr > 0:
                # Aspirate
                pickup_vol = max_aspirate_vol if transfer_vol_ctr > max_aspirate_vol else transfer_vol_ctr  # noqa: E501
                p1000.aspirate(pickup_vol, source_well.bottom(asp_height))
                transfer_vol_ctr -= pickup_vol
                if asp_delay_TF:
                    ctx.delay(seconds=asp_delay_time)
                if tip_pos_after_asp_delay_TF:
                    tip_pos_after_asp_delay = int(row[13])
                    p1000.move_to(source_well.bottom(tip_pos_after_asp_delay))
                if asp_touch_tip_TF:
                    asp_touch_tip_height = int(row[15])
                    p1000.touch_tip(v_offset=-(source_well.depth-asp_touch_tip_height))  # noqa: E501
                if asp_airgap_TF:
                    p1000.air_gap(100)

                # Dispense
                if asp_airgap_TF:
                    p1000.dispense(pickup_vol+100, dest_well.bottom(disp_height))  # noqa: E501
                else:
                    p1000.dispense(pickup_vol, dest_well.bottom(disp_height))
                if disp_delay_TF:
                    ctx.delay(seconds=disp_delay_time)
                if tip_pos_after_disp_delay_TF:
                    tip_pos_after_disp_delay = int(row[21])
                    p1000.move_to(dest_well.bottom(tip_pos_after_disp_delay))
                if disp_touch_tip_TF:
                    disp_touch_tip_height = int(row[23])
                    p1000.touch_tip(v_offset=-(dest_well.depth-disp_touch_tip_height))  # noqa: E501
                if disp_blow_out_TF:
                    p1000.blow_out()
                # if disp_airgap_TF:
                #     p1000.air_gap(99)
            ctx.comment('\n\n')
