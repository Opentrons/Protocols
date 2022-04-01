metadata = {
    'protocolName': 'SuperScript III: qRT-PCR Prep with CSV File',
    'author': 'Rami Farawi <rami.farawi@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.11'
}


def run(ctx):

    [csv, dna_asp_rate, p300_mount] = get_values(  # noqa: F821
        "csv", "dna_asp_rate", "p300_mount")

    # load Labware
    dna_plate = ctx.load_labware('nest_96_wellplate_200ul_flat', 1)
    final_plate = ctx.load_labware('nest_96_wellplate_200ul_flat', 2)
    tuberack = ctx.load_labware('opentrons_6_tuberack_falcon_50ml_conical', 3)
    tipracks = [ctx.load_labware('opentrons_96_tiprack_300ul', slot)
                for slot in [4, 5]]

    # load instrument
    p300 = ctx.load_instrument("p300_single_gen2", p300_mount,
                               tip_racks=tipracks)

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
        if int(row[4]) >= 200:
            raise Exception("Volume greater than 200ul TE in csv file")
    num_samp = len(csv_rows)

    # transferring TE
    ctx.comment('\n\n TRANSFERRING TE TO PLATE\n')
    p300.pick_up_tip()
    for well, row in zip(final_plate.wells()[:num_samp], csv_rows):
        te_vol = int(row[4])
        if te_vol > 0:
            p300.aspirate(te_vol, te)
            p300.dispense(te_vol, well)
        else:
            continue
    p300.drop_tip()

    ctx.comment('\n\n TRANSFERRING DNA TO PLATE\n')
    for source_well, dest_well, row in zip(final_plate.wells()[:num_samp],
                                           dna_plate.wells(),
                                           csv_rows):
        dna_vol = int(row[2])
        te_vol = int(row[4])
        total_vol = te_vol + dna_vol
        p300.pick_up_tip()
        p300.aspirate(dna_vol, source_well.bottom(z=3), rate=dna_asp_rate)
        p300.dispense(dna_vol, dest_well)
        p300.mix(3, total_vol*0.8, dest_well)
        p300.drop_tip()
