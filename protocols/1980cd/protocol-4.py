metadata={"apiLevel": "2.5"}

def run(ctx):

    tip_rack = [ctx.load_labware('opentrons_96_filtertiprack_200ul', x) for x in ['7','8']]
    p300m = ctx.load_instrument('p300_multi_gen2', "right", tip_racks=tip_rack)

    test_plate_1 = ctx.load_labware('nest_96_wellplate_200ul_flat', '5')
    test_plate_2 = ctx.load_labware('nest_96_wellplate_200ul_flat', '6')

    read_buffer = ctx.load_labware('nest_1_reservoir_195ml','4').wells()[0]

    for plate in [test_plate_1, test_plate_2]:
        for col in plate.rows()[0]:
            p300m.transfer(150, read_buffer, col)
