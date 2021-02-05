import math

metadata = {
    'protocolName': 'Protocol 3 - Sample Plate setup',
    'author': 'Sakib <sakib.hossain@opentrons.com>',
    'description': 'Custom Protocol Request',
    'apiLevel': '2.8'
}


def run(ctx):

    [m300_mount, p300_mount, samples, tuberack_1, tuberack_2, tuberack_3,
        tuberack_4, tuberack_5, tuberack_6, tuberack_7,
        final_asp_speed, final_air_gap, tube_height, sample_plate_height,
        reservoir_height, tip_type] = get_values(  # noqa: F821
        "m300_mount", "p300_mount", "samples", "tuberack_1",
        "tuberack_2", "tuberack_3",
        "tuberack_4", "tuberack_5", "tuberack_6",
        "tuberack_7", "final_asp_speed", "final_air_gap",
        "tube_height", "sample_plate_height", "reservoir_height", "tip_type")

    final_asp_speed = float(final_asp_speed)
    final_air_gap = float(final_air_gap)
    tube_height = float(tube_height)
    sample_plate_height = float(sample_plate_height)
    reservoir_height = float(reservoir_height)

    # Get sample number
    samples = int(samples)
    if samples > 96:
        raise Exception("You cannot have greater than 96 samples")

    columns = math.ceil(samples/8)

    # Load Labware
    tipracks = [ctx.load_labware(tip_type, slot)
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

    # Get list of tubes across 7 racks based on sample number
    tuberack_wells = [tuberacks[i].wells() for i in range(len(tuberacks))]
    tuberack_samples = [well for wells in tuberack_wells for well in
                        wells][:samples]

    sample_plate_wells = sample_plate.rows()[0][:columns]
    reservoir_columns = reservoir.wells()[:columns]

    # Aliquot 200 uL from ~7 Tube Racks
    for tuberack_well, sample_well in zip(tuberack_samples,
                                          sample_plate.wells()[:samples]):
        p300.transfer(200, tuberack_well.bottom(tube_height),
                      sample_well.bottom(sample_plate_height),
                      new_tip='always')

    # Aliquot 275 uL from Reservoir
    m300.flow_rate.aspirate = final_asp_speed
    for res, sample_well in zip(reservoir_columns, sample_plate_wells):
        m300.transfer(275, res.bottom(reservoir_height), sample_well.center(),
                      air_gap=final_air_gap, new_tip='always')
