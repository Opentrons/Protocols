"""Protocol."""

metadata = {
    'protocolName': 'Extraction Prep for TaqPath Covid-19 Combo Kit',
    'author': 'Rami Farawi <rami.farawi@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.10'
}


def run(ctx):
    """Protocol."""
    [num_samp, p1000_sample_height, mag_bead_mix_speed,
     p1000_mag_flow_rate, p300_mount, p1000_mount] = get_values(  # noqa: F821
        "num_samp", "p1000_sample_height", "mag_bead_mix_speed",
        "p1000_mag_flow_rate",
        "p300_mount", "p1000_mount")

    if not 1 <= num_samp <= 95:
        raise Exception("Enter a sample number between 1-95")

    num_samp = num_samp+1

    # load labware
    samples = [ctx.load_labware('opentrons_15_tuberack_5000ul', slot)
               for slot in ['1', '2', '3', '4', '5', '6', '7']]
    sample_plate = ctx.load_labware('nest_96_wellplate_2ml_deep', '8',
                                    label='Sample plate')
    tiprack1000 = [ctx.load_labware('opentrons_96_tiprack_1000ul', '9')]

    # load instrument
    p1000 = ctx.load_instrument('p1000_single_gen2', p1000_mount,
                                tip_racks=tiprack1000)

    # PROTOCOL

    # reagents
    sample_tube_map = [tube for tuberack in samples
                       for tube in tuberack.wells()][:num_samp-1]
    sample_map = [well for row in sample_plate.columns()
                  for well in row][:num_samp]

    # add patient samples
    for i, (sample, well) in enumerate(zip(sample_tube_map*3,
                                           sample_map[:num_samp-1])):
        p1000.pick_up_tip()
        p1000.aspirate(200, sample_tube_map[i].bottom(z=p1000_sample_height))
        p1000.dispense(200, well)
        p1000.blow_out()
        p1000.drop_tip()
