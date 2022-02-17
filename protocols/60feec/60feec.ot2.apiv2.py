metadata = {
    'protocolName': 'DNA Dilution with CSV File',
    'author': 'Rami Farawi <rami.farawi@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.11'
}


def get_values(*names):
    import json
    _all_values = json.loads("""{ "csv":"",
                        "p300_mount":"left",
                                  "p20_mount":"right"}""")
    return [_all_values[n] for n in names]


def run(ctx):

    [csv, p20_mount, p300_mount] = get_values(  # noqa: F821
        "csv", "p20_mount", "p300_mount")

    # labware
    reservoir = ctx.load_labware('nest_1_reservoir_195ml', '1')
    final_plate = ctx.load_labware('nest_96_wellplate_100ul_pcr_full_skirt', '2')  # noqa: E501
    dna_plate = ctx.load_labware('nest_96_wellplate_100ul_pcr_full_skirt', '3')  # noqa: E501
    tiprack20 = [ctx.load_labware('opentrons_96_filtertiprack_20ul', slot)
                 for slot in ['4', '5']]
    tiprack300 = [ctx.load_labware('opentrons_96_filtertiprack_200ul', '6')]

    # instruments
    p20 = ctx.load_instrument('p20_single_gen2', p20_mount, tip_racks=tiprack20)  # noqa: E501
    p300 = ctx.load_instrument('p300_single_gen2', p300_mount, tip_racks=tiprack300)  # noqa: E501

    # csv --> nested list
    list_of_rows = [[val.strip() for val in line.split(',')]
                    for line in csv.splitlines()
                    if line.split(',')[0].strip()][1:]

    # mapping
    source_well_loc = 1
    dest_well_loc = 8
    dna_vol_loc = 3
    water_vol_loc = 4

    ctx.comment('\n\nTRANSFERRING WATER\n')
    for line in list_of_rows:
        dest_well = line[dest_well_loc].replace("0", "") if line[dest_well_loc][1] == "0" else line[dest_well_loc]  # noqa: E501
        dest = final_plate.wells_by_name()[dest_well]
        water_vol = float(line[water_vol_loc])

        pip = p20 if water_vol < 20 else p300

        pip.pick_up_tip()
        pip.transfer(water_vol, reservoir.wells()[0], dest, new_tip='never')
        pip.drop_tip()

    ctx.comment('\n\nTRANSFERRING DNA\n')
    for line in list_of_rows:
        source_well = line[source_well_loc].replace("0", "") if line[source_well_loc][1] == "0" else line[source_well_loc]  # noqa: E501
        dest_well = line[dest_well_loc].replace("0", "") if line[dest_well_loc][1] == "0" else line[dest_well_loc]  # noqa: E501
        source = dna_plate.wells_by_name()[source_well]
        dest = final_plate.wells_by_name()[dest_well]
        dna_vol = float(line[dna_vol_loc])

        pip = p20 if water_vol < 20 else p300

        pip.pick_up_tip()
        pip.transfer(dna_vol, source, dest, new_tip='never')
        pip.drop_tip()
