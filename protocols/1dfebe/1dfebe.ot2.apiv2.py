import itertools
import math

metadata = {
    'protocolName': 'Urine Toxicology Using Enzyme Hydrolysis',
    'author': 'Rami Farawi <rami.farawi@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.11'
}


def run(ctx):

    [use_csv, csv_samp, num_samp, v_0_tube15_enz, v_0_tube15_acid,
        v_0_tube50, samp_asp_height, p300_mount] = get_values(  # noqa: F821
        "use_csv", "csv_samp", "num_samp", "v_0_tube15_enz", "v_0_tube15_acid",
            "v_0_tube50", "samp_asp_height",  "p300_mount")

    if not 1 <= num_samp <= 81:
        raise Exception("Enter a sample number between 1-81")

    v_0_tube50 *= 1000
    v_0_tube15_enz *= 1000
    v_0_tube15_acid *= 1000

    # load labware
    tuberacks = [ctx.load_labware('custom_24_tuberack_7500ul',
                                  slot, label="SAMPLE RACK")
                 for slot in ['4', '1', '5', '2']]
    plate = ctx.load_labware('nest_96_wellplate_1000ul', '3')
    tiprack = ctx.load_labware('opentrons_96_tiprack_300ul', '10')
    reagents = ctx.load_labware(
                    'opentrons_10_tuberack_falcon_4x50ml_6x15ml_conical', '6')

    # load instrument
    p300 = ctx.load_instrument('p300_single_gen2',
                               p300_mount, tip_racks=[tiprack])

    if csv_samp[0] == ',':
        csv_samp = csv_samp[1:]
    plate_map_nest = [[val.strip() for val in line.split(',')][1:]
                      for line in csv_samp.splitlines()
                      if line.split(',')[0].strip()][1:]

    # protocol
    tube_map_double_nest = [

                  [tuberacks[j].columns()[i]+tuberacks[j+1].columns()[i]
                   for i in range(len(tuberacks[0].columns()))]
                  for j in range(0, 4, 2)

                  ]

    tube_map_nest = list(itertools.chain.from_iterable(tube_map_double_nest))
    full_tube_map = list(itertools.chain.from_iterable(tube_map_nest))
    asp_height_concat = list(itertools.chain.from_iterable(plate_map_nest))
    controls = 15

    tube_map = full_tube_map[controls:controls+num_samp]
    sample_plate = plate.wells()[controls:controls+num_samp]
    asp_height_map = asp_height_concat[controls:controls+num_samp]

    # liquid height tracking
    v_naught_enz = v_0_tube15_enz
    v_naught_acid = v_0_tube15_acid
    v_naught_50 = v_0_tube50

    radius15 = reagents.wells()[0].diameter/2
    radius50 = reagents.wells()[-1].diameter/2

    h_naught15_enz = v_naught_enz/(math.pi*radius15**2)
    h_naught15_acid = v_naught_acid/(math.pi*radius15**2)
    h_naught50 = v_naught_50/(math.pi*radius50**2)

    h15_enz = h_naught15_enz
    h15_acid = h_naught15_acid
    h50 = h_naught50

    def adjust_height(vol, tube):
        nonlocal h15_enz
        nonlocal h15_acid
        nonlocal h50

        dh15 = vol/(math.pi*radius15**2)
        dh50 = vol/(math.pi*radius50**2)
        if tube == 'enzyme':
            h15_enz -= dh15
            if h15_enz < 20:
                h15_enz = 1
            else:
                return h15_enz - 10
        elif tube == 'acid':
            h15_acid -= dh15
            if h15_acid < 20:
                h15_acid = 1
            else:
                return h15_acid - 10
        else:
            h50 -= dh50
            if h50 < 10:
                h50 = 1
            else:
                return h50 - 10

    # reagents
    enzyme_hydrolysis = reagents.wells()[0]
    trichloro_acid = reagents.wells()[1]
    buffer = reagents.wells()[-1]

    def create_chunks(list, n):
        for i in range(0, len(list), n):
            yield list[i:i+n]

    # move enzyme to plate
    ctx.comment('Moving enzyme to plate')
    p300.pick_up_tip()
    for chunk in create_chunks(plate.wells()[:num_samp+controls], 4):
        p300.aspirate(240, enzyme_hydrolysis)
        [p300.dispense(60, well) for well in chunk]
        adjust_height(240, 'enzyme')
    p300.drop_tip()
    ctx.comment('\n\n\n\n\n\n')

    ctx.comment('Moving urine to plate')
    # move urine sample to plate
    for tube, dest_well, height in zip(tube_map, sample_plate, asp_height_map):
        p300.pick_up_tip()
        if use_csv:
            p300.aspirate(50, tube.bottom(
                          z=samp_asp_height
                          if height == 'X' or height == 'x' else 1))
        else:
            p300.aspirate(50, tube.bottom(z=samp_asp_height))
        p300.touch_tip()
        p300.dispense(50, dest_well)
        p300.mix(5, 80, dest_well)
        p300.blow_out()
        p300.touch_tip()
        p300.drop_tip()
    ctx.comment('\n\n\n\n\n\n')

    ctx.delay(minutes=30)

    # move acid to plate
    ctx.comment('Moving acid to plate')
    disp_vol = 30
    p300.pick_up_tip()
    for chunk in create_chunks(plate.wells()[:num_samp+controls], 13):
        p300.aspirate(20*len(chunk)+disp_vol, trichloro_acid)
        [p300.dispense(20, well.top(z=-2)) for well in chunk]
        p300.dispense(disp_vol, trichloro_acid)
        p300.blow_out()
        adjust_height(20, 'acid')
    p300.drop_tip()
    ctx.comment('\n\n\n\n\n\n')
    ctx.pause(
                """
    Protocol pausing - Trichloroacetic acid solution has been added.
    to the plate. Select "Resume" on the Opentrons App to resume the protocol.
                """)

    # move buffer to plate
    ctx.comment('Moving buffer to plate')
    p300.pick_up_tip()
    for well in plate.wells()[:num_samp+controls]:
        p300.aspirate(150, buffer)
        p300.dispense(150, well.top())
        p300.blow_out(well.top())
        adjust_height(150, 'buffer')
    p300.drop_tip()
    ctx.comment('\n\n\n\n\n\n')
