metadata = {'apiLevel': '2.0'}

def run(ctx):

    column_count = 12

    p20m = ctx.load_instrument('p20_multi_gen2', 'right', tip_racks=[ctx.load_labware("opentrons_96_filtertiprack_20ul", "2")])
    p1000s = ctx.load_instrument('p1000_single_gen2', 'left', tip_racks=[ctx.load_labware("opentrons_96_filtertiprack_1000ul", "1")])

    biorad_96_well = ctx.load_labware("opentrons_96_aluminumblock_biorad_wellplate_200ul","7")
    pcr_strip = ctx.load_labware("opentrons_96_aluminumblock_generic_pcr_strip_200ul", "5")
    master_mix = ctx.load_labware("opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap","4").wells_by_name()["A1"]

    p1000s.transfer(column_count*5, master_mix, pcr_strip.columns()[0], new_tip="once")
    p20m.transfer(3.8, pcr_strip.wells_by_name()["A1"], biorad_96_well.rows()[0][:column_count], new_tip="once")

