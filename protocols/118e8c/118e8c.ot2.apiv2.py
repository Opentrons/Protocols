import csv
import os

metadata = {
    'protocolName': 'FluoGene HLA NX 96-Well Setup',
    'author': 'Steve <protocols@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.9'
}


def run(ctx):

    [tracking_reset, dispense_height, aspirate_height, touch_radius,
     touch_v_offset, touch_speed, tip_max, dna_volume,
     reservoir_fill_volume] = get_values(  # noqa: F821
        "tracking_reset", "dispense_height", "aspirate_height", "touch_radius",
        "touch_v_offset", "touch_speed", "tip_max", "dna_volume",
        "reservoir_fill_volume")

    ctx.set_rail_lights(True)

    """
    for reservoir column tracking between protocol runs
    """
    # for reservoir column tracking between protocol runs
    if not ctx.is_simulating():
        file_path = '/data/temporary/columnandtiptracking.csv'
        file_dir = os.path.dirname(file_path)
        # check for file directory
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        # check for file; if not there, create initial csv
        if not os.path.isfile(file_path):
            with open(file_path, 'w') as outfile:
                outfile.write(",".join([
                 "0", "A1 of Opentrons 96 Filter Tip Rack 20 µL on 10",
                 "A1 of Opentrons 96 Filter Tip Rack 200 µL on 11", "\n"]))

    current_data_list = []
    if ctx.is_simulating():
        current_data_list = [0,
                             "A1 of Opentrons 96 Filter Tip Rack 20 µL on 10",
                             "A1 of Opentrons 96 Filter Tip Rack 200 µL on 11"]
    else:
        with open(file_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            current_data_list = next(csv_reader)

    current_col_index = int(current_data_list[0])
    [current_starting_tip_20, current_starting_tip_300] = [
     current_data_list[i] for i in range(1, 3)]

    # reservoir with column tracking between protocol runs
    reservoir = ctx.load_labware('nest_12_reservoir_15ml', '7')

    # increment column index for future protocol run
    if current_col_index < len(reservoir.columns()) - 1:
        new_col_index = current_col_index + 1
    else:
        new_col_index = 0
    """
    protocol steps using tracked reservoir column
    """
    # reagent mix in reservoir column tracked across protocol runs
    reservoir_mix = reservoir.columns()[current_col_index][0]

    ctx.set_rail_lights(True)

    # tips and p300 multi
    tips300 = [ctx.load_labware('opentrons_96_filtertiprack_200ul', '11')]
    tips20 = [ctx.load_labware('opentrons_96_filtertiprack_20ul', '10')]
    p300s = ctx.load_instrument('p300_single_gen2', 'right', tip_racks=tips300)
    p20m = ctx.load_instrument('p20_multi_gen2', 'left', tip_racks=tips20)

    # trays
    trays = [
     ctx.load_labware(labware, slot) for labware, slot in zip(
      ['innotrainot2pcrplate_96_wellplate_200ul',
       'innotrainot22pcrplate_96_wellplate_200ul'], ['5', '6'])]

    # tube rack rxn components: water in A1, pcr mix in A2, DNA dilution in A3
    tube_rack = ctx.load_labware(
     'opentrons_24_tuberack_eppendorf_2ml_safelock_snapcap', '4')
    [water, pcr_mix, dna_dilution] = [
     tube_rack.wells_by_name()[well] for well in ['A1', 'A2', 'A3']]

    """
    pick_up() function to use only the rear-most channel of the p20 multi
    """
    num_channels_per_pickup = 1  # (only pickup tips on rear-most channel)
    tips_ordered = [
        tip for rack in tips20
        for row in rack.rows(
        )[len(rack.rows())-num_channels_per_pickup::-1*num_channels_per_pickup]
        for tip in row]

    tip_count = tips_ordered.index(
     tips20[0].wells_by_name()[
      current_starting_tip_20.split()[0].replace('A', 'H')])

    def pick_up(pip):
        nonlocal tip_count
        pip.pick_up_tip(tips_ordered[tip_count])
        tip_count += 1

    # p20m "single channel" 4 ul each of water and PCR mx to H1 of each tray
    p20m.flow_rate.aspirate = 3.8
    p20m.flow_rate.dispense = 3.8
    pick_up(p20m)
    for tray in trays:
        for reagent in [water, pcr_mix]:
            p20m.mix(1, 4, reagent)
            p20m.aspirate(4, reagent)
            p20m.dispense(
             4, tray.wells_by_name()['H1'].bottom(dispense_height))
            p20m.touch_tip(
             tray.wells_by_name()['H1'], radius=touch_radius,
             v_offset=touch_v_offset, speed=touch_speed)
    p20m.drop_tip()

    # helper function for repeat large vol transfers
    def repeat_max_transfer(remaining, source, dest, flowrate):
        while remaining > tip_max:
            p300s.aspirate(tip_max, source, rate=flowrate)
            p300s.dispense(tip_max, dest, rate=flowrate)
            remaining -= tip_max
        p300s.aspirate(remaining, source, rate=flowrate)
        p300s.dispense(remaining, dest, rate=flowrate)

    # combine DNA dilution with pcr mix and fill reservoir
    p300s.starting_tip = tips300[0].wells_by_name()[
     current_starting_tip_300.split()[0]]
    p300s.pick_up_tip()
    p300s.mix(10, 200, dna_dilution, rate=3.2)
    repeat_max_transfer(dna_volume, dna_dilution, pcr_mix, 0.5)
    p300s.mix(20, 200, pcr_mix, rate=3.2)
    repeat_max_transfer(reservoir_fill_volume, pcr_mix, reservoir_mix, 0.5)
    p300s.drop_tip()
    if tips300[0].next_tip(1, p300s.starting_tip) is not None:
        future_tip_300 = tips300[0].next_tip(1, p300s.starting_tip)
    else:
        future_tip_300 = "A1 of Opentrons 96 Filter Tip Rack 200 µL on 11"

    # standard multi transfer 8 ul to remaining tray wells A1-G1 in column 1
    p20m.flow_rate.dispense = 22
    p20m.reset_tipracks()
    p20m.starting_tip = tips20[0].wells_by_name()[
     current_starting_tip_20.split()[0]]
    p20m.pick_up_tip()
    for tray in trays:
        p20m.aspirate(8, reservoir_mix.bottom(aspirate_height))
        p20m.dispense(8, tray.columns()[0][0].bottom(dispense_height))
        p20m.touch_tip(
         tray.columns()[0][0], radius=touch_radius,
         v_offset=touch_v_offset, speed=touch_speed)
    p20m.drop_tip()

    # standard multi distribute 8 ul to remaining tray wells in columns 2-12
    p20m.pick_up_tip()
    for tray in trays:
        for index, column in enumerate(tray.columns()[1:]):
            if not index % 2:
                if index < len(tray.columns()[1:]) - 1:
                    p20m.aspirate(16, reservoir_mix.bottom(aspirate_height))
                else:
                    p20m.aspirate(8, reservoir_mix.bottom(aspirate_height))
            p20m.dispense(8, column[0].bottom(dispense_height))
            p20m.touch_tip(
             column[0], radius=touch_radius,
             v_offset=touch_v_offset, speed=touch_speed)
    p20m.drop_tip()
    if tips20[0].next_tip(8, p20m.starting_tip) is not None:
        future_tip_20 = tips20[0].next_tip(8, p20m.starting_tip)
    else:
        future_tip_20 = "A1 of Opentrons 96 Filter Tip Rack 20 µL on 10"
    """
    for reservoir column tracking between protocol runs
    """
    # write future column and starting tips to csv for next protocol run
    new_data = ",".join([
     str(new_col_index), str(future_tip_20), str(future_tip_300), '\n'])
    if not ctx.is_simulating():
        with open(file_path, 'w') as outfile:
            if not tracking_reset:
                outfile.write(new_data)
            else:
                outfile.write(",".join([
                 "0", "A1 of Opentrons 96 Filter Tip Rack 20 µL on 10",
                 "A1 of Opentrons 96 Filter Tip Rack 200 µL on 11", "\n"]))
