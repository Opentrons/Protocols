metadata = {
    'protocolName': 'swiftbiosci.com accel-amplicon-plus-egfr-pathway-panel',
    'author': 'Steve Plonk <protocols@opentrons.com>',
    'apiLevel': '2.9'
}


def run(ctx):

    # bring in constant values from json string above
    [sample_count, hold_pcr_plate_on_ice_until_block_reaches_98, sample_volume,
     mm_volume, room_temp, mm_well, beads_well, index_rxn_mx_well,
     PEG_NaCl_well, post_PCR_TE_well, initial_sample_col, indexing_sample_col,
     output_sample_col, mag_sample_col, mag_post_index_col
     ] = get_values(  # noqa: F821
      'sample_count', 'hold_pcr_plate_on_ice_until_block_reaches_98',
      'sample_volume', 'mm_volume', 'room_temp', 'mm_well', 'beads_well',
      'index_rxn_mx_well', 'PEG_NaCl_well', 'post_PCR_TE_well',
      'initial_sample_col', 'indexing_sample_col', 'output_sample_col',
      'mag_sample_col', 'mag_post_index_col')

    ctx.set_rail_lights(True)

    ctx.delay(seconds=10)

    if sample_count < 1 or sample_count > 24:
        raise Exception('Invalid number of DNA samples (must be 1-24).')

    # turn off rail lights to bring the pause to the user's attention
    ctx.set_rail_lights(False)
    ctx.pause("""Please pre-cool both the thermocycler block and the
    temperature module to 4 degrees via settings in the Opentrons app prior to
    running this protocol. Please add multiplex master mix and PCR plate
    containing 10 ul DNA samples to their locations on the OT-2 deck""")
    ctx.set_rail_lights(True)

    # setup p20 single channel, p300 single channel, tips
    tips20 = [ctx.load_labware("opentrons_96_filtertiprack_20ul", '5')]
    tips300 = [ctx.load_labware("opentrons_96_tiprack_300ul", '9')]
    p20 = ctx.load_instrument(
        "p20_single_gen2", 'left', tip_racks=tips20)
    p300 = ctx.load_instrument(
        "p300_single_gen2", 'right', tip_racks=tips300)

    # setup temperature module at 4 degrees for multiplex mastermix
    temp = ctx.load_module('Temperature Module', '3')
    temp_reagents = temp.load_labware(
        'opentrons_24_aluminumblock_nest_0.5ml_screwcap',
        'Opentrons 24-Well Aluminum Block')
    temp.set_temperature(4)

    # setup 4 degree thermocycler for mastermix addition to initial samples
    tc = ctx.load_module('thermocycler')
    tc.open_lid()
    tc_plate = tc.load_labware("biorad_96_wellplate_200ul_pcr")
    tc.set_block_temperature(4)

    # setup magnetic module with status 'disengaged'
    mag = ctx.load_module('magnetic module gen2', 6)
    mag_plate = mag.load_labware("nest_96_wellplate_100ul_pcr_full_skirt")
    mag.disengage()

    # define initial DNA sample locations
    # avoid wells located at plate edge to minimize evaporation during PCR
    # example B2 to G2, B3 to G3, B4 to G4, B5 to G5 for 24 samples
    initial_sample = [well for column in tc_plate.columns()[
      initial_sample_col:] for well in column[1:len(column)-1]][:sample_count]

    # setup samples, indices, etoh, master mix, beads, waste, output
    column_well_count = len(tc_plate.columns()[0])
    indexing_sample = tc_plate.wells()[
      indexing_sample_col*column_well_count:sample_count +
      indexing_sample_col*column_well_count]
    output_sample = tc_plate.wells()[
      output_sample_col*column_well_count:sample_count +
      output_sample_col*column_well_count]
    multiplex_mm = temp_reagents.wells_by_name()[mm_well]
    index = ctx.load_labware("biorad_96_wellplate_200ul_pcr", 4)
    reservoir = ctx.load_labware("nest_12_reservoir_15ml", '2')
    etoh = reservoir.wells()[0]
    mag_waste = reservoir.wells()[1]
    mag_sample = mag_plate.wells()[
      mag_sample_col*column_well_count:sample_count +
      mag_sample_col*column_well_count]
    mag_post_index = mag_plate.wells()[
      mag_post_index_col*column_well_count:sample_count +
      mag_post_index_col*column_well_count]
    beads = temp_reagents.wells_by_name()[beads_well]

    # thoroughly mix multiplex mastermix, return tip for reuse
    ctx.set_rail_lights(False)
    ctx.set_rail_lights(True)
    p300.pick_up_tip()
    p300.mix(4, mm_volume*sample_count / 2, multiplex_mm)
    p300.return_tip()
    p300.reset_tipracks()

    # mix DNA samples and multiplex master mix at 4 degrees
    # then (optional) manually transfer plate
    # directly to pre-heated 98 degree thermocycler block
    p20.flow_rate.aspirate = 25
    p20.flow_rate.dispense = 50
    p20.flow_rate.blow_out = 1000
    p20.transfer(
      mm_volume, multiplex_mm, initial_sample, mix_after=(4, 15),
      new_tip='always', disposal_volume=0)

    # deactivate temp deck for later use with room temp cleanup reagents
    temp.deactivate()

    # pcr
    if hold_pcr_plate_on_ice_until_block_reaches_98:
        ctx.set_rail_lights(False)
        ctx.pause("""Please remove the thermocycler plate and place it on ice.
        Then click resume.""")
        ctx.set_rail_lights(True)

    tc.set_lid_temperature(105)
    tc.set_block_temperature(98)

    if hold_pcr_plate_on_ice_until_block_reaches_98:
        ctx.set_rail_lights(False)
        ctx.pause("""Please place thermocycler plate back on the pre-heated
        98 degree block and immediately click resume""")
        ctx.set_rail_lights(True)
    tc.close_lid()

    # define cycling profiles
    profile1 = [{'temperature': 98, 'hold_time_seconds': 30}]

    profile2 = [
        {'temperature': 98, 'hold_time_seconds': 10},
        {'temperature': 63, 'hold_time_minutes': 5},
        {'temperature': 65, 'hold_time_minutes': 1}]

    profile3 = [
        {'temperature': 98, 'hold_time_seconds': 10},
        {'temperature': 64, 'hold_time_minutes': 1}]

    profile4 = [
        {'temperature': 65, 'hold_time_minutes': 1}]

    # run pcr
    rxn_volume = sample_volume + mm_volume
    tc.execute_profile(
      steps=profile1, repetitions=1, block_max_volume=rxn_volume)
    tc.execute_profile(
      steps=profile2, repetitions=4, block_max_volume=rxn_volume)
    tc.execute_profile(
      steps=profile3, repetitions=23, block_max_volume=rxn_volume)
    tc.execute_profile(
      steps=profile4, repetitions=1, block_max_volume=rxn_volume)
    tc.set_block_temperature(4, hold_time_seconds=30)
    tc.set_block_temperature(room_temp)
    tc.set_lid_temperature(room_temp)
    tc.open_lid()

    # clean up post-pcr samples
    bead_mix_volume = sample_count*10
    p300.pick_up_tip()

    # suspend the beads
    ctx.set_rail_lights(False)
    ctx.pause(
      "Please add beads and ethanol to their locations on the OT-2 deck")
    ctx.set_rail_lights(True)
    p300.mix(10, bead_mix_volume, beads)

    # dispense beads to wells of mag module plate, return tip for later reuse
    p300.flow_rate.aspirate = 10
    p300.flow_rate.dispense = 10
    for mag_samp in mag_sample:
        if not p300.has_tip:
            p300.pick_up_tip()
        p300.aspirate(36, beads)
        p300.default_speed = 50
        p300.move_to(mag_samp.top(-2))
        p300.default_speed = 400
        p300.dispense(36, mag_samp.top(-5))
        p300.blow_out()
        p300.return_tip()
    p300.reset_tipracks()

    # pre-cool temperature deck to 4 degrees for cold indexing reaction mix
    temp.set_temperature(4)
    index_rxn_mx = temp_reagents.wells_by_name()[index_rxn_mx_well]

    # dispense post-PCR sample to magnetic module plate (magnets disengaged)
    # mix, let stand 5 min room temp
    # return tip for reuse with supernatant removal on same sample
    p300.transfer(
      30, initial_sample, mag_sample, mix_after=(4, 15),
      new_tip="always", trash=False)
    p300.reset_tipracks()

    # set thermocycler block temperature to 37 for indexing step
    ctx.set_rail_lights(False)
    ctx.pause("""Please add index plate and cold indexing reaction mix to
    their locations on the OT-2 deck""")
    ctx.set_rail_lights(True)
    tc.set_block_temperature(37)
    ctx.delay(minutes=5)

    # magnets engaged, let stand 5 min
    mag.engage()
    ctx.delay(minutes=5)

    # remove sup, return tips for later supernatant removal on same sample
    p300.flow_rate.aspirate = 20
    p300.flow_rate.dispense = 50
    p300.transfer(
      60, [mag_samp.bottom(2) for mag_samp in mag_sample],
      mag_waste.top(1.5), new_tip='always', trash=False)
    p300.reset_tipracks()

    # wash samples 2x with 180 ul 80% etoh
    # reuse etoh tip to distribute etoh in second and later washes
    # reuse other tips for supernatant removal from same sample
    p300.default_speed = 200
    p300.flow_rate.aspirate = 75
    p300.flow_rate.dispense = 50
    for i in range(2):
        p300.pick_up_tip(tips300[0]['A4'])
        for mag_samp in mag_sample:
            p300.air_gap(10)
            p300.aspirate(180, etoh)
            p300.air_gap(5)
            p300.dispense(210, mag_samp.top(-2))
        p300.return_tip()
        if sample_count <= 8:
            ctx.delay(seconds=15)
        for mag_samp in mag_sample:
            p300.pick_up_tip()
            p300.air_gap(10)
            p300.aspirate(190, mag_samp)
            p300.air_gap(5)
            p300.dispense(210, mag_waste.top(1.5))
            p300.return_tip()
        p300.reset_tipracks()

    # aspirate last traces of etoh
    for mag_samp in mag_sample:
        p300.pick_up_tip()
        p300.aspirate(30, mag_samp.bottom(-0.5))
        p300.air_gap(5)
        p300.dispense(35, mag_waste.top(1.5))
        p300.return_tip()

    if sample_count <= 8:
        ctx.comment("Letting beads dry for 3 minutes.")
        ctx.delay(minutes=3)
    mag.disengage()

    # indexing step with post-pcr sample bead pellets
    # distribute cold index reaction mix to post-pcr bead pellets
    p300.pick_up_tip(tips300[0]['B4'])
    p300.distribute(
      35, index_rxn_mx, [mag_samp.top(-2) for mag_samp in mag_sample],
      new_tip='never', trash=False)
    p300.return_tip()

    # add indices to bead pellets and mix
    p20.transfer(
      15, index.wells()[:sample_count], [mag_samp for mag_samp in mag_sample],
      mix_after=(4, 20), new_tip='always')

    # transfer suspended bead pellet to 37 degree thermocycler plate
    p300.starting_tip = tips300[0]['A7']
    p300.transfer(
      55, [mag_samp for mag_samp in mag_sample],
      [ind_samp for ind_samp in indexing_sample],
      new_tip='always', trash=False)

    # define thermocycler profile for indexing
    profile5 = [{'temperature': 37, 'hold_time_minutes': 20}]
    tc.close_lid()
    tc.execute_profile(steps=profile5, repetitions=1)
    tc.set_block_temperature(room_temp)

    # set temp module for room temperature PEG NaCl and post-PCR TE
    temp.set_temperature(room_temp)
    ctx.set_rail_lights(False)
    ctx.pause("""Please add room temperature PEG NaCl and post PCR TE to their
    locations on the OT-2 deck""")
    ctx.set_rail_lights(True)
    PEG_NaCl = temp_reagents.wells_by_name()[PEG_NaCl_well]
    post_PCR_TE = temp_reagents.wells_by_name()[post_PCR_TE_well]

    # post indexing clean up
    # distribute room temperature PEG NaCl to magnetic module plate wells
    p300.pick_up_tip(tips300[0]['C4'])
    p300.distribute(
      42.5, PEG_NaCl, [mag_post_ind for mag_post_ind in mag_post_index],
      new_tip='never')
    p300.drop_tip()

    # transfer post-indexing sample to magnetic module plate
    # mix with room temperature PEG NaCl
    tc.open_lid()
    p300.starting_tip = tips300[0]['A10']
    p300.transfer(
      50, [ind_samp for ind_samp in indexing_sample],
      [mag_post_ind for mag_post_ind in mag_post_index],
      mix_after=(4, 45), new_tip='always', trash=False)

    # let stand 5 minutes magnets disengaged
    ctx.delay(minutes=5)

    # let stand 5 minutes magnets engaged
    mag.engage()
    ctx.delay(minutes=5)

    # remove supernatant with magnet engaged
    p300.reset_tipracks()
    p300.starting_tip = tips300[0]['A10']
    p300.transfer(
      50, [mag_post_ind.bottom(2) for mag_post_ind in mag_post_index],
      mag_waste.bottom(1.5), new_tip='always', trash=False)
    p300.reset_tipracks()
    p300.starting_tip = tips300[0]['A10']

    # post-indexing wash 2x with 180 ul 80% etoh
    # reuse etoh tip to distribute etoh
    # reuse other tips for supernatant removal from same sample
    p300.default_speed = 200
    p300.flow_rate.aspirate = 75
    p300.flow_rate.dispense = 50
    for i in range(2):
        p300.pick_up_tip(tips300[0]['A4'])
        for mag_samp in mag_sample:
            p300.air_gap(10)
            p300.aspirate(180, etoh)
            p300.air_gap(5)
            p300.dispense(210, mag_samp.top(-2))
        p300.return_tip()
        if sample_count <= 8:
            ctx.delay(seconds=15)
        for mag_samp in mag_sample:
            p300.pick_up_tip()
            p300.air_gap(10)
            p300.aspirate(190, mag_samp)
            p300.air_gap(5)
            p300.dispense(210, mag_waste.top(1.5))
            p300.return_tip()
        p300.reset_tipracks()
        p300.starting_tip = tips300[0]['A10']

    # aspirate last traces of etoh
    for mag_samp in mag_sample:
        p300.pick_up_tip()
        p300.aspirate(30, mag_samp.bottom(-0.5))
        p300.air_gap(5)
        p300.dispense(35, mag_waste.top(1.5))
        p300.return_tip()

    if sample_count <= 8:
        ctx.comment("Letting beads dry for 3 minutes.")
        ctx.delay(minutes=3)
    mag.disengage()

    # elute by mixing with 20 ul post-PCR TE
    p20.distribute(
      20, post_PCR_TE,
      [mag_post_ind.top(-2) for mag_post_ind in mag_post_index],
      disposal_volume=0, trash=False)
    p20.reset_tipracks()
    p20.starting_tip = tips20[0]['A7']
    for mag_post_ind in mag_post_index:
        p20.pick_up_tip()
        p20.mix(4, 10, mag_post_ind)
        p20.drop_tip()

    # let stand 2 minutes magnets disengaged
    ctx.delay(minutes=2)

    # let stand 3 minutes magnets engaged
    mag.engage()
    ctx.delay(minutes=3)

    # transfer eluate to output well
    p20.transfer(
      20, [mag_post_ind for mag_post_ind in mag_post_index],
      [output_samp for output_samp in output_sample], new_tip='always')

    # hold at 4 degrees
    tc.set_block_temperature(4)
