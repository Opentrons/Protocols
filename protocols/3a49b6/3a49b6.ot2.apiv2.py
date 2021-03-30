metadata = {
    'protocolName': 'Normalization',
    'author': 'Steve <protocols@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.9'
}


def run(ctx):

    ctx.set_rail_lights(True)

    # uploaded csv
    [uploaded_csv] = get_values(  # noqa: F821
        "uploaded_csv")

    # data from csv
    header_line, *data_lines = uploaded_csv.splitlines()
    data = [
     dict(zip([item for item in header_line.split(",") if any(item)],
          [item for item in line.split(',')])) for line in data_lines]

    # tips and p20 single
    tips20 = [
     ctx.load_labware(
      "opentrons_96_filtertiprack_20ul", str(slot)) for slot in [8, 5]]
    p20s = ctx.load_instrument(
        "p20_single_gen2", 'right', tip_racks=tips20)

    # labware
    [tube_rack, intermediate_plate, dest_plate] = [
     ctx.load_labware(labware, slot) for labware, slot in zip(
        ["opentrons_10_tuberack_falcon_4x50ml_6x15ml_conical",
         "nest_96_wellplate_100ul_pcr_full_skirt",
         "nest_96_wellplate_100ul_pcr_full_skirt"],
        [str(num) for num in [11, 6, 9]])]

    # water in well A1 of tube rack in slot 11
    water = tube_rack.wells_by_name()['A1']

    # temperature module with pcr plate containing RNA in slot 3
    temp_mod = ctx.load_module('temperature module gen2', '3')
    rna = temp_mod.load_labware("nest_96_wellplate_100ul_pcr_full_skirt")
    temp_mod.set_temperature(4)

    # water to destination plate
    # if Vol RNA <= 2 ul, RNA diluted 5X (water is reduced accordingly)
    p20s.pick_up_tip()
    for item in data:
        if float(item['Vol RNA']) > 2:
            p20s.transfer(
             round(float(item['Vol H2O']), 2), water,
             dest_plate.wells_by_name()[item['Well']],
             new_tip='never', trash=False)
        # for concentrated RNA samples
        # (4*Vol RNA) less water (to make room for 5X diluted RNA below)
        else:
            p20s.transfer(
             round(float(item['Vol H2O']) - (4*float(item['Vol RNA'])), 2),
             water, dest_plate.wells_by_name()[item['Well']],
             new_tip='never', trash=False)
    p20s.return_tip()
    p20s.reset_tipracks()

    # rna to destination plate
    for item in data:
        if float(item['Vol RNA']) > 2:
            p20s.transfer(
             round(float(item['Vol RNA']), 2),
             rna.wells_by_name()[item['Well']],
             dest_plate.wells_by_name()[item['Well']],
             mix_after=(4, 10), new_tip='always')
        # for concentrated RNA samples
        # 5X intermediate dilution of the RNA sample and tranfer 5* Vol RNA
        else:
            p20s.pick_up_tip()
            p20s.consolidate(
             [12, 3], [water, rna.wells_by_name()[item['Well']]],
             intermediate_plate.wells_by_name()[item['Well']],
             mix_after=(4, 10), new_tip='never')
            p20s.transfer(
             round(float(item['Vol RNA']), 2)*5,
             intermediate_plate.wells_by_name()[item['Well']],
             dest_plate.wells_by_name()[item['Well']],
             mix_after=(4, 10), new_tip='never')
            p20s.drop_tip()
