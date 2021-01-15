metadata = {
    'protocolName': 'Protocol 3 - Sample Plate setup',
    'author': 'Sakib <sakib.hossain@opentrons.com>',
    'description': 'Custom Protocol Request',
    'apiLevel': '2.8'
}


def run(ctx):

    [m300_mount, p300_mount, tuberack_1, tuberack_2, tuberack_3, tuberack_4,
        tuberack_5, tuberack_6, tuberack_7] = get_values(  # noqa: F821
        "m300_mount", "p300_mount", "tuberack_1", "tuberack_2", "tuberack_3",
        "tuberack_4", "tuberack_5", "tuberack_6", "tuberack_7")

    # Load Labware
    tipracks = [ctx.load_labware('opentrons_96_filtertiprack_200ul', slot)
                for slot in range(1, 3)]
    tuberack_types = [tuberack_1, tuberack_2, tuberack_3, tuberack_4,
                      tuberack_5, tuberack_6, tuberack_7]

    tuberacks = []
    for rack, slot in zip(tuberack_types, range(5, 12)):
        tuberacks.append(ctx.load_labware(rack, slot))

    sample_plate = ctx.load_labware('kingfisher_96_deepwell_plate_2ml', 3)
    reservoir = ctx.load_labware('nest_12_reservoir_15ml', 4)

    # Load Pipette
    p300 = ctx.load_instrument('p300_single_gen2', p300_mount,
                               tip_racks=tipracks)
    m300 = ctx.load_instrument('p300_multi_gen2', m300_mount,
                               tip_racks=tipracks)

    # Get list of tubes across 7 racks, get first 96
    tuberack_wells = [tuberacks[i].wells() for i in range(len(tuberacks))]
    tuberack_samples = [well for wells in tuberack_wells for well in
                        wells][:96]

    # Aliquot 200 uL from ~7 Tube Racks
    p300.transfer(200, tuberack_samples, sample_plate.wells(),
                  new_tip='always')

    # Aliquot 275 uL from Reservoir
    m300.transfer(275, reservoir.wells(), sample_plate.wells(),
                  new_tip='always')
