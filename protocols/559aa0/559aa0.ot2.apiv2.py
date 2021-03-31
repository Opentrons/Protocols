metadata = {
    'protocolName': 'PCR/qPCR prep: distribute primers to 384 well plates',
    'author': 'Steve Plonk <protocols@opentrons.com>',
    'apiLevel': '2.9'
}


def run(ctx):

    # bring in constant values from json string above
    [samp_col_counts, plate_count, labware_384_well_plate, n1_col, n2_col,
     rp_col, ntc_col, primer_volume
     ] = get_values(  # noqa: F821
      'samp_col_counts', 'plate_count', 'labware_384_well_plate', 'n1_col',
      'n2_col', 'rp_col', 'ntc_col', 'primer_volume')

    ctx.set_rail_lights(True)

    # a samp_col_count value between 1-12 specified for each 384-well plate
    if len(samp_col_counts.split(',')) != int(plate_count):
        raise Exception('''A count of patient sample columns (between 1 and 12,
        for downstream steps) must be specified for each 384-well plate.''')

    for num in samp_col_counts.split(','):
        if (int(num) < 1) or (int(num) > 12):
            raise Exception('Invalid number of sample columns specified')

    # patient sample column count (in downstream steps) for each 384-well plate
    col_counts = samp_col_counts.split(',')

    # p20 multi channel, tips
    tips20 = [
     ctx.load_labware(
      "opentrons_96_filtertiprack_20ul", slot) for slot in [9]]

    p20m = ctx.load_instrument(
        "p20_multi_gen2", 'right', tip_racks=tips20)

    # source and destination plates
    one_ml_plate = ctx.load_labware("nunc_96_wellplate_1000ul", '8')

    available_slots = [
     str(slot) for slot in [*range(1, 12)] if ctx.deck[slot] is None]
    plates = [ctx.load_labware(
     labware_384_well_plate, slot) for slot in available_slots[
     :int(plate_count)]]

    for mod, col, well in zip(
     [0, 0, 1, 1], [n1_col, rp_col, n2_col, ntc_col], [0, 1, 0, 1]):
        p20m.pick_up_tip()
        for i, plate in enumerate(plates):
            col_count = int(col_counts[i])*2
            for index, column in enumerate(plate.columns()[:col_count]):
                if index % 2 == mod:
                    p20m.aspirate(
                     primer_volume,
                     one_ml_plate.columns_by_name()[str(col)][0])
                    p20m.dispense(primer_volume, column[well])
        p20m.drop_tip()
