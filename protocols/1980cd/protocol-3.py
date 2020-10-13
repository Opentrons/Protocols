metadata={"apiLevel": "2.5"}

def run(ctx):

    tip_rack = [ctx.load_labware('opentrons_96_filtertiprack_200ul', x) for x in ['7','8']]
    p300m = ctx.load_instrument('p300_multi_gen2', "right", tip_racks=tip_rack)

    test_plate_1 = ctx.load_labware('nest_96_wellplate_200ul_flat', '5')
    test_plate_2 = ctx.load_labware('nest_96_wellplate_200ul_flat', '6')

    reagents = ctx.load_labware('nest_12_reservoir_15ml', '4')
    detection_antibody = reagents.wells_by_name()["A1"]

    for plate in [test_plate_1, test_plate_2]:
        for col in plate.rows()[0]:
            p300m.transfer(25, detection_antibody, col)
