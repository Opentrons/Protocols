metadata = {
    'protocolName': 'PCR/qPCR prep: distribute primers to 384 well plate',
    'author': 'Steve Plonk <protocols@opentrons.com>',
    'apiLevel': '2.9'
}


def run(ctx):

    # bring in constant values from json string above
    [labware_384_well_plate, n1_primer_well, n1_col, n2_primer_well, n2_col,
     rp_primer_well, rp_col, ntc_primer_well, ntc_col, primer_col_volume,
     primer_volume
     ] = get_values(  # noqa: F821
      'labware_384_well_plate', 'n1_primer_well', 'n1_col', 'n2_primer_well',
      'n2_col', 'rp_primer_well', 'rp_col', 'ntc_primer_well', 'ntc_col',
      'primer_col_volume', 'primer_volume')

    ctx.set_rail_lights(True)

    # p20 multi channel, p300 single channel, tips
    tips20 = [
     ctx.load_labware(
      "opentrons_96_filtertiprack_20ul", slot) for slot in [5, 6, 8, 9]]

    tips300 = [
     ctx.load_labware("opentrons_96_tiprack_300ul", '4')]

    p300s = ctx.load_instrument(
        "p300_single_gen2", 'left', tip_racks=tips300)

    p20m = ctx.load_instrument(
        "p20_multi_gen2", 'right', tip_racks=tips20)

    # source and destination plates
    two_ml_plate = ctx.load_labware("nunc_96_wellplate_2000ul", '1')
    one_ml_plate = ctx.load_labware("nunc_96_wellplate_1000ul", '2')
    three_eighty_four = ctx.load_labware(labware_384_well_plate, '3')

    # each primer in a 1 mL plate column (source for multichannel transfer)
    for well, col in zip(
     [n1_primer_well, n2_primer_well, rp_primer_well, ntc_primer_well],
     [n1_col, n2_col, rp_col, ntc_col]):
        p300s.transfer(
         primer_col_volume, two_ml_plate.wells_by_name()[well],
         one_ml_plate.columns_by_name()[col])

    # primer to 384 well plate in arrangement specified by "384 plate map.png"
    for index, column in enumerate(three_eighty_four.columns()):
        if index % 2 == 0:
            p20m.transfer(
             primer_volume,
             [one_ml_plate.columns_by_name()[n1_col],
              one_ml_plate.columns_by_name()[rp_col]], column,
             new_tip='always')
        else:
            p20m.transfer(
             primer_volume, [
              one_ml_plate.columns_by_name()[n2_col],
              one_ml_plate.columns_by_name()[ntc_col]], column,
             new_tip='always')
