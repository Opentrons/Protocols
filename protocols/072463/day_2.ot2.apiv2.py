"""OPENTRONS."""
from opentrons import protocol_api

metadata = {
    'protocolName': 'Day 2 Procedure',
    'author': 'Opentrons <protocols@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.11'   # CHECK IF YOUR API LEVEL HERE IS UP TO DATE
                         # IN SECTION 5.2 OF THE APIV2 "VERSIONING"
}


def run(ctx: protocol_api.ProtocolContext):
    """PROTOCOL."""
    [
     num_samples,
     vol_trans,
     temp_boolean,
     p300_mount
    ] = get_values(  # noqa: F821 (<--- DO NOT REMOVE!)
        "num_samples",
        "vol_trans",
        "temp_boolean",
        "p300_mount")

    # define all custom variables above here with descriptions:
    if p300_mount == 'left':
        p20_mount = 'right'
    else:
        p20_mount = 'left'

    # load modules

    # load labware
    reagent_resv = ctx.load_labware('nest_12_reservoir_15ml', '1')
    std_plate = ctx.load_labware('opentrons_24_tuberack_generic_2ml_screwcap',
                                 '2')
    if temp_boolean:
        temp_mod = ctx.load_module('temperature module gen2', '3')
        temp_mod.set_temperature(95)
        final_plate = temp_mod.load_labware('zinsser_96_wellplate_1898ul')
    else:
        final_plate = ctx.load_labware('zinsser_96_wellplate_1898ul')
    sample_plate = ctx.load_labware('opentrons_24_tuberack_generic_'
                                    '2ml_screwcap', '6')
    if vol_trans < 20:
        tip_rack_list_300 = ['8', '9', '10', '11']
        tip_rack_list_20 = ['4', '7']
    else:
        tip_rack_list_300 = ['7', '8', '9', '10', '11']
        tip_rack_list_20 = ['4']
    # load tipracks
    tiprack_300 = [ctx.load_labware('opentrons_96_tiprack_300ul', slot)
                   for slot in tip_rack_list_300]
    tiprack_20 = [ctx.load_labware('opentrons_96_tiprack_20ul', slot)
                  for slot in tip_rack_list_20]

    # load instrument
    p300 = ctx.load_instrument('p300_single_gen2', p300_mount,
                               tip_racks=tiprack_300)
    p20 = ctx.load_instrument('p20_single_gen2', p20_mount,
                              tip_racks=tiprack_20)
    # chunking

    def div_chunks(len, how_many, n):

        for i in range(0, how_many, n):
            yield len[i:i + n]

    wells_reorder = []
    for sublist in final_plate.rows():
        for item in sublist:
            wells_reorder.append(item)
    # reagents
    std_dest_wells = wells_reorder[num_samples*3:num_samples*3+21]
    dest_list = list(div_chunks(wells_reorder, 96, 3))
    total_dest = wells_reorder[:num_samples*3+21]
    std_wells = std_plate.wells()[:7]
    water = reagent_resv.wells()[0]
    reag_a = reagent_resv.wells()[1]
    reag_b = reagent_resv.wells()[2]
    reag_c = reagent_resv.wells()[3]
    # reag_a = std_plate.rows()[3][0]
    # reag_b = std_plate.rows()[3][1]
    # reag_c = std_plate.rows()[3][2]
    sample_list = sample_plate.wells()[:num_samples]

    # BEGIN PROTOCOL

    # Transfer X uL from starting vials slot 6 to slot 3 in triplicate
    ctx.comment("\n~~~~~ADDING SAMPLES TO 96 WELL PLATE~~~~~\n\n")
    for i, start in enumerate(sample_list):
        if vol_trans > 20:
            pip = p300
        else:
            pip = p20
        pip.pick_up_tip()
        for dest in dest_list[i]:
            pip.aspirate(vol_trans, start, rate=0.5)
            pip.dispense(vol_trans, dest, rate=0.5)
        pip.drop_tip()

    # Transfer 36 uL DI from slot 1 well 1 to all 7 standards in triplicate
    ctx.comment("\n\n~~~~~~ADDING DI WATER TO FUTURE STANDARD WELLS~~~~~~\n\n")
    p300.pick_up_tip()
    for dest in std_dest_wells:
        p300.aspirate(36, water)
        p300.dispense(36, dest)
    p300.drop_tip()

    # Same as samples but for standards
    ctx.comment("\n~~~~~ADDING STANDARDS TO 96 WELL PLATE~~~~~\n\n")
    for i, src in enumerate(std_wells):
        if vol_trans > 20:
            pip = p300
        else:
            pip = p20
        pip.pick_up_tip()
        for dest in dest_list[num_samples+i]:
            pip.aspirate(vol_trans, src, rate=0.5)
            pip.dispense(vol_trans, dest, rate=0.5)
        pip.drop_tip()

    # Wait 1 hour
    if temp_boolean:
        temp_mod.set_temperature(95)
    ctx.delay(minutes=60)

    # Add 46 uL to samples
    ctx.comment("\n~~~~~ADDING 46 uL DI WATER TO 96 WELL PLATE~~~~~\n\n")
    for dest in sample_list:
        p300.pick_up_tip()
        p300.aspirate(46, water)
        p300.dispense(46, dest)
        p300.mix(1, 46, dest)
        p300.drop_tip()
    # Reagent A, add 30 uL to all samples and standards
    ctx.comment("\n~~~~~ADDING REAGENT A TO 96 WELL PLATE~~~~~\n\n")
    for dest in total_dest:
        p300.pick_up_tip()
        p300.aspirate(30, reag_a, rate=0.5)
        p300.dispense(30, dest)
        p300.mix(1, 30, dest)
        p300.drop_tip()
    # Turn off temp module

    # 1 hour wait
    ctx.delay(minutes=60)
    # 49 uL Reagent B added to all samples/standards
    ctx.comment("\n~~~~~ADDING REAGENT B TO 96 WELL PLATE~~~~~\n\n")
    for dest in total_dest:
        p300.pick_up_tip()
        p300.aspirate(49, reag_b, rate=0.5)
        p300.dispense(49, dest)
        p300.mix(1, 49, dest)
        p300.drop_tip()
    # 75 uL Reagent C added to all samples/standards
    ctx.comment("\n~~~~~ADDING REAGENT C TO 96 WELL PLATE~~~~~\n\n")
    for dest in total_dest:
        p300.pick_up_tip()
        p300.aspirate(75, reag_c, rate=0.5)
        p300.dispense(75, dest)
        p300.mix(1, 75, dest)
        p300.drop_tip()

    for c in ctx.commands():
        print(c)
    # print(dest_list)
