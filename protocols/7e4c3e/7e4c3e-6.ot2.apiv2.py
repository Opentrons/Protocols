metadata = {'apiLevel': '2.0'}

def run(ctx):

    column_count = 12

    p20m = ctx.load_instrument('p20_multi_gen2', 'right', tip_racks=[ctx.load_labware("opentrons_96_filtertiprack_20ul", "2")])
    p1000s = ctx.load_instrument('p1000_single_gen2', 'left', tip_racks=[ctx.load_labware("opentrons_96_filtertiprack_1000ul", "1")])

    applied_biosystems_plate = ctx.load_labware("appliedbiosystemsmicroampoptical384wellreactionplatewithbarcode_384_wellplate_30ul", "6")
    tube_rack = ctx.load_labware("opentrons_24_tuberack_eppendorf_2ml_safelock_snapcap", "4")
    pcr_strip = ctx.load_labware("opentrons_96_aluminumblock_generic_pcr_strip_200ul", "5")

    master_mix_1 = tube_rack.wells_by_name()["A1"]
    master_mix_2 = tube_rack.wells_by_name()["B1"]

    p1000s.transfer(

    p1000s.transfer(column_count*5, master_mix, pcr_strip.columns()[0], new_tip="once")
    p20m.transfer(3.8, pcr_strip.wells_by_name()["A1"], biorad_96_well.rows()[0][:column_count], new_tip="once")

