import math
from opentrons import protocol_api

metadata = {
    'protocolName': 'Extraction Prep for TaqPath Covid-19 Combo Kit',
    'author': 'Rami Farawi <rami.farawi@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.10'
}


def run(ctx):

    [num_samp, p1000_sample_height, mag_bead_mix_speed,
     p1000_mag_flow_rate, p300_mount, p1000_mount] = get_values(  # noqa: F821
        "num_samp", "p1000_sample_height", "mag_bead_mix_speed",
        "p1000_mag_flow_rate",
        "p300_mount", "p1000_mount")

    if not 1 <= num_samp <= 95:
        raise Exception("Enter a sample number between 1-95")

    num_col = math.floor(num_samp/8)
    num_samp = num_samp+1
    mix_rate = mag_bead_mix_speed/274.7
    remainder = num_samp-num_col*8

    # load labware
    samples = [ctx.load_labware('sample_15_tuberack_5000ul', slot)
               for slot in ['1', '2', '3']]
    ethanol_plate = ctx.load_labware('nest_96_wellplate_2ml_deep', '4',
                                     label='Ethanol plate')
    buffer_plate = ctx.load_labware('nest_96_wellplate_2ml_deep', '5',
                                    label='Buffer plate')
    elution_plate = ctx.load_labware('nest_96_wellplate_2ml_deep', '6',
                                     label='Elution plate')
    sample_plate = ctx.load_labware('nest_96_wellplate_2ml_deep', '7',
                                    label='Sample plate')
    reagents = ctx.load_labware('nest_12_reservoir_15ml', '8')
    ethanol = ctx.load_labware('nest_1_reservoir_195ml', '9',
                               label='Ethanol reservoir')
    tiprack1000 = [ctx.load_labware('opentrons_96_tiprack_1000ul', '10')]
    tiprack300 = [ctx.load_labware('opentrons_96_tiprack_300ul', '11')]

    # load instrument
    p300 = ctx.load_instrument('p300_multi_gen2',
                               p300_mount, tip_racks=tiprack300)
    p1000 = ctx.load_instrument('p1000_single_gen2', p1000_mount,
                                tip_racks=tiprack1000)

    def pick_up1000():
        try:
            p1000.pick_up_tip()
        except protocol_api.labware.OutOfTipsError:
            ctx.pause("Replace all 1000ul tip racks. Empty trash if needed.")
            p1000.reset_tipracks()
            p1000.pick_up_tip()

    def pick_up300():
        try:
            p300.pick_up_tip()
        except protocol_api.labware.OutOfTipsError:
            ctx.pause("Replace all 300ul tip racks. Empty trash if needed.")
            p300.reset_tipracks()
            p300.pick_up_tip()

    # PROTOCOL

    # reagents
    buffer = reagents.wells()[:4]
    elution_solution = reagents.wells()[4]
    mag_beads = reagents.wells()[5:7]
    eth = ethanol.wells()[0]
    sample_tube_map = [tube for tuberack in samples
                       for tube in tuberack.wells()][:num_samp-1]
    sample_map = [well for row in sample_plate.columns()
                  for well in row][:num_samp]

    # make buffer plate
    pick_up300()
    for buffer_col, dest_col in zip(buffer*num_col,
                                    buffer_plate.rows()[0][
                                        :num_col if num_samp % 8 != 0
                                        else num_col+1]):
        p300.transfer(500,
                      buffer_col,
                      dest_col,
                      new_tip='never',
                      touch_tip=True)
    p300.drop_tip()

    if num_samp % 8 != 0:
        pick_up1000()
        for buffer_well, dest_well in zip(buffer*num_col,
                                          buffer_plate.wells()[
                                                            num_col*8:
                                                            num_col*8+remainder
                                                            ]):
            p1000.aspirate(500, buffer_well)
            p1000.dispense(500, dest_well)
        p1000.drop_tip()
    ctx.comment('\n\n\n')

    # make ethanol plate
    ctx.comment('\n\n\n')
    pick_up300()
    for eth_col in buffer_plate.rows()[0][:num_col if num_samp % 8 != 0
                                          else num_col+1]:
        p300.transfer(1000,
                      eth,
                      eth_col,
                      new_tip='never',
                      touch_tip=True)
    p300.drop_tip()
    if num_samp % 8 != 0:
        pick_up1000()
        for eth_well in ethanol_plate.wells()[num_col*8:num_col*8+remainder]:
            p1000.aspirate(1000, eth)
            p1000.dispense(1000, eth_well)
        p1000.drop_tip()

    # make elution buffer plate
    chunks = [
                elution_plate.rows()[0][i:i+4]
                [
                    :num_col+1 if num_samp % 8 == 0
                    else num_col % 4 if i+4 >= num_col+1 else 4
                ]
                for i in range(0, len(elution_plate.rows()[0][:num_col]), 4)
              ]

    if num_samp > 8:
        pick_up300()
    for chunk in chunks:
        p300.aspirate(50*len(chunk)+50, elution_solution)
        p300.touch_tip()
        for well in chunk:
            p300.dispense(50, well)
        p300.dispense(50, elution_solution)
        p300.blow_out()
    if p300.has_tip:
        p300.drop_tip()

    if num_samp % 8 != 0 or num_samp == 8:
        ctx.comment('\n\n\n')
        floor = 115
        pick_up1000()
        p1000.aspirate(floor+50*remainder, elution_solution)
        for elution_well in elution_plate.wells()[
                                                    num_col*8:
                                                    num_col*8+remainder
                                                    ]:
            p1000.dispense(50, elution_well)
        p1000.dispense(floor, elution_solution)
        p1000.blow_out()
        p1000.drop_tip()

    # add patient samples
    samp_ctr = 0
    for sample, well in zip(sample_tube_map*3, sample_map[:num_samp-1]):
        pick_up1000()
        p1000.aspirate(200,
                       sample_tube_map[samp_ctr].bottom(z=p1000_sample_height))
        p1000.dispense(200, well)
        p1000.blow_out()
        p1000.drop_tip()
        samp_ctr += 1
        if samp_ctr == 45:
            ctx.pause("Replace sample racks")
            samp_ctr = 0

    # add mag beads
    pick_up300()
    for well in mag_beads:
        p300.mix(15, 300, well, rate=mix_rate)
    p300.drop_tip()
    p1000.flow_rate.aspirate = p1000_mag_flow_rate
    p1000.flow_rate.dispense = p1000_mag_flow_rate

    for beads, dest_col in zip(mag_beads*num_col,
                               sample_plate.rows()[0][
                                        :num_col if num_samp % 8 != 0
                                        else num_col+1]):
        pick_up300()
        p300.transfer(275,
                      beads,
                      dest_col,
                      new_tip='never',
                      touch_tip=True)
        p300.drop_tip()

    if num_samp % 8 != 0:

        for beads, dest_well in zip(mag_beads*num_col,
                                    sample_plate.wells()[
                                                        num_col*8:
                                                        num_col*8+remainder
                                                        ]):
            pick_up1000()
            p1000.aspirate(275, beads)
            p1000.dispense(275, dest_well)
            p1000.drop_tip()
    ctx.comment('\n\n\n')
