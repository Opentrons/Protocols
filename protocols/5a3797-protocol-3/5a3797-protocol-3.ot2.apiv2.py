metadata = {
    'protocolName': 'Protocol 3 - Sample Plate setup',
    'author': 'Sakib <sakib.hossain@opentrons.com>',
    'description': 'Custom Protocol Request',
    'apiLevel': '2.8'
}


def run(ctx):

    # [m300_mount] = get_values(  # noqa: F821
    #     "m300_mount")

    # Load Labware
    tipracks = [ctx.load_labware('opentrons_96_filtertiprack_200ul', slot) for slot in range(1,3)]
    tuberacks = [ctx.load_labware('opentrons_15_tuberack_falcon_15ml_conical', slot) for slot in range(4,11)]
    dw_plate = ctx.load_labware('kingfisher_96_deepwell_plate_2ml', 4)
    sample_plate = ctx.load_labware('kingfisher_96_deepwell_plate_2ml', 5)
    reservoir = ctx.load_labware('nest_12_reservoir_15ml')

    # Load Pipette
    p300 = ctx.load_instrument('p300_single_gen2', 'right', tip_racks=tipracks)
    m300 = ctx.load_instrument('p300_multi_gen2', 'left', tip_racks=tipracks)

    # Get list of tubes across 7 racks, get first 96

    # Add a tip changing pause step