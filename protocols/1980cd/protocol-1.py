metadata={"apiLevel": "2.5"}

def run(ctx):

    tip_rack = [ctx.load_labware('opentrons_96_filtertiprack_200ul', '8')]
    p300m = ctx.load_instrument('p300_multi_gen2', "right", tip_racks=tip_rack)
    trough = ctx.load_labware('nest_1_reservoir_195ml','5').wells()[0]
    # https://www.mesoscale.com/~/media/files/product%20inserts/human%20total%20tau.pdf is
    # not specific with their plate size, but this should roughly be right.
    sample_plate = ctx.load_labware('nest_96_wellplate_200ul_flat', '6') 

    for sample_well in [sample_plate.wells_by_name()[x] for x in ["A1","A2","A3","A4","A5","A8","A9","A10","A11","A12"]]:
        p300m.transfer(150, trough, sample_well)

