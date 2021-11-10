metadata = {
    'protocolName': 'SuperScript III: qRT-PCR Prep with CSV File',
    'author': 'Rami Farawi <rami.farawi@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.11'
}


def run(ctx):

    [num_slides, spot_labware,
     spot_volume, asp_rate, disp_rate, p20_mount] = get_values(  # noqa: F821
        "num_slides", "spot_labware",
        "spot_volume", "asp_rate", "disp_rate", "p20_mount")

    if not 1 <= num_slides <= 6:
        raise Exception("Enter a slide number 1-6")
    if not 1 <= spot_volume <= 6:
        raise Exception("Enter a volume between 1-20ul")

    # load labware
    tuberack = ctx.load_labware(
                'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', '3')
    tiprack = ctx.load_labware('opentrons_96_filtertiprack_10ul', '4')
    slide_plates = [ctx.load_labware(spot_labware,
                    slot) for slot in ['1', '2']]  # [:math.ceil(num_slides/6)]

    # load instrument
    p20 = ctx.load_instrument('p20_single_gen2',
                              p20_mount,
                              tip_racks=[tiprack])

    p20.flow_rate.aspirate = p20.flow_rate.aspirate*asp_rate
    p20.flow_rate.dispense = p20.flow_rate.dispense*disp_rate

    bdf_wells = [
                 well
                 for j in range(-(len(slide_plates[0].columns())-1), 1, 1)
                 for k in range(2)
                 for i in range(2)
                 for well in slide_plates[i].columns()[-j][2+k:14+k:2]
                 ][:num_slides*48]

    bdf_wells_chunks = [bdf_wells[i:i+12]
                        for i in range(0, len(bdf_wells), 12)]

    p20.pick_up_tip()
    for tube, chunk in zip(tuberack.wells(), bdf_wells_chunks):
        p20.distribute(spot_volume, tube, chunk, new_tip='never')
    p20.drop_tip()
