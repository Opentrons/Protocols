metadata = {
    'protocolName': 'Pooling and Normalization via CSV',
    'author': 'Rami Farawi <rami.farawi@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.13'
}


def run(ctx):

    [protocol, csv_samp, p20_mount] = get_values(  # noqa: F821
        "protocol", "csv_samp", "p20_mount")

    if "normalization" in csv_samp.lower() and protocol == "pooling":
        raise Exception("""
                           There appears to be the word "normalization"
                           in your csv, although you have selected "pooling"
                           as the protocol. Please input the correct csv for
                           the "pooling" protocol.
                           """)
    if "pool" in csv_samp.lower() and protocol == "normalization":
        raise Exception("""
                           There appears to be the word "pool" in your csv,
                           although you have selected "normalization"
                           as the protocol. Please input the correct csv for
                           the "pooling" protocol.
                           """)

    csv_lines = [[val.strip() for val in line.split(',')]
                 for line in csv_samp.splitlines()
                 if line.split(',')[0].strip()][2:]

    # labware

    if protocol == "normalization":
        water = ctx.load_labware('agilent_1_reservoir_290ml', 1).wells()[0]
        source_plate = ctx.load_labware('biorad_96_wellplate_200ul_pcr', 2)
        dest_plate = ctx.load_labware('biorad_96_wellplate_200ul_pcr', 3)
        tips = [ctx.load_labware('opentrons_96_filtertiprack_20ul', slot)
                for slot in [4, 5]]

    if protocol == "pooling":
        source_plate = ctx.load_labware('biorad_96_wellplate_200ul_pcr', 2)
        dest_plate = ctx.load_labware('biorad_96_wellplate_200ul_pcr', 3)
        tips = [ctx.load_labware('opentrons_96_filtertiprack_20ul', slot)
                for slot in [4]]

    # pipettes
    p20 = ctx.load_instrument('p20_single_gen2', p20_mount, tip_racks=tips)

    # protocol
    if protocol == "normalization":

        # transfer water
        ctx.comment('\n ------------- TRANSFERRING WATER ------------ \n\n')

        p20.pick_up_tip()
        for line in csv_lines:
            water_vol = float(line[1])
            dest_well = dest_plate.wells_by_name()[line[3]]

            if water_vol <= 0.0:
                continue

            else:
                p20.transfer(water_vol, water, dest_well, new_tip='never')
        p20.drop_tip()

        # dna
        ctx.comment('\n ------------- TRANSFERRING DNA ------------ \n\n')
        for line in csv_lines:

            dna_vol = float(line[2])
            source_well = source_plate.wells_by_name()[line[0]]
            dest_well = dest_plate.wells_by_name()[line[3]]

            if dna_vol <= 0.0:
                continue

            if dna_vol <= 1.0:
                raise Exception("DNA volume found which is less than 1.0ul")

            else:
                p20.pick_up_tip()
                p20.transfer(dna_vol, source_well,
                             dest_well, new_tip='never')
                p20.drop_tip()

    if protocol == "pooling":

        # dna
        ctx.comment('\n ------------- POOLING DNA ------------ \n\n')
        for line in csv_lines:

            dna_vol = float(line[3])
            source_well = source_plate.wells_by_name()[line[0]]
            dest_well = dest_plate.wells_by_name()[line[4]]

            if dna_vol <= 0.0:
                continue

            if dna_vol <= 1.0:
                raise Exception("DNA volume found which is less than 1.0ul")

            else:
                p20.pick_up_tip()
                p20.transfer(dna_vol, source_well,
                             dest_well, new_tip='never')
                p20.drop_tip()
