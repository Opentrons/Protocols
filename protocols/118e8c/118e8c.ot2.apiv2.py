import csv
import os

metadata = {
    'protocolName': 'FluoGene HLA NX 96-Well Setup',
    'author': 'Steve <protocols@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.9'
}


def run(ctx):

    [p20_blowout_height, disposal_volume, p300_transfer_height,
     dispense_volume, p300_mixing_height, reduced_pick_up_current,
     p20_tube_height, tracking_reset, p20_dispense_height,
     p20_reservoir_height, touch_radius, touch_v_offset, touch_speed, tip_max,
     dna_volume, reservoir_fill_volume] = get_values(  # noqa: F821
        "p20_blowout_height", "disposal_volume", "p300_transfer_height",
        "dispense_volume", "p300_mixing_height", "reduced_pick_up_current",
        "p20_tube_height", "tracking_reset", "p20_dispense_height",
        "p20_reservoir_height", "touch_radius", "touch_v_offset",
        "touch_speed", "tip_max", "dna_volume", "reservoir_fill_volume")

    ctx.set_rail_lights(True)

    # constrain reduced_pick_up_current value to acceptable range
    if reduced_pick_up_current < 0.1 or reduced_pick_up_current > 0.15:
        raise Exception('''Invalid value for reduced_pick_up_current parameter
                           (must be between 0.1 and 0.15).''')

    """
    for reservoir column tracking between protocol runs
    """
    # for reservoir column tracking between protocol runs
    # if ctx.is_simulating():    # logic reversed for simulation
    if not ctx.is_simulating():
        file_path = '/data/temporary/columnandtiptracking.csv'
        file_dir = os.path.dirname(file_path)
        # check for file directory
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        # check for file; if not there, create initial csv
        if (not os.path.isfile(file_path) or tracking_reset):
            with open(file_path, 'w') as outfile:
                outfile.write(",".join([
                 "0", "A1 of Opentrons 96 Filter Tip Rack 20 µL on 10",
                 "A1 of Opentrons 96 Filter Tip Rack 200 µL on 11", "\n"]))

    current_data_list = []
    # if not ctx.is_simulating():    # logic reversed for simulation
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
    reservoir = ctx.load_labware('nunc_96_wellplate_500ul', '7')

    # increment column index for future protocol run
    if current_col_index < len(reservoir.columns()) - 1:
        new_col_index = current_col_index + 1
    else:
        new_col_index = 0
    """
    protocol steps using tracked reservoir column
    """
    # reagent mix in reservoir column tracked across protocol runs
    reservoir_mix = reservoir.columns()[current_col_index]
    ctx.set_rail_lights(True)

    # tips and p300 multi
    tips300 = [ctx.load_labware('opentrons_96_filtertiprack_200ul', '11')]
    tips20 = [ctx.load_labware('opentrons_96_filtertiprack_20ul', '10')]
    p300s = ctx.load_instrument('p300_single_gen2', 'left', tip_racks=tips300)
    p20m = ctx.load_instrument('p20_multi_gen2', 'right', tip_racks=tips20)

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

    # capture and report original value for p20m pick_up_current
    default_current = ctx._implementation._hw_manager.hardware.\
        _attached_instruments[p20m._implementation.get_mount()].\
        config.pick_up_current
    ctx.comment("""Tip pick-up current for the p20 multi-channel pipette
    initially configured to {} mAmp.""".format(str(default_current)))

    # temporarily reduce p20m pick_up_current for one-channel tip pickup
    ctx._implementation._hw_manager.hardware._attached_instruments[
     p20m._implementation.get_mount()].update_config_item(
     'pick_up_current', reduced_pick_up_current)
    ctx.comment("""Tip pick-up current configuration for the p20 multi-channel
    pipette temporarily reduced to {} mAmp for one-tip pickup.""".format(
     str(reduced_pick_up_current)))

    # one-tip pickup with p20m
    pick_up(p20m)

    # reset p20m pick_up_current to original value
    ctx._implementation._hw_manager.hardware._attached_instruments[
     p20m._implementation.get_mount()].update_config_item(
     'pick_up_current', default_current)
    ctx.comment("""Tip pick-up current for the p20 multi-channel pipette
    restored to initial value of {} mAmp for standard 8-tip pickup.""".format(
     str(ctx._implementation._hw_manager.hardware._attached_instruments[
      p20m._implementation.get_mount()].config.pick_up_current)))

    for tray in trays:
        for reagent in [water, pcr_mix]:
            p20m.mix(1, 4, reagent.bottom(p20_tube_height))
            p20m.aspirate(4, reagent.bottom(p20_tube_height))
            p20m.dispense(
             4, tray.wells_by_name()['H1'].bottom(p20_dispense_height))
            p20m.touch_tip(
             tray.wells_by_name()['H1'], radius=touch_radius,
             v_offset=touch_v_offset, speed=touch_speed)
    p20m.drop_tip()

    # helper function for repeat large vol transfers
    def repeat_max_transfer(current_pipette, remaining, source, dest,
                            flowrate, track_liquid=False,
                            start_clearance_asp=1, stop_clearance_asp=1,
                            start_clearance_disp=1, stop_clearance_disp=1):
        if (start_clearance_asp < 0 or stop_clearance_asp < 0 or
           start_clearance_disp < 0 or stop_clearance_disp < 0):
            raise Exception('Clearances must be greater than 0.')
        total = remaining
        initial_clearance_asp = current_pipette.well_bottom_clearance.aspirate
        initial_clearance_disp = current_pipette.well_bottom_clearance.dispense
        if track_liquid is True:
            current_pipette.well_bottom_clearance.aspirate =\
             start_clearance_asp
            current_pipette.well_bottom_clearance.dispense =\
                start_clearance_disp
            clearance_increment_asp = round((
             start_clearance_asp - stop_clearance_asp) / (total / tip_max))
            clearance_increment_disp = round((
             start_clearance_disp - stop_clearance_disp) / (total / tip_max))
        while remaining > tip_max:
            current_pipette.aspirate(tip_max, source, rate=flowrate)
            current_pipette.dispense(tip_max, dest, rate=flowrate)
            if track_liquid is True:
                if current_pipette.well_bottom_clearance.aspirate >=\
                 stop_clearance_asp + clearance_increment_asp:
                    current_pipette.well_bottom_clearance.aspirate -=\
                     clearance_increment_asp
                else:
                    current_pipette.well_bottom_clearance.aspirate =\
                     stop_clearance_asp
                if current_pipette.well_bottom_clearance.dispense >=\
                   stop_clearance_disp + clearance_increment_disp:
                    current_pipette.well_bottom_clearance.dispense -=\
                     clearance_increment_disp
                else:
                    current_pipette.well_bottom_clearance.dispense =\
                     stop_clearance_disp
            remaining -= tip_max
        current_pipette.aspirate(remaining, source, rate=flowrate)
        current_pipette.dispense(remaining, dest, rate=flowrate)
        restore_initial_clearances(current_pipette, initial_clearance_asp,
                                   initial_clearance_disp)

    def restore_initial_clearances(current_pipette, initial_clearance_asp,
                                   initial_clearance_disp):
        current_pipette.well_bottom_clearance.aspirate = initial_clearance_asp
        current_pipette.well_bottom_clearance.dispense = initial_clearance_disp

    # combine DNA dilution with pcr mix
    p300s.starting_tip = tips300[0].wells_by_name()[
     current_starting_tip_300.split()[0]]
    p300s.pick_up_tip()
    p300s.mix(10, 200, dna_dilution.bottom(p300_mixing_height), rate=3.2)
    repeat_max_transfer(p300s, dna_volume, dna_dilution.bottom(
     p300_transfer_height), pcr_mix.bottom(p300_transfer_height), 0.5)
    p300s.mix(20, 200, pcr_mix.bottom(p300_mixing_height), rate=3.2)

    # reservoir filling
    increment = round((p300_mixing_height - p300_transfer_height) / 7)
    height = p300_mixing_height
    for well in reservoir_mix:
        for rep in range(2):
            repeat_max_transfer(
             p300s, reservoir_fill_volume / 16, pcr_mix.bottom(height),
             well.bottom(5), 0.5)
        if height > 3:
            height -= increment
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
        p20m.aspirate(dispense_volume, reservoir_mix[0].bottom(
         p20_reservoir_height))
        p20m.dispense(dispense_volume, tray.columns()[0][0].bottom(
         p20_dispense_height))
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
                    p20m.aspirate(
                     2*dispense_volume + disposal_volume, reservoir_mix[
                      0].bottom(p20_reservoir_height))
                else:
                    p20m.aspirate(
                     dispense_volume, reservoir_mix[0].bottom(
                      p20_reservoir_height))
            p20m.dispense(dispense_volume, column[0].bottom(
             p20_dispense_height))
            p20m.touch_tip(
             column[0], radius=touch_radius,
             v_offset=touch_v_offset, speed=touch_speed)
            if index % 2:
                p20m.dispense(disposal_volume, reservoir_mix[0].bottom(
                 p20_blowout_height))
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
    # if ctx.is_simulating():    # logic reversed for simulation
    if not ctx.is_simulating():
        with open(file_path, 'w') as outfile:
            outfile.write(new_data)
