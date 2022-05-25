from opentrons import protocol_api
import math

metadata = {
    'protocolName': 'CovidNow SARS-CoV-2 Assay rRT-PCR Batch Set Up',
    'author': 'Rami Farawi <rami.farawi@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.11'
}


def run(ctx: protocol_api.ProtocolContext):

    [
     num_samp,
     m20_mount
     ] = get_values(  # noqa: F821
         "num_samp",
         "m20_mount"
         )

    if not 0 <= num_samp <= 382:
        raise Exception("Enter a sample number 0-384")
    if 368 <= num_samp < 382:
        raise Exception("This sample number does not work with controls")

    # LABWARE
    pcr_plate = ctx.load_labware(
                  "lifetechnologies_384_wellplate_50ul", '3',
                  label='the 384 PCR PLATE')
    sample_plates = [ctx.load_labware(
                      "thermofisherscientific_96_wellplate_50ul",
                      slot, label="the SAMPLE PLATE")
                     for slot in ['7', '8', '1', '2']]
    reservoir = ctx.load_labware('nest_12_reservoir_15ml', '9')

    # TIPRACKS
    tiprack = [ctx.load_labware('opentrons_96_filtertiprack_20ul', slot,
                                label='20uL TIPRACK')
               for slot in ['4', '5', '10', '11', '6']]

    # INSTRUMENTS
    m20 = ctx.load_instrument('p20_multi_gen2', m20_mount,
                              tip_racks=tiprack)

    # protocol
    reagent = reservoir.wells()[0]
    num_full_plates = math.floor(num_samp/96)
    num_full_cols = math.floor(num_samp/8)
    leftover_cols = num_full_cols - num_full_plates*12
    leftover_samp_col = num_samp % 8

    tip_count = 0

    def pick_up_less(num_tips):
        nonlocal tip_count
        num_channels_per_pickup = num_tips
        tips_ordered = [
                        tip for rack in tiprack
                        for row in rack.rows()[
                            len(rack.rows())-num_channels_per_pickup::-1*num_channels_per_pickup]  # noqa: E501
                        for tip in row]
        m20.pick_up_tip(tips_ordered[tip_count])
        tip_count += 1

    plate_to_384 = [well for i in range(int(len(pcr_plate.columns())/4))
                    for col in pcr_plate.columns()[i*6:i*6+6]
                    for well in col[:2]]

    ctx.comment('\n\n~~~~~~~~MOVING RXN MIX TO PLATE FULL COLUMN~~~~~~~~~\n')
    pick_up_less(8)
    for col in plate_to_384[:num_full_cols-1 if num_samp == 382 else num_full_cols]:  # noqa: E501
        m20.aspirate(15, reagent)
        m20.dispense(15, col)
    m20.drop_tip()

    if num_samp == 382:
        ctx.comment('\n')
        pick_up_less(8)
        m20.aspirate(15, reagent)
        m20.dispense(15, pcr_plate.wells_by_name()['A24'])
        m20.aspirate(15, reagent)
        m20.dispense(15, pcr_plate.wells_by_name()['B24'])
        m20.drop_tip()

    if leftover_samp_col > 0 and num_samp != 382:
        ctx.comment('\n\n~~~~~~~~MOVING RXN MIX TO UNFILLED COLUMN~~~~~~~~~\n')
        pick_up_less(leftover_samp_col)
        m20.aspirate(15, reagent)
        m20.dispense(15, plate_to_384[num_full_cols])
        m20.drop_tip()

    #########################################################################

    ctx.comment('\n\n~~~~~~~~MOVING SAMPLE TO PLATE FULL COLUMN~~~~~~~~~\n')
    source_cols = [well for plate in sample_plates for well in plate.rows()[0]]
    for i, (source, col) in enumerate(zip(
                                        source_cols,
                                        plate_to_384[:num_full_cols-1 if num_samp == 382 else num_full_cols])):  # noqa: E501
        pick_up_less(8)
        m20.aspirate(15, source)
        m20.dispense(15, col)
        m20.drop_tip()

    if num_samp == 382:
        ctx.comment('\n')
        pick_up_less(7)
        m20.aspirate(15, sample_plates[3].rows()[0][10])
        m20.dispense(15, pcr_plate.wells_by_name()['A24'])
        m20.drop_tip()
        pick_up_less(7)
        m20.aspirate(15, sample_plates[3].rows()[0][11])
        m20.dispense(15, pcr_plate.wells_by_name()['B24'])
        m20.drop_tip()

    if leftover_samp_col > 0 and num_samp != 382:
        ctx.comment('\n\n~~~~~~~~MOVING SAMPLE TO UNFILLED COLUMN~~~~~~~~~\n')
        pick_up_less(leftover_samp_col)
        m20.aspirate(15, sample_plates[num_full_plates].rows()[0][leftover_cols])  # noqa: E501
        m20.dispense(15, plate_to_384[num_full_cols])
        m20.drop_tip()
