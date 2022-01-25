from opentrons import protocol_api


metadata = {
    'protocolName': 'RNA Normalization I & II',
    'author': 'Rami Farawi <rami.farawi@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.11'
}


def run(ctx: protocol_api.ProtocolContext):

    [
     _num_samp,
     _p300_mount,

    ] = get_values(  # noqa: F821 (<--- DO NOT REMOVE!)
        "_num_samp",
        "_p300_mount")

    # VARIABLES

    # number of samples running (not including controls)
    num_samp = _num_samp

    # change pipette mounts here to "left" or "right", respectively
    p300_mount = _p300_mount

    # MODULES
    temp_mod = ctx.load_module('temperature module gen2', '1')
    temp_mod.set_temperature(4)

    # LABWARE
    prl_tuberacks = [ctx.load_labware(
                 'nest_32_tuberack_8x15ml_8x15ml_8x15ml_8x15ml',
                 slot, label='Sample Tuberack')
                 for slot in ['4', '7']]
    plate = temp_mod.load_labware('nest_96_wellplate_100ul_pcr_full_skirt')
    reagent_tuberacks = [ctx.load_labware(
                    'opentrons_24_tuberack_nest_1.5ml_screwcap',
                    slot, label='rack') for slot in ['9', '6', '3']]

    # TIPRACKS
    tipracks = [ctx.load_labware('opentrons_96_filtertiprack_200ul', '10')]

    # INSTRUMENTS
    p300 = ctx.load_instrument('p300_single_gen2', p300_mount,
                               tip_racks=tipracks)

    # MAPPING
    prl_rows = [tube
                for rack in prl_tuberacks
                for row in rack.rows()
                for tube in row][:num_samp]
    reagent_tubes = [tube
                     for rack in reagent_tuberacks
                     for row in rack.rows()
                     for tube in row][6:]
    negative_ctrl = plate.wells()[0]
    neg_ctrl_tube = reagent_tuberacks[0].wells()[0]
    positive_ctrl_1 = plate.wells()[95]
    pos_ctrl_tube = reagent_tuberacks[0].rows()[0][1]
    positive_ctrl_final = plate.wells()[1]
    plate_wells = plate.wells()[2:]

    # protocol
    ctx.comment('\n\nMOVING NEGATIVE CONTROL TO PLATE\n')
    p300.pick_up_tip()
    p300.aspirate(50, neg_ctrl_tube)
    p300.dispense(30, negative_ctrl.bottom(negative_ctrl.depth/2))
    p300.dispense(20, negative_ctrl)
    p300.mix(5, 40, negative_ctrl)
    p300.drop_tip()

    ctx.comment('\n\nMOVING SAMPLEs TO PLATE\n')
    for prl_source, dest1, final_dest in zip(prl_rows,
                                             reagent_tubes,
                                             plate_wells):
        p300.pick_up_tip()
        p300.aspirate(50, prl_source)
        p300.dispense(50, dest1)
        p300.mix(3, 200, dest1)
        p300.aspirate(50, dest1)
        p300.dispense(30, final_dest.bottom(final_dest.depth/2))
        p300.dispense(20, final_dest)
        p300.mix(3, 40, final_dest)
        p300.drop_tip()
        ctx.comment('\n')

    ctx.comment('\n\nMOVING POSITIVE CONTROL TO PLATE\n')
    p300.pick_up_tip()
    p300.aspirate(50, pos_ctrl_tube)
    p300.dispense(30, positive_ctrl_1.bottom(positive_ctrl_1.depth/2))
    p300.dispense(20, positive_ctrl_1)
    p300.mix(5, 40, positive_ctrl_1)

    p300.aspirate(50, positive_ctrl_1)
    p300.dispense(30, positive_ctrl_final.bottom(positive_ctrl_1.depth/2))
    p300.dispense(20, positive_ctrl_final)
    p300.mix(5, 40, positive_ctrl_final)
    p300.drop_tip()
