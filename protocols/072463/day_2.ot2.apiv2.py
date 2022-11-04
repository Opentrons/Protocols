"""OPENTRONS."""
from opentrons import protocol_api

metadata = {
    'protocolName': 'Day 2',
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
     p300_mount
    ] = get_values(  # noqa: F821 (<--- DO NOT REMOVE!)
        "num_samples",
        "vol_trans",
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
    final_plate = ctx.load_labware('nest_96_wellplate_2ml_deep', '3')
    sample_plate = ctx.load_labware('opentrons_24_tuberack_generic_'
                                    '2ml_screwcap', '6')

    # load tipracks
    tiprack_300 = [ctx.load_labware('opentrons_96_tiprack_300ul', slot)
                   for slot in ['8', '11']]
    tiprack_20 = [ctx.load_labware('opentrons_96_tiprack_20ul', slot)
                  for slot in ['7', '10']]

    # load instrument
    p300 = ctx.load_instrument('p300_single_gen2', p300_mount,
                               tip_racks=tiprack_300)
    p20 = ctx.load_instrument('p20_single_gen2', p20_mount,
                              tip_racks=tiprack_20)
    # chunking

    def div_chunks(len, n):

        for i in range(0, num_samples, n):
            yield len[i:i + n]

    wells_reorder = []
    for sublist in final_plate.rows():
        for item in sublist:
            wells_reorder.append(item)
    # reagents
    std_dest_wells = wells_reorder[num_samples*3:num_samples*3+21]
    dest_list = list(div_chunks(wells_reorder, 3))
    dest_list_std = list(div_chunks(std_dest_wells,
                                    3))
    total_dest = wells_reorder[:num_samples*3+21]
    std_wells = std_plate.wells()[:7]
    reag_a = std_plate.rows()[3][0]
    reag_b = std_plate.rows()[3][1]
    reag_c = std_plate.rows()[3][2]
    water = reagent_resv.wells()[0]
    sample_list = sample_plate.wells()[:num_samples]

    # BEGIN PROTOCOL

    # Transfer X uL from starting vials slot 6 to slot 3 in triplicate
    for i, start in enumerate(sample_list):
        if vol_trans > 20:
            pip = p300
        else:
            pip = p20
        pip.pick_up_tip()
        for lst in dest_list[i]:
            for dest in lst:
                if vol_trans > 20:
                    pip = p300
                else:
                    pip = p20
                pip.aspirate(vol_trans, start, rate=0.5)
                pip.dispense(vol_trans, dest, rate=0.5)
        pip.drop_tip()
    # Transfer 36 uL DI from slot 1 well 1 to all 7 standards in triplicate
    p300.pick_up_tip()
    for dest in std_dest_wells:
        p300.aspirate(36, water)
        p300.dispense(36, dest)
    p300.drop_tip()
    # Same as samples but for standards
    for i, src in enumerate(std_wells):
        if vol_trans > 20:
            pip = p300
        else:
            pip = p20
        pip.pick_up_tip()
        for lst in dest_list_std[i]:
            for dest in lst:
                pip.aspirate(vol_trans, src, rate=0.5)
                pip.dispense(vol_trans, dest, rate=0.5)
                pip.mix(1, vol_trans, dest)
        pip.drop_tip()

    # Wait 1 hour
    ctx.delay(minutes=60)

    # Add 46 uL to samples
    for dest in sample_list:
        p300.pick_up_tip()
        p300.aspirate(46, water)
        p300.dispense(46, dest)
        p300.mix(1, 46, dest)
        p300.drop_tip()
    # Reagent A, add 30 uL to all samples and standards
    for dest in total_dest:
        p300.pick_up_tip()
        p300.aspirate(30, reag_a)
        p300.dispense(30, dest)
        p300.mix(1, 30, dest)
        p300.drop_tip()
    # Turn off temp module

    # 1 hour wait
    ctx.delay(minutes=60)
    # 49 uL Reagent B added to all samples/standards
    for dest in total_dest:
        p300.pick_up_tip()
        p300.aspirate(49, reag_b)
        p300.dispense(49, dest)
        p300.mix(1, 49, dest)
        p300.drop_tip()
    # 75 uL Reagent C added to all samples/standards
    for dest in total_dest:
        p300.pick_up_tip()
        p300.aspirate(75, reag_c)
        p300.dispense(75, dest)
        p300.mix(1, 75, dest)
        p300.drop_tip()

    for c in ctx.commands():
        print(c)
