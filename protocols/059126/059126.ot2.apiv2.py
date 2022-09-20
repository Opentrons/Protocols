"""OPENTRONS."""
from opentrons import protocol_api

metadata = {
    'protocolName': 'Reagent Addition',
    'author': 'John C. Lynch <john.lynch@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.11'
}


def run(ctx: protocol_api.ProtocolContext):
    """PROTOCOL."""
    [
     num_384_cols,
     starting_tip_col,
     m20_mount,
     file_input
    ] = get_values(  # noqa: F821 (<--- DO NOT REMOVE!)
        "num_384_cols",
        "starting_tip_col",
        "m20_mount",
        "file_input")

    # define all custom variables above here with descriptions:
    if m20_mount == 'right':
        m300_mount = 'left'
    else:
        m300_mount = 'right'

    # load labware

    plate_96 = ctx.load_labware('greiner_96_wellplate_340ul', '1')
    plate_384 = ctx.load_labware('greiner_384_wellplate_50ul', '2')
    vials = ctx.load_labware('cytiva_24_wellplate_2000ul', '7')

    # load tipracks
    tiprack_300 = [ctx.load_labware('opentrons_96_tiprack_300ul', slot)
                   for slot in '8']
    tiprack_20 = [ctx.load_labware('opentrons_96_tiprack_20ul', slot)
                  for slot in '9']

    # List Creation
    csv_1 = file_input.split('\\n')
    csv_2 = [val.split(',') for val in csv_1]
    header_removed = csv_2[1:]
    flattened_list = [item for sublist in header_removed
                      for item in sublist]
    well_list = flattened_list[::3]
    vol_trans_96 = [eval(i) for i in flattened_list[1::3]]
    vol_trans_384 = [eval(i) for i in flattened_list[2::3]]

    # Tip Logic
    starting_tip = 8*starting_tip_col
    final_tip = starting_tip-len(well_list)
    single_tip_loc = tiprack_300[0].wells()[final_tip:starting_tip][::-1]
    if final_tip < 0:
        raise Exception('Invalid starting tip column for specified number of'
                        ' vials. Not enough tips.')

    # load instrument
    m20 = ctx.load_instrument('p20_multi_gen2', m20_mount,
                              tip_racks=tiprack_20)
    m300 = ctx.load_instrument('p300_multi_gen2', m300_mount,
                               tip_racks=tiprack_300)

    # reagents
    row_a_384 = plate_384.rows()[0][:num_384_cols]
    row_b_384 = plate_384.rows()[1][:num_384_cols]
    vial_list = []
    vial_list.append(well_list)
    plate_96_cols = plate_96.rows()[0][:len(well_list)]
    rows_384 = [row_a_384, row_b_384]

    pre_air_gap = 5
    # BEGIN PROTOCOL

    # Transfer to 96 Plate
    ctx.comment('\n\n~~~~~~~~~~~~~~ADDING TO 96 WELL PLATE~~~~~~~~~~~~~~\n\n')
    for i, (tip, well, vol) in enumerate(zip(single_tip_loc,
                                         vial_list[0], vol_trans_96)):
        m300.pick_up_tip(tip)
        for dest in plate_96.columns()[i][:8]:
            m300.aspirate(vol, vials.wells_by_name()[well], rate=0.5)
            m300.dispense(vol, dest, rate=0.5)
        m300.drop_tip()

    # Transfer to 384 Well Plate
    ctx.comment('\n\n~~~~~~~~~~~~~~ADDING TO 384 WELL PLATE~~~~~~~~~~~~~~\n\n')
    for src, vol in zip(plate_96_cols, vol_trans_384):
        m20.pick_up_tip()
        for plate_384 in rows_384:
            for i, dest in enumerate(plate_384):
                if i == 0:
                    m20.aspirate(pre_air_gap, src.top())
                m20.aspirate(vol, src, rate=0.5)
                m20.dispense(vol+pre_air_gap, dest.top(), rate=2)
                m20.aspirate(pre_air_gap, src.top())
        m20.drop_tip()

    for c in ctx.commands():
        print(c)
