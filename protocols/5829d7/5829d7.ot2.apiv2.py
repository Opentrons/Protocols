metadata = {
    'protocolName': 'Tube to Plate Viral Media Transfer',
    'author': 'Rami Farawi <rami.farawi@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.10'
}


def run(ctx):

    [num_samp, p1000_mount] = get_values(  # noqa: F821
        "num_samp", "p1000_mount")

    # load labware
    wellplate = ctx.load_labware('biorad_96_wellplate_200ul_pcr', '3')
    tiprack = [ctx.load_labware('opentrons_96_filtertiprack_1000ul', '6')]
    tuberacks = [ctx.load_labware(
                 'nest_32_tuberack_8x15ml_8x15ml_8x15ml_8x15ml', slot)
                 for slot in ['1', '4', '7']]

    # load instruments
    p1000 = ctx.load_instrument('p1000_single_gen2', p1000_mount,
                                tip_racks=tiprack)

    # PROTOCOL
    tubes = [tube for tuberack in tuberacks for row in tuberack.rows()
             for tube in row][:num_samp]
    wells = [well for row in wellplate.rows() for well in row]

    for tube, well in zip(tubes, wells):
        p1000.pick_up_tip()
        p1000.aspirate(200, tube)
        p1000.dispense(200, well)
        p1000.drop_tip()
