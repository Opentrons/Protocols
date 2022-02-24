from opentrons import protocol_api

metadata = {
    'protocolName': 'Bioanalysis with CSV input',
    'author': 'Rami Farawi <rami.farawi@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.11'
}


def run(ctx: protocol_api.ProtocolContext):

    [
     _csv,
     _p1000_mount,
     _p20_mount
    ] = get_values(  # noqa: F821 (<--- DO NOT REMOVE!)
        "_csv",
        "_p1000_mount",
        "_p20_mount")

    # VARIABLES
    csv = _csv
    p20_mount = _p20_mount
    p1000_mount = _p1000_mount

    # LABWARE
    tuberacks = [ctx.load_labware(
                 'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
                 slot, label='Sample Tuberack')
                 for slot in ['1', '2', '4']]
    reagent_rack = ctx.load_labware(
                'opentrons_10_tuberack_falcon_4x50ml_6x15ml_conical', '3')

    # TIPRACKS
    tiprack20 = [ctx.load_labware('opentrons_96_filtertiprack_20ul', slot)
                 for slot in ['8', '11']]
    tiprack1000 = [ctx.load_labware('opentrons_96_tiprack_1000ul', slot)
                   for slot in ['10']]

    # INSTRUMENTS
    p20 = ctx.load_instrument('p20_single_gen2',
                              p20_mount,
                              tip_racks=tiprack20)
    p1000 = ctx.load_instrument('p1000_single_gen2',
                                p1000_mount,
                                tip_racks=tiprack1000)

    csv_rows = [[val.strip() for val in line.split(',')]
                for line in csv.splitlines()
                if line.split(',')[0].strip()][1:]
    print(tuberacks, reagent_rack)
    p20.flow_rate.aspirate = 0.75*p20.flow_rate.aspirate
    p20.flow_rate.dispense = 0.75*p20.flow_rate.dispense
    p1000.flow_rate.aspirate = 0.75*p1000.flow_rate.aspirate
    p1000.flow_rate.dispense = 0.75*p1000.flow_rate.dispense

    # protocol
    for row in csv_rows:
        tube_type, source_slot, source_well, transfer_vol, dest_slot, dest_well = row[1:7]  # noqa: E501
        if int(transfer_vol) > 100:
            pip = p1000
        else:
            pip = p20
        source = ctx.loaded_labwares[int(source_slot)].wells_by_name()[
                                        source_well]
        dest = ctx.loaded_labwares[int(dest_slot)].wells_by_name()[
                                        dest_well]

        if "falcon" and "50" in tube_type.lower():
            asp_height = 48

        elif pip == p20 and "15" in tube_type.lower():
            asp_height = 30
        else:
            asp_height = 1

        print(asp_height)

        pip.pick_up_tip()
        pip.transfer(int(transfer_vol),
                     source.bottom(z=asp_height),
                     dest.top(),
                     blowout_location='destination well',
                     air_gap=5,
                     touch_tip=True,
                     new_tip='never')
        pip.blow_out()
        pip.drop_tip()
        ctx.comment('\n')
