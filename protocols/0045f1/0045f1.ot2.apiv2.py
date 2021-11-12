metadata = {
    'protocolName': 'Variable Slide Dispensing',
    'author': 'Rami Farawi <rami.farawi@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.11'
}


def run(ctx):

    [num_tubes, num_slides, spot_labware,
     spot_volume, asp_rate, disp_rate, p20_mount] = get_values(  # noqa: F821
        "num_tubes", "num_slides", "spot_labware",
        "spot_volume", "asp_rate", "disp_rate", "p20_mount")
    num_tubes = int(num_tubes)

    if not 1 <= num_slides <= 6:
        raise Exception("Enter a slide number 1-6")
    if not 1 <= spot_volume <= 6:
        raise Exception("Enter a volume between 1-20ul")
    num_plates = 2 if num_slides > 3 else 1

    # load labware
    tuberack = ctx.load_labware(
                'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', '3')
    tiprack = ctx.load_labware('opentrons_96_filtertiprack_10ul', '4')
    slide_plates = [ctx.load_labware(spot_labware,
                    slot) for slot in ['1', '2'][:num_plates]]

    # load instrument
    p20 = ctx.load_instrument('p20_single_gen2',
                              p20_mount,
                              tip_racks=[tiprack])

    p20.flow_rate.aspirate = p20.flow_rate.aspirate*asp_rate
    p20.flow_rate.dispense = p20.flow_rate.dispense*disp_rate

    all_wells = []

    for z in [2, 4]:
        for k in range(4):
            for i in range(2):
                for j, plate in enumerate(slide_plates):
                    if j > 0:
                        rel_slides = num_slides - 3
                    for column in plate.columns()[k:(rel_slides if j > 0
                                                  else num_slides)*4:4]:
                        for well in column[z+i:14+i:4]:
                            all_wells.append(well)

    all_wells_chunks = [all_wells[i:i+3*num_slides]
                        for i in range(0, len(all_wells), 3*num_slides)]

    p20.pick_up_tip()
    for tube, chunk in zip(tuberack.wells()[:num_tubes], all_wells_chunks):
        p20.distribute(spot_volume, tube, chunk, new_tip='never')
    p20.drop_tip()
