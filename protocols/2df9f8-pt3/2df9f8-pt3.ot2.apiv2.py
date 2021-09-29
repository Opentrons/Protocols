"""Protocol."""
import math
metadata = {
    'protocolName': 'Plate Filling Heat Inactivated Covid Samples for PCR - Part 3',  # noqa: E501
    'author': 'Rami Farawi <rami.farawi@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.11'
}


def run(ctx):
    """Protocol."""

    [num_samp, num_plates, p1000_mount] = get_values(  # noqa: F821
        'num_samp', 'num_plates', 'p1000_mount')

    if not 1 <= num_samp <= 96:
        raise Exception("Enter a number of samples between 1-94")

    # load labware
    reservoirs = [ctx.load_labware('nest_1_reservoir_195ml', slot)
                  for slot in ['1', '2']]
    tiprack = [ctx.load_labware('opentrons_96_tiprack_1000ul', '3')]
    plates = [ctx.load_labware(
        'nest_96_wellplate_2ml_deep', slot)
        for slot in ['4', '5', '6', '7', '8', '9', '10', '11']][:num_plates]

    # load instrument
    p1000 = ctx.load_instrument('p1000_single_gen2', p1000_mount,
                                tip_racks=tiprack)

    wells = [well for plate in plates for well in plate.wells()[:num_samp]]
    res_wells = [well for res in reservoirs for well in res.wells()]

    # protocol
    p1000.pick_up_tip()
    for s, d in zip(res_wells*num_samp*12, wells):
        p1000.aspirate(500, s)
        p1000.dispense(500, d)
        p1000.blow_out()
    p1000.drop_tip()
