import math
from opentrons import protocol_api


metadata = {
    'protocolName': 'PCR Plate Prep with 384 Well Plate',
    'author': 'Rami Farawi <rami.farawi@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.9'
}


def run(ctx):

    [num_samp, overage_percent, mix_reps,
        p20_mount, p300_mount] = get_values(  # noqa: F821
        "num_samp", "overage_percent",
        "mix_reps", "p20_mount", "p300_mount")

    if not 0 <= num_samp <= 384:
        raise Exception("Enter a sample number between 1-384")

    num_plates = math.ceil(num_samp/96)
    plates = [str(num+1) for num in range(0, num_plates)]
    overage = 1+overage_percent/100

    if not 0 <= num_samp <= 384:
        raise Exception("Enter a sample number between 1-384")

    # load labware
    sample_plates = [ctx.load_labware('nest_96_wellplate_2ml_deep', slot)
                     for slot in plates]
    tuberack = ctx.load_labware('opentrons_24_tuberack_1500ul', '5')
    pcr_plate_384 = ctx.load_labware('pr1ma_384_wellplate_50ul', '6')
    tiprack20 = [ctx.load_labware('opentrons_96_filtertiprack_20ul', slot)
                 for slot in ['8', '9', '11']]
    tiprack300 = [ctx.load_labware('opentrons_96_tiprack_300ul', slot)
                  for slot in ['7', '10']]

    # load instrument
    p300 = ctx.load_instrument('p300_multi_gen2', p300_mount,
                               tip_racks=tiprack300)
    p20 = ctx.load_instrument('p20_single_gen2', p20_mount,
                              tip_racks=tiprack20)

    num_channels_per_pickup = 1  # (only pickup tips on front-most channel)
    tips_ordered = [
        tip for rack in tiprack300
        for row in rack.rows()[
         len(rack.rows())-num_channels_per_pickup::-1*num_channels_per_pickup]
        for tip in row]
    tip_count = 0

    def pick_up_300():
        nonlocal tip_count
        p300.pick_up_tip(tips_ordered[tip_count])
        tip_count += 1

    def pick_up_20():
        try:
            p20.pick_up_tip()
        except protocol_api.labware.OutOfTipsError:
            ctx.pause("Replace empty tip racks")
            p20.reset_tipracks()
            pick_up_20()

    # protocol
    sample_wells = [well for plate in sample_plates
                    for well in plate.wells()][:num_samp]

    # reagents
    rp_blue = tuberack.rows()[0][0]
    n1_pink = tuberack.rows()[0][1]
    reagents = [rp_blue, n1_pink]

    n1_pink_vol_tot = (0.39*num_samp*overage)
    rp_blue_vol_tot = n1_pink_vol_tot
    one_step_buffer_vol_tot = (6.25*num_samp*overage)
    num_mastermix_tubes = math.ceil(
            (n1_pink_vol_tot+rp_blue_vol_tot+one_step_buffer_vol_tot)/1000)

    n1_pink_vol = (0.39*num_samp*overage)/num_mastermix_tubes
    rp_blue_vol = n1_pink_vol
    one_step_buffer_vol = (6.25*num_samp*overage)/num_mastermix_tubes

    vols = [rp_blue_vol, n1_pink_vol]
    total_mix_vol = n1_pink_vol+rp_blue_vol+one_step_buffer_vol

    one_step_buffer = tuberack.rows()[1][:num_mastermix_tubes]
    mastermix_tube = tuberack.rows()[2][:num_mastermix_tubes]
    positive_control = tuberack.rows()[3][5]

    mastermix_tube_vols = [0 for tube in range(0, num_mastermix_tubes)]

    liquid_prompt = f'''Please ensure you have:
                    {one_step_buffer_vol}ul  of one step buffer in all tubes
                    out of {num_mastermix_tubes} one step buffer tubes.
                    As well as {n1_pink_vol}ul of n1 pink, and
                    {rp_blue_vol}ul of rp blue in their respective tubes.'''
    print('\n\n', liquid_prompt, '\n\n')

    # make mastermix pt. 1
    airgap = 5
    p20.flow_rate.aspirate = p20.flow_rate.aspirate/3
    p300.flow_rate.aspirate = p300.flow_rate.aspirate/3
    p20.flow_rate.dispense = p20.flow_rate.dispense/3
    p300.flow_rate.dispense = p300.flow_rate.dispense/3
    for i, (tube, vol) in enumerate(zip(reagents, vols)):
        for j, mix_tubes in enumerate(mastermix_tube):
            if vol > 20:
                pip = p300
                pick_up_300()
            else:
                pip = p20
                pick_up_20()
            tube_vol = 0
            pip.aspirate(vol, tube.bottom(z=1.5))
            if vol < 15:
                pip.air_gap(airgap)
            pip.dispense(vol+airgap, mix_tubes)
            ctx.delay(seconds=5)
            pip.blow_out()
            pip.touch_tip()
            tube_vol += vol
            mastermix_tube_vols[j] += tube_vol
            pip.drop_tip()
            ctx.comment('\n')
    p20.flow_rate.aspirate = p20.flow_rate.aspirate*3
    p300.flow_rate.aspirate = p300.flow_rate.aspirate*3
    p20.flow_rate.dispense = p20.flow_rate.dispense*3
    p300.flow_rate.dispense = p300.flow_rate.dispense*3

    # make mastermix pt.2
    remainder = one_step_buffer_vol % 300
    number_transfers = math.floor(one_step_buffer_vol/300)
    for i, (source_tube, dest_tube) in enumerate(
                                zip(one_step_buffer, mastermix_tube)):
        if one_step_buffer_vol > 20:
            pip = p300
            if not pip.has_tip:
                pick_up_300()
        else:
            pip = p20
            if not pip.has_tip:
                pick_up_20()
        tube_vol = 0

        pip.flow_rate.aspirate = pip.flow_rate.aspirate/2
        pip.flow_rate.dispense = pip.flow_rate.dispense/2
        for _ in range(number_transfers):
            pip.aspirate(300, source_tube.bottom(z=1.5))
            pip.dispense(300, dest_tube.bottom(z=1.5))
            ctx.delay(seconds=5)
            pip.blow_out()
            pip.touch_tip()

        for _ in range(number_transfers):
            pip.aspirate(300, source_tube)
            pip.dispense(300, dest_tube)

        pip.aspirate(remainder, source_tube.bottom(z=1.5))
        pip.dispense(remainder, dest_tube.bottom(z=1.5))
        tube_vol += remainder
        mastermix_tube_vols[i] += tube_vol
        pip.flow_rate.aspirate = pip.flow_rate.aspirate*2
        pip.flow_rate.dispense = pip.flow_rate.dispense*2

        pip.aspirate(remainder, source_tube)
        pip.dispense(remainder, dest_tube)
        tube_vol += remainder
        mastermix_tube_vols[i] += tube_vol


    if p20.has_tip:
        p20.drop_tip()
    if not p300.has_tip:
        p300.pick_up_tip()

    # mix mastermix solution
    for tube in mastermix_tube:
        p300.mix(mix_reps,
                 total_mix_vol if total_mix_vol < 270 else 270,
                 tube.bottom(z=1.5))

    p300.drop_tip()

    # plate mapping
    plate1_to_384 = [well for column in pcr_plate_384.columns()[::2]
                     for well in column[::2]][:96 if
                                              num_samp > 96 else num_samp]
    plate2_to_384 = [well for column in pcr_plate_384.columns()[1::2]
                     for well in column[::2]][:96 if num_samp > 192
                                              else num_samp-96
                                              if num_samp-96 > 0 else 0]
    plate3_to_384 = [well for column in pcr_plate_384.columns()[::2]
                     for well in column[1::2]][:96 if
                                               num_samp > 288
                                               else num_samp-192
                                               if num_samp-192 > 0 else 0]
    plate4_to_384 = [well for column in pcr_plate_384.columns()[1::2]
                     for well in column[1::2]][:num_samp-288
                                               if num_samp-288 > 0 else 0]
    if num_samp == 384:
        plate4_to_384.pop()

    plates = {
                0: plate1_to_384,
                1: plate2_to_384,
                2: plate3_to_384,
                3: plate4_to_384
            }

    # distribute mastermix
    ctx.comment('Distributing Mastermix')
    pick_up_20()
    p20.aspirate(7, mastermix_tube[0].bottom(z=1.5))
    p20.air_gap(airgap)
    p20.dispense(7+airgap, pcr_plate_384.wells()[-1])

    for i, plate in enumerate(sample_plates):
        for source, well in zip(mastermix_tube*num_samp, plates[i]):

            p20.aspirate(7, source.bottom(z=1.5))
            p20.dispense(7+airgap, well)
    p20.drop_tip()
    ctx.comment('\n\n\n\n\n\n')

    # add positive control
    ctx.comment('Adding Positive Control')
    pick_up_20()
    p20.aspirate(5.5, positive_control.bottom(1.5))
    p20.air_gap(airgap)
    p20.dispense(7+airgap, pcr_plate_384.wells()[-1])
    p20.mix(mix_reps, 12.5, pcr_plate_384.wells()[-1])
    p20.drop_tip()

    # add sample and mix
    ctx.comment('Adding Sample')
    for i, plate in enumerate(sample_plates):
        for s, d in zip(sample_wells, plates[i]):
            pick_up_20()
            p20.aspirate(5.5, s.bottom(z=-2.75))
            p20.air_gap(airgap)
            p20.dispense(5.5+airgap, d)
            p20.mix(mix_reps, 12.5, d)
            p20.blow_out()
            p20.drop_tip()
