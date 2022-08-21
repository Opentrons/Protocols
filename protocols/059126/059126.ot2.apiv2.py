"""OPENTRONS."""
from opentrons import protocol_api
import math

metadata = {
    'protocolName': 'Reagent Addition',
    'author': 'John C. Lynch <john.lynch@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.11'
}


def run(ctx: protocol_api.ProtocolContext):
    """PROTOCOL."""
    [
     num_samples,
     vol_transfer,
     num_vials,
     m20_mount
    ] = get_values(  # noqa: F821 (<--- DO NOT REMOVE!)
        "num_samples",
        "vol_transfer",
        "num_vials",
        "m20_mount")

    # define all custom variables above here with descriptions:
    if m20_mount == 'right':
        m300_mount = 'left'
    else:
        m300_mount = 'right'

    num_384_cols = math.ceil(num_samples/16)
    # load labware

    plate_96 = ctx.load_labware('greiner_96_wellplate_340ul', '1')
    plate_384 = ctx.load_labware('greiner_384_wellplate_50ul', '2')
    vials = ctx.load_labware('corning_24_wellplate_3.4ml_flat', '4')

    # load tipracks
    tiprack_300 = [ctx.load_labware('opentrons_96_tiprack_300ul', slot)
                   for slot in '8']
    tiprack_20 = [ctx.load_labware('opentrons_96_tiprack_20ul', slot)
                  for slot in '9']
    single_tip_loc = tiprack_300[0].wells()[:num_vials:-1]

    # load instrument
    m20 = ctx.load_instrument('p20_multi_gen2', m20_mount,
                              tip_racks=tiprack_20)
    m300 = ctx.load_instrument('p300_multi_gen2', m300_mount,
                               tip_racks=tiprack_300)

    # reagents
    row_a_384 = plate_384.rows()[0][:num_384_cols]
    row_b_384 = plate_384.rows()[1][:num_384_cols]
    vial_list = vials.wells()[:num_vials]
    plate_96_cols = plate_96.rows()[0][:num_vials]
    rows_384 = [row_a_384, row_b_384]

    pre_air_gap = 5
    # BEGIN PROTOCOL

    # Transfer to 96 Plate
    ctx.comment('\n\n~~~~~~~~~~~~~~ADDING TO 96 WELL PLATE~~~~~~~~~~~~~~\n\n')
    for i, (tip, src) in enumerate(zip(single_tip_loc, vial_list)):
        m300.pick_up_tip(tip)
        for dest in plate_96.columns()[i][:8]:
            m300.aspirate(150, src, rate=0.5)
            m300.dispense(150, dest, rate=0.5)
        m300.drop_tip()

    # Transfer to 384 Well Plate
    ctx.comment('\n\n~~~~~~~~~~~~~~ADDING TO 384 WELL PLATE~~~~~~~~~~~~~~\n\n')
    for src in plate_96_cols:
        m20.pick_up_tip()
        for plate_384 in rows_384:
            for dest in plate_384:
                m20.aspirate(pre_air_gap, src.top())
                m20.aspirate(vol_transfer, src, rate=0.5)
                m20.dispense(vol_transfer+pre_air_gap, dest.top(), rate=2)
                m20.blow_out()
                m20.touch_tip()
        m20.drop_tip()

    for c in ctx.commands():
        print(c)
