
metadata={"apiLevel": "2.5"}

def run(ctx):

    tip_rack = [ctx.load_labware('opentrons_96_filtertiprack_200ul', '8')]
    p300m = ctx.load_instrument('p300_multi_gen2', "right", tip_racks=tip_rack)

    sample_plate = ctx.load_labware('nest_96_wellplate_200ul_flat', '5')
    test_plate_1 = ctx.load_labware('nest_96_wellplate_200ul_flat', '9')
    test_plate_2 = ctx.load_labware('nest_96_wellplate_200ul_flat', '6')

    reagents = ctx.load_labware('nest_12_reservoir_15ml', '3')
    control_1 = reagents.wells_by_name()["A1"]
    control_2 = reagents.wells_by_name()["A2"]

    for control, well in [(control_1,"A1"), (control_2,"A2")]:
        p300m.pick_up_tip()
        for transfer_well in [test_plate_1.wells_by_name()[well], test_plate_2.wells_by_name()[well]]:
            p300m.transfer(150, control, transfer_well, new_tip='never')
        p300m.drop_tip()

    for test_plate, well_list in [(test_plate_1, ["A1","A2","A3","A4","A5"]),(test_plate_2, ["A8","A9","A10","A11","A12"])]:
        for i,from_well in enumerate([sample_plate.wells_by_name()[well] for well in well_list]):
            p300m.pick_up_tip()
            for destination in [test_plate.columns()[col] for col in range(2+(i*2),4+(i*2))]:
                p300m.transfer(150, from_well, destination, new_tip='never')
            p300m.drop_tip()


