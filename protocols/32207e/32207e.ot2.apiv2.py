metadata = {
    'protocolName': 'Diluting DNA with TE, Using .csv File',
    'author': 'Rami Farawi <rami.farawi@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.11'
}


def run(ctx):

    [csv, dna_asp_rate,
        p20_mount, p300_mount] = get_values(  # noqa: F821
        "csv", "dna_asp_rate",
            "p20_mount", "p300_mount")

    # load Labware
    dna_plate = ctx.load_labware('kingfisher_96_wellplate_100ul', 1)
    final_plate = ctx.load_labware('starstedt_96_wellplate_200ul', 2)
    tuberack = ctx.load_labware('opentrons_6_tuberack_falcon_50ml_conical', 3)
    tipracks20 = [ctx.load_labware('opentrons_96_tiprack_20ul', slot)
                  for slot in [4, 5]]
    tipracks300 = [ctx.load_labware('opentrons_96_tiprack_300ul', slot)
                   for slot in [7, 8]]

    # load instrument
    p20 = ctx.load_instrument("p20_single_gen2", p20_mount,
                              tip_racks=tipracks20)

    p300 = ctx.load_instrument("p300_single_gen2", p300_mount,
                               tip_racks=tipracks300)

    # mapping and parsing
    te = tuberack.wells()[0]
    csv_rows = [[val.strip() for val in line.split(',')]
                for line in csv.splitlines()
                if line.split(',')[0].strip()][1:]

    num_samp = 0
    for row in csv_rows:

        if len(row[4]) == 0:
            break
        else:
            num_samp += 1
    csv_rows = csv_rows[:num_samp]

    for row in csv_rows:
        if float(row[4]) >= 200:
            raise Exception("Volume greater than 200ul TE in csv file")
    num_samp = len(csv_rows)

    # transferring TE
    ctx.comment('\n\n TRANSFERRING TE TO PLATE\n')
    for row in csv_rows:
        well = row[0]
        te_vol = float(row[4])
        pip = p20 if te_vol < 20 else p300
        if not pip.has_tip:
            pip.pick_up_tip()
        if te_vol > 0:
            pip.aspirate(te_vol, te)
            pip.dispense(te_vol, final_plate.wells_by_name()[well])
        else:
            continue
    if p20.has_tip:
        p20.drop_tip()

    if p300.has_tip:
        p300.drop_tip()

    ctx.comment('\n\n TRANSFERRING DNA TO PLATE\n')

    for row in csv_rows:

        dna_vol = float(row[2])
        well = row[0]
        te_vol = float(row[4])
        total_vol = te_vol + dna_vol
        pip = p20 if dna_vol < 20 else p300
        pip.pick_up_tip()
        pip.aspirate(dna_vol, dna_plate.wells_by_name()[well].bottom(z=3), rate=dna_asp_rate)  # noqa: E501
        pip.dispense(dna_vol, final_plate.wells_by_name()[well])
        if total_vol*0.8 > 20:
            if not p300.has_tip:
                p300.pick_up_tip()
                p300.mix(3, total_vol*0.8, final_plate.wells_by_name()[well])
                p300.drop_tip()
            else:
                p300.mix(3, total_vol*0.8, final_plate.wells_by_name()[well])
        else:
            pip.mix(3, total_vol*0.8, final_plate.wells_by_name()[well])
        pip.drop_tip()
