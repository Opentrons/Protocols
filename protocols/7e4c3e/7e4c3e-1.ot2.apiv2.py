metadata = {'apiLevel': '2.0'}

def run(ctx):

    column_count = 12

    p20m = ctx.load_instrument('p20_multi_gen2', 'right', tip_racks=[ctx.load_labware("opentrons_96_filtertiprack_20ul", x) for x in ["2","3"]])
    p1000s = ctx.load_instrument('p1000_single_gen2', 'left', tip_racks=[])

    biorad_96_well = ctx.load_labware("opentrons_96_aluminumblock_biorad_wellplate_200ul","4")
    b_cols = biorad_96_well.rows()[0][:column_count]
    #applied_biosystems = ctx.load_labware("appliedbiosystemsmicroampoptical384wellreactionplatewithbarcode_384_wellplate_30ul","5")
    applied_biosystems = ctx.load_labware("hardshellbioradpcr_384_wellplate_50ul", "5")

    applied_wells = [item for sublist in [[[applied_biosystems.wells_by_name()["{}{}".format(a,b+(x*3))] for b in range(1,4)] for a in ["A","B"]] for x in range(0,6)] for item in sublist]
    print(type(applied_biosystems.wells_by_name()["A1"]))
    print(type(applied_biosystems.wells_by_name()["B1"]))
    p20m.transfer(2, b_cols[0], applied_biosystems.wells_by_name()["B1"], new_tip="always")
    for col, target_wells in zip(b_cols, applied_wells):
        p20m.pick_up_tip()
        p20m.aspirate(4.5, col) # Get extra for nice dead volume
        for target_well_num in range(0,2):
            p20m.dispense(2, target_wells[target_well_num])
        p20m.drop_tip()
        print(col)
        print(target_wells[2])
        p20m.transfer(2, col, target_wells[2], new_tip="always")



            


