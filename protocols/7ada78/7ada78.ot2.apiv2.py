from opentrons import protocol_api

metadata = {
    'protocolName': 'RNA Quantitation',
    'author': 'Rami Farawi <rami.farawi@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.11'
}


def run(ctx: protocol_api.ProtocolContext):

    [
     _csv,
     _p20_mount
    ] = get_values(  # noqa: F821 (<--- DO NOT REMOVE!)
        "_csv",
        "_p20_mount")

    # VARIABLES
    csv = _csv
    p20_mount = _p20_mount

    # MODULES
    thermocyc = ctx.load_module('thermocycler')

    # LABWARE
    tuberacks = [ctx.load_labware(
                 'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
                 slot, label='Sample Tuberack')
                 for slot in ['1', '2', '4', '5']]
    tc_plate = thermocyc.load_labware('nest_96_wellplate_100ul_pcr_full_skirt')
    dest_plate = ctx.load_labware('optiplate_96_wellplate_400ul',
                                  '3', label='Optiplate')

    # TIPRACKS
    tipracks = [ctx.load_labware('opentrons_96_filtertiprack_20ul', slot)
                for slot in ['6', '9']]

    # INSTRUMENTS
    p20 = ctx.load_instrument('p20_single_gen2', p20_mount, tip_racks=tipracks)

    def pre_wet(vol, well):
        ctx.comment('PRE-WET')
        p20.aspirate(vol, well, rate=0.5)
        p20.dispense(vol, well, rate=0.5)
        ctx.comment('DONE PRE-WET')

    # MAPPING
    slot_source = 0
    source_well = 1
    transfer_vol = 3
    slot_dest = 4
    dest_well = 5

    all_rows = [[val.strip() for val in line.split(',')]
                for line in csv.splitlines()
                if line.split(',')[0].strip()][1:]

    print(tuberacks, tc_plate, dest_plate)
    if thermocyc.lid_position != 'open':
        thermocyc.open_lid()

    # protocol

    ctx.comment('\n\nMOVING SAMPLES TO PLATE\n')

    for the in all_rows:
        if the[transfer_vol].lower() == 'x':
            continue
        vol = int(the[transfer_vol])
        source = ctx.loaded_labwares[int(the[slot_source])].wells_by_name()[
                                        the[source_well]]
        dest = ctx.loaded_labwares[int(the[slot_dest])].wells_by_name()[
                                        the[dest_well]]
        p20.pick_up_tip()
        pre_wet(vol, source)
        p20.aspirate(vol, source)
        p20.dispense(vol, dest)
        p20.drop_tip()
