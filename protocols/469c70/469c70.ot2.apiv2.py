import math


metadata = {
    'protocolName': 'Serial Dilution of Analyte Stock',
    'author': 'Rami Farawi <rami.farawi@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.11'
}


def run(ctx):

    [csv, num_tipracks, num_tipracks20, num_mix, asp_rate, disp_rate,
        blowout_rate, p1000_mount, p20_mount] = get_values(  # noqa: F821
        "csv", "num_tipracks", "num_tipracks20", "num_mix",
        "asp_rate", "disp_rate",
            "blowout_rate", "p1000_mount", "p20_mount")

    list_of_rows = [[val.strip() for val in line.split(',')]
                    for line in csv.splitlines()
                    if line.split(',')[0].strip()][1:]

    rack_type = 0
    slot_num_source = 1
    tube_source = 2
    init_vol_tracking = 4
    transfer_vol = 5
    slot_num_dest = 6
    dispense_height = 7
    tube_dest = 8

    slots_15 = []
    slots_24 = []
    for the in list_of_rows:
        if the[rack_type] == "24":
            slots_24.append(the[slot_num_source])

        elif the[rack_type] == "15":
            slots_15.append(the[slot_num_source])

    slots_15 = list(set(slots_15))
    slots_24 = list(set(slots_24))

    # load labware
    racks_15 = [ctx.load_labware(
                    'opentrons_15_tuberack_falcon_15ml_conical',
                    slot, label='SERIAL RACK') for slot in slots_15]
    diluent_labware = ctx.load_labware('nest_1_reservoir_195ml', '3',
                                       label='DILUTION RESERVOIR')
    racks_24 = [ctx.load_labware(
        'opentrons_24_tuberack_eppendorf_2ml_safelock_snapcap', slot,
        label='STOCK RACK') for slot in slots_24]

    tiprack1 = [ctx.load_labware('opentrons_96_tiprack_1000ul', slot)
                for slot in ['6', '9', '11'][:int(num_tipracks)]]

    tiprack20 = [ctx.load_labware('opentrons_96_tiprack_20ul', slot)
                 for slot in ['8', '10'][:int(num_tipracks20)]]

    # load instrument
    p1000 = ctx.load_instrument('p1000_single_gen2', p1000_mount,
                                tip_racks=tiprack1)
    p20 = ctx.load_instrument('p20_single_gen2', p20_mount,
                              tip_racks=tiprack20)

    asp_rate = float(asp_rate)
    disp_rate = float(disp_rate)
    blowout_rate = float(blowout_rate)
    num_mix = int(num_mix)
    print(racks_15, diluent_labware, racks_24)

    p1000.flow_rate.aspirate = p1000.flow_rate.aspirate*asp_rate
    p1000.flow_rate.dispense = p1000.flow_rate.dispense*disp_rate
    p1000.flow_rate.blow_out = p1000.flow_rate.blow_out*blowout_rate
    p20.flow_rate.aspirate = p20.flow_rate.aspirate*asp_rate
    p20.flow_rate.dispense = p20.flow_rate.dispense*disp_rate
    p20.flow_rate.blow_out = p20.flow_rate.blow_out*blowout_rate

    for the in list_of_rows:

        # source and dest
        source_labware = ctx.loaded_labwares[int(the[slot_num_source])]
        dest_labware = ctx.loaded_labwares[int(the[slot_num_dest])]

        # height tracking
        if the[slot_num_source] in slots_15 or \
                the[slot_num_source] in slots_24:
            v_naught = float(the[init_vol_tracking])*1000
            radius = source_labware.wells()[0].diameter/2
            h = v_naught/(math.pi*radius**2)*0.6
            check_height = 0.5*source_labware.wells()[0].depth
            asp_loc_z = h if h > check_height else 1

        # transfer
        if str(the[slot_num_source]) in slots_15:
            source_well = the[tube_source]
            asp_height = asp_loc_z
        elif str(the[slot_num_source]) in slots_24:
            source_well = the[tube_source]
            asp_height = asp_loc_z
        else:
            if int(the[slot_num_source]) == 3:
                source_well = 'A1'
            else:
                source_well = the[tube_source]
            asp_height = 1

        # variables
        transfer_volume = float(the[transfer_vol])*1000
        source = source_labware.wells_by_name()[source_well]
        dest = dest_labware.wells_by_name()[the[tube_dest]]
        if the[dispense_height].lower() == "top":
            final_dest = dest.top()
        elif the[dispense_height].lower() == "middle":
            final_dest = dest.bottom(0.5*dest.depth)
        else:
            final_dest = dest.bottom(z=1)

        if transfer_volume > 100:
            pip = p1000
        else:
            pip = p20
        pip.pick_up_tip()
        pip.transfer(transfer_volume,
                     source.bottom(asp_height),
                     final_dest,
                     new_tip='never',
                     blow_out=True,
                     blowout_location='destination well')
        if str(the[slot_num_source]) == "3" and \
                pip == ctx.loaded_instruments[p1000_mount]:
            pip.mix(num_mix,
                    0.6*transfer_volume
                    if 0.6*transfer_volume*1000 < 1000 else 1000,
                    final_dest)
        pip.drop_tip()
        ctx.comment('\n\n')
