import math

metadata = {
    'protocolName': 'Extraction Prep for TaqPath Covid-19 Combo Kit',
    'author': 'Rami Farawi <rami.farawi@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.7'
}


def run(ctx):

    [num_samp, p1000_sample_height,
     p1000_water_height, p20_mount, p1000_mount] = get_values(  # noqa: F821
        "num_samp", "p1000_sample_height",
        "p1000_water_height", "p20_mount", "p1000_mount")

    if not 1 <= num_samp <= 95:
        raise Exception("Enter a sample number between 1-95")

    num_samp = num_samp+1

    # load labware
    samples = [ctx.load_labware('sample_15_tuberack_5000ul', slot)
               for slot in ['1', '2', '3']]
    ethanol_plate = ctx.load_labware('nest_96_wellplate_2ml_deep', '4')
    buffer_plate = ctx.load_labware('nest_96_wellplate_2ml_deep', '5')
    elution_plate = ctx.load_labware('nest_96_wellplate_2ml_deep', '6')
    sample_plate = ctx.load_labware('nest_96_wellplate_2ml_deep', '7')
    buff_reg = ctx.load_labware('buffer_6_tuberack_50000ul', '8')
    proK_water = ctx.load_labware('reagent_15_tuberack_1500ul', '9')
    tiprack1000 = [ctx.load_labware('opentrons_96_tiprack_1000ul', '10')]
    tiprack20 = [ctx.load_labware('opentrons_96_filtertiprack_20ul', '11')]

    # load instrument
    p20 = ctx.load_instrument('p20_single_gen2',
                              p20_mount, tip_racks=tiprack20)
    p1000 = ctx.load_instrument('p1000_single_gen2', p1000_mount,
                                tip_racks=tiprack1000)

    # protocol
    sample_tube_map = [tube for tuberack in samples
                       for tube in tuberack.wells()][:num_samp-1]
    ethanol_map = [well for row in ethanol_plate.rows()
                   for well in row][:num_samp]
    buffer_map = [well for row in buffer_plate.rows()
                  for well in row][:num_samp]
    elution_map = [well for row in elution_plate.rows()
                   for well in row][:num_samp]
    sample_map = [well for row in sample_plate.rows()
                  for well in row][:num_samp]

    # reagents
    buffer = buff_reg.wells()[1]

    if num_samp < 48:
        ethanol = [buff_reg.wells()[0]]
    else:
        ethanol = buff_reg.rows()[0][:2]

    mag_beads = buff_reg.rows()[0][2]
    elution_solution = buff_reg.rows()[1][1]
    proK = proK_water.wells()[0]
    water = proK_water.wells()[1]
    ms2 = proK_water.wells()[2]

    radius = 14
    v_naught_ethanol = 1000*num_samp/2 if num_samp >= 48 else num_samp*1000
    v_naught_buffer = 0.5*v_naught_ethanol
    v_naught_mag_beads = num_samp*275
    h_naught_eth = v_naught_ethanol/(math.pi*radius**2)-10
    h_naught_buff = v_naught_buffer/(math.pi*radius**2)-10
    h_naught_mag = v_naught_mag_beads/(math.pi*radius**2)-10
    dh_eth = 1000/(math.pi*radius**2)*1.2
    dh_buff = 0.5*dh_eth*1.2
    dh_mag = 275/(math.pi*radius**2)*1.2

    # make buffer plate
    p1000.pick_up_tip()
    h_track_buff = h_naught_buff
    for well in buffer_map:
        p1000.aspirate(500, buffer.bottom(z=h_track_buff))
        p1000.dispense(500, well)
        h_track_buff -= dh_buff if h_track_buff > 3 else 0
    p1000.drop_tip()

    # make ethanol plate
    h_track_eth = h_naught_eth
    p1000.pick_up_tip()
    for i, (tube, well) in enumerate(zip(ethanol*num_samp, ethanol_map)):
        p1000.aspirate(1000, tube.bottom(
                        z=h_track_eth))
        p1000.dispense(1000, well)
        if i % 2 == 0:
            h_track_eth -= dh_eth if h_track_eth > 3 else 0
    p1000.drop_tip()

    # make elution buffer plate
    floor = 115
    p1000.pick_up_tip()
    p1000.aspirate(floor, elution_solution)
    chunks = [elution_map[i:i+12] for i in range(0, len(elution_map), 12)]

    for chunk in chunks:
        p1000.aspirate(50*len(chunk), elution_solution)
        for well in chunk:
            p1000.dispense(50, well)
            # ctx.delay(seconds=1.5)
    ctx.comment('\n\n')

    p1000.dispense(floor, elution_solution)
    p1000.blow_out()
    p1000.drop_tip()

    # add proteinase k
    p20.flow_rate.dispense = 3.78
    p20.pick_up_tip()
    for well in sample_map:
        p20.aspirate(5, proK)
        p20.dispense(5, well.top())
        p20.blow_out()
    p20.drop_tip()
    p20.flow_rate.dispense = 7.56

    # add patient samples
    samp_ctr = 0
    for sample, well in zip(sample_tube_map, sample_map):
        p1000.pick_up_tip()
        p1000.aspirate(200,
                       sample_tube_map[samp_ctr].bottom(z=p1000_sample_height))
        p1000.dispense(200, well)
        p1000.drop_tip()
        samp_ctr += 1
        if samp_ctr == 45:
            ctx.pause("Replace sample racks")
            samp_ctr = 0

    # add control
    ctx.comment('Adding control')
    p1000.pick_up_tip()
    p1000.aspirate(200, water)
    p1000.dispense(200, sample_map[samp_ctr].bottom(z=p1000_water_height))
    p1000.drop_tip()

    # add mag beads
    p1000.pick_up_tip()
    h_track_mag = h_naught_mag
    p1000.mix(15, 750, mag_beads.bottom(2))
    for well in sample_map:
        p1000.mix(2, 750, mag_beads.bottom(2))
        p1000.aspirate(275, buffer.bottom(z=h_track_mag))
        p1000.dispense(275, well.top())
        h_track_mag -= dh_mag if h_track_mag > 3 else 1
    p1000.drop_tip()

    # add ms2
    p20.pick_up_tip()
    for well in sample_map:
        p20.aspirate(5, ms2)
        p20.dispense(5, well.top())
    p20.drop_tip()
