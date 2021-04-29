metadata = {
    'protocolName': 'Plate Aliquoting with CSV',
    'author': 'Rami Farawi <rami.farawi@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.7'
}


def run(ctx):

    [csv_sample, mount, source_plate, dest_plate1,
        dest_plate2, dest_plate3] = get_values(  # noqa: F821
        "csv_sample", "mount", "source_plate", "dest_plate1",
            "dest_plate2", "dest_plate3")

    # load labware
    source_plate = ctx.load_labware('nest_96_wellplate_2ml_deep', '1')
    dest_plate1 = ctx.load_labware(dest_plate1, '4')
    dest_plate2 = ctx.load_labware(dest_plate2, '7')
    dest_plate3 = ctx.load_labware(dest_plate3, '10')
    dest_plates = [dest_plate1, dest_plate2, dest_plate3]

    tiprack = [ctx.load_labware('opentrons_96_filtertiprack_200ul', '3')]

    # load instrument
    p300 = ctx.load_instrument('p300_multi_gen2', mount, tip_racks=tiprack)

    # csv file --> nested list
    transfer = [[val.strip().lower() for val in line.split(',')]
                for line in csv_sample.splitlines()
                if line.split(',')[0].strip()][1:]

    cols = [col for plate in dest_plates for col in plate.rows()[0]]
    destinations = [cols[i::12] for i in range(0, len(cols))][:12]
    print(destinations)

    for line, chunk in zip(transfer, destinations):
        p300.pick_up_tip()
        p300.aspirate(int(line[2]),
                      source_plate.rows()[0][int(line[0])-1].bottom(
                      z=int(line[1])))
        [p300.dispense(int(line[3]), dest.top()) for dest in chunk]
        p300.blow_out(source_plate.rows()[0][int(line[0])-1])
        p300.drop_tip()
