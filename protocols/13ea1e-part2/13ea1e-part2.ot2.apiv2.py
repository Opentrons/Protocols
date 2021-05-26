import math
from opentrons import protocol_api

metadata = {
    'protocolName': 'Extraction Prep for Kingfisher Flex Extractor',
    'author': 'Rami Farawi <rami.farawi@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.7'
}


def get_values(*names):
    import json
    _all_values = json.loads("""{"num_samp":384,"overage_percent": 15,"mix_reps":1,"p20_mount":"left","p300_mount":"right"}""")
    return [_all_values[n] for n in
    names]


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
    tuberack = ctx.load_labware(
        'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', '5')
    pcr_plate_384 = ctx.load_labware('corning_384_wellplate_112ul_flat', '6')
    tiprack20 = [ctx.load_labware('opentrons_96_filtertiprack_20ul', slot)
                 for slot in ['8', '9', '11']]
    tiprack300 = [ctx.load_labware('opentrons_96_tiprack_300ul', slot)
                  for slot in ['7', '10']]

    # load instrument
    p300 = ctx.load_instrument('p300_multi_gen2', p300_mount,
                               tip_racks=tiprack300)
    p20 = ctx.load_instrument('p20_multi_gen2', p20_mount,
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
    n1_pink_vol = (0.39*num_samp*overage)/6  # divide by 6 for number of tube
    rp_blue_vol = n1_pink_vol
    vols = [rp_blue_vol, n1_pink_vol]

    one_step_buffer = tuberack.rows()[1][:6]
    one_step_buffer_vol = (6.25*num_samp*overage)/6
    mastermix_tube = tuberack.rows()[2][:6]
    positive_control = tuberack.rows()[3][5]

    total_mix_vol = (n1_pink_vol+rp_blue_vol+one_step_buffer_vol)*6

    # make mastermix pt. 1
    for tube, vol in zip(reagents, vols):
        if vol > 20:
            pip = p300
            pick_up_300()
        else:
            pip = p20
            pick_up_20()
        for mix_tubes in mastermix_tube:
            pip.aspirate(vol, tube)
            pip.dispense(vol, mix_tubes.top())
        pip.drop_tip()

    # make mastermix pt.2
    remainder = one_step_buffer_vol % 300
    number_transfers = math.floor(one_step_buffer_vol/300)
    for source_tube, dest_tube in zip(one_step_buffer, mastermix_tube):
        if one_step_buffer_vol > 20:
            pip = p300
            if not pip.has_tip:
                pick_up_300()
        else:
            pip = p20
            if not pip.has_tip:
                pick_up_20()
        for _ in range(number_transfers):
            pip.aspirate(300, source_tube)
            pip.dispense(300, dest_tube)
        if remainder > 20:
            pip = p300
            if not pip.has_tip:
                pick_up_300()
        else:
            pip = p20
            if not pip.has_tip:
                pick_up_20()
        pip.aspirate(remainder, source_tube)
        pip.dispense(remainder, dest_tube)
    if p20.has_tip:
        p20.drop_tip()
    if p300.has_tip:
        p300.drop_tip()

    # mix mastermix solution
    pick_up_300()
    for tube in mastermix_tube:
        p300.mix(mix_reps,
                 total_mix_vol if total_mix_vol < 300 else 300,
                 tube)
    p300.drop_tip()

    # plate mapping
    plate1_to_384 = [well for column in pcr_plate_384.columns()[::2]
                     for well in column[::2]][:96 if
                                              num_samp > 96 else num_samp]
    plate2_to_384 = [well for column in pcr_plate_384.columns()[1::2]
                     for well in column[::2]][:96 if num_samp > 192
                                              else num_samp-96]
    plate3_to_384 = [well for column in pcr_plate_384.columns()[::2]
                     for well in column[1::2]][:96 if
                                               num_samp > 288
                                               else num_samp-192]
    plate4_to_384 = [well for column in pcr_plate_384.columns()[1::2]
                     for well in column[1::2]][:num_samp-289]  # 289 for ctrl
    plates = {
                0: plate1_to_384,
                1: plate2_to_384,
                2: plate3_to_384,
                3: plate4_to_384
            }

    # add positive control
    airgap = 5
    ctx.comment('Adding Positive Control')
    pick_up_20()
    p20.aspirate(5.5, positive_control)
    p20.air_gap(airgap)
    p20.dispense(7+airgap, pcr_plate_384.wells()[-1].top())
    p20.drop_tip()

    # distribute mastermix
    ctx.comment('Distributing Mastermix')
    pick_up_20()
    p20.aspirate(7, mastermix_tube[0])
    p20.air_gap(airgap)
    p20.dispense(7+airgap, pcr_plate_384.wells()[-1].top())
    for i, plate in enumerate(sample_plates):
        for tube, well in zip((num_samp*mastermix_tube)[1:], plates[i]):
            p20.aspirate(7, tube)
            p20.air_gap(airgap)
            p20.dispense(7+airgap, well.top())
        ctx.comment('\n\n\n\n\n\n')
    p20.drop_tip()

    # add sample and mix
    ctx.comment('Adding Sample')
    for i, plate in enumerate(sample_plates):
        for s, d in zip(sample_wells, plates[i]):
            pick_up_20()
            p20.aspirate(5.5, s)
            p20.air_gap(airgap)
            p20.dispense(5.5+airgap, d)
            p20.mix(mix_reps, 12.5, d)
            p20.blow_out()
            p20.drop_tip()
