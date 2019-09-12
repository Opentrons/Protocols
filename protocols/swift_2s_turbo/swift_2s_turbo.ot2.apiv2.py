# Opentrons Labworks
# Author: Kinnari Watson
# Eight samples of lambda phage genomic DNA
# Define the pipettes and tip racks for the protocol
# Blow out added after every dispense
# APIV2

metadata = {
    "author": "Kinnari Watson",
    "organization": "Opentrons Labworks"
}


def run(protocol_context):
    # Labware Setup
    # rt_reagents = protocol_context.load_labware(
    #     'nest_12_reservoir_15ml', '1')
    # TODO IMMEDIATELY: change this back to nest_12_reservoir_15ml
    # when that labware is added to shared-data
    rt_reagents = protocol_context.load_labware(
        'usascientific_12_reservoir_22ml', '1')

    p20rack = protocol_context.load_labware('opentrons_96_tiprack_20ul', '6')

    p300racks = [protocol_context.load_labware(
                 'opentrons_96_tiprack_300ul', slot) for slot in ['2', '5']]
    # Pipette Setup
    p20 = protocol_context.load_instrument('p20_single_v2.0', 'right',
                                           tip_racks=[p20rack])
    p300 = protocol_context.load_instrument('p300_single_v2.0', 'left',
                                            tip_racks=p300racks)
    # Module Setup
    magdeck = protocol_context.load_module('Magnetic Module', '4')
    mag_plate = magdeck.load_labware('nest_96_wellplate_100ul_pcr_full_skirt')

    tempdeck = protocol_context.load_module('Temperature Module', '3')
    cool_reagents = tempdeck.load_labware(
        'opentrons_24_aluminumblock_generic_2ml_screwcap')

    thermocycler = protocol_context.load_module('thermocycler')
    reaction_plate = thermocycler.load_labware(
        'nest_96_wellplate_100ul_pcr_full_skirt')

    # Reagent Setup
    enzymatic_prep_mm = cool_reagents.wells_by_name()['A1']
    ligation_mm = cool_reagents.wells_by_name()['A2']
    pcr_mm = cool_reagents.wells_by_name()['A3']
    beads = rt_reagents.wells_by_name()['A1']
    ethanol = rt_reagents.wells_by_name()['A2']
    te = rt_reagents.wells_by_name()['A3']
    waste = rt_reagents.wells_by_name()['A12']

    # input DNA volume in microliters
    DNAvolume = 1
    # number of samples
    sample_num = 8

    # Destination of input DNA samples and samples on the magnetic module
    tc_samples = reaction_plate.rows_by_name()
    enzymatic_prep_samples = tc_samples['B'][1:9]
    pcr_prep_samples = tc_samples['C'][1:9]
    purified_samples = tc_samples['D'][1:9]

    mag_samples = mag_plate.rows_by_name()['B'][1:9]

    # Actively cool the samples and enzymes
    tempdeck.set_temperature(4)

    thermocycler.open_lid()
    thermocycler.set_block_temperature(4)

    # Resuspend DNA in a total volume of 19.5 uL
    # # Work around for apiv2 calibration bug is in this loop # #
    for well in enzymatic_prep_samples:
        p20.pick_up_tip()
        p20.aspirate(19.5 - DNAvolume, te)
        p20.dispense(19.5 - DNAvolume, well.top(-12))
        p20.blow_out()
        p20.flow_rate.aspirate = 10
        p20.flow_rate.dispense = 15
        p20.mix(2, 10, well.top(-13.5))
        p20.blow_out(well.top(-12.3))
        p20.drop_tip()

    # Dispense Enzymatic Prep Master Mix to the samples
    for well in enzymatic_prep_samples:
        p20.pick_up_tip()
        p20.aspirate(10.5, enzymatic_prep_mm.bottom(0.2))
        p20.dispense(10.5, well.top(-12))
        p20.blow_out()
        p20.mix(2, 15, well.top(-13.5))
        p20.move_to(well.top(-12))
        protocol_context.delay(seconds=0.5)
        p20.blow_out()
        p20.drop_tip()

    # set speed back to default
    p20.flow_rate.aspirate = 25
    p20.flow_rate.dispense = 50

    # Run Enzymatic Prep Profile
    thermocycler.close_lid()
    thermocycler.set_lid_temperature(70)
    thermocycler.set_block_temperature(32, hold_time_minutes=12)
    thermocycler.set_block_temperature(64.5, hold_time_minutes=30)
    thermocycler.set_block_temperature(4)
    thermocycler.deactivate_lid()
    thermocycler.open_lid()

    # Transfer Ligation Master Mix to the samples
    for well in enzymatic_prep_samples:
        p300.home()
        p300.pick_up_tip()
        p300.aspirate(30, ligation_mm)
        p300.dispense(30, well.top(-7))
        p300.blow_out()
        p300.flow_rate.aspirate = 30
        p300.flow_rate.dispense = 30
        p300.mix(2, 30, well.top(-13.5))
        p300.flow_rate.aspirate = 150
        p300.flow_rate.dispense = 300
        p300.blow_out(well.top(-7))
        p300.drop_tip()

    thermocycler.close_lid()
    thermocycler.set_lid_temperature(40)
    thermocycler.set_block_temperature(20.2, hold_time_minutes=20)
    thermocycler.set_block_temperature(4)
    thermocycler.deactivate_lid()
    thermocycler.open_lid()

    """Ligation Purification"""

    # Transfer samples to the Magnetic Module
    p300.flow_rate.aspirate = 75
    for tc, m in zip(enzymatic_prep_samples, mag_samples):
        p300.pick_up_tip()
        p300.aspirate(60, tc.bottom(0.1))
        p300.dispense(60, m.top(-7))
        p300.blow_out()
        p300.drop_tip()

    # Transfer beads to the samples
    for well in mag_samples:
        p300.pick_up_tip()
        # Slow down flow rates to aspirate the beads
        p300.flow_rate.aspirate = 10
        p300.flow_rate.dispense = 10
        p300.aspirate(48, beads)
        p300.default_speed = 50  # slow down robot speed
        p300.move_to(well.top(-2))
        p300.default_speed = 400  # default robot speed
        p300.dispense(48, well.top(-5))
        p300.blow_out()
        # Speed up flow rates for mix steps
        p300.flow_rate.aspirate = 50
        p300.flow_rate.dispense = 50
        p300.mix(10, 80, well.top(-13.5))
        p300.blow_out(well.top(-5))
        p300.drop_tip()

    # Incubate for 1 minutes
    protocol_context.delay(minutes=1)

    # Transfer samples to the PCR plate on the Magnetic Module
    # for tc, mag in zip(enzymatic_prep_samples, mag_samples):
    #     p300.pick_up_tip()
    #     p300.aspirate(108, tc)
    #     p300.dispense(108, mag.top(-4))
    #     p300.blow_out(mag.top(-3))
    #     p300.drop_tip()

    # Place samples on the magnets
    magdeck.engage()
    protocol_context.delay(minutes=3)

    # Remove supernatant
    p300.flow_rate.aspirate = 10
    p300.flow_rate.dispense = 50
    for well in mag_samples:
        p300.pick_up_tip()
        p300.aspirate(108, well.bottom(2))
        p300.dispense(108, waste.bottom(1.5))
        p300.drop_tip()
    for well in mag_samples:
        p20.pick_up_tip()
        p20.aspirate(20, well)
        p20.dispense(20, waste.bottom(1.5))
        p20.drop_tip()

    # Wash samples 2X with 180 uL of 80% EtOH
    p300.default_speed = 200
    p300.flow_rate.aspirate = 10
    p300.flow_rate.dispense = 10
    for _ in range(2):
        for well in mag_samples:
            p300.pick_up_tip()
            p300.aspirate(180, ethanol)
            p300.air_gap(5)
            p300.dispense(210, well.top(-2))
            protocol_context.delay(seconds=0.2)
            p300.air_gap(10)
            p300.drop_tip()
        protocol_context.delay(seconds=30)
        for well in mag_samples:
            p300.pick_up_tip()
            p300.aspirate(180, well)
            p300.air_gap(5)
            p300.dispense(210, waste.bottom(1.5))
            p300.air_gap(10)
            p300.drop_tip()

    # Remove samples from the magnets
    magdeck.disengage()

    # Elute clean ligation product
    for well in mag_samples:
        p300.pick_up_tip()
        p300.aspirate(22, te)
        p300.dispense(22, well.top(-12))
        p300.blow_out(well.top())
        p300.mix(10, 10, well.top(-13.5))
        p300.blow_out(well.top())
        p300.drop_tip()

    # Incubate for 1 minute
    protocol_context.delay(minutes=1)

    # Place samples on the magnets
    magdeck.engage()
    protocol_context.delay(minutes=3)

    # Transfer clean samples to aluminum block plate, new column/8-well strip
    #   The clean ligation product will be transfered to column 2 of the PCR
    #   strips on the aluminum block
    #     tc_samples = reaction_plate.wells()[sample_num:sample_num * 2]
    p300.flow_rate.aspirate = 10
    for mag, tc in zip(mag_samples, pcr_prep_samples):
        p300.pick_up_tip()
        p300.aspirate(22, mag.bottom(0.25))
        p300.dispense(22, tc)
        p300.blow_out(tc.top())
        p300.drop_tip()

    # Disengage MagDeck for PCR purification protocol
    magdeck.disengage()

    """PCR Prep"""
    # Transfer Dual Indexes to the sample
    # Primer screw tubes are shallow !!!!
    primers = [well for well in cool_reagents.wells(
        'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'C1', 'C2')][:sample_num]
    for primer, well in zip(primers, pcr_prep_samples):
        p20.pick_up_tip()
        p20.aspirate(5, primer.top(-24))
        p20.dispense(5, well)
        p20.blow_out()
        p20.drop_tip()

    # Transfer PCR Master Mix to the samples
    for well in pcr_prep_samples:
        p300.pick_up_tip()
        p300.aspirate(25, pcr_mm)
        p300.dispense(25, well.top(-12))
        p300.blow_out()
        p300.mix(10, 10, well.top(-13.5))
        p300.blow_out(well.top(-12))
        p300.drop_tip()

    # Run profile for Indexing PCR
    # COVER_TEMP = 105
    # PLATE_TEMP_PRE = 4
    # PLATE_TEMP_HOLD_1 = (97, 30)  # 30)
    # PLATE_TEMP_HOLD_2 = (97, 10)  # 10)
    # PLATE_TEMP_HOLD_3 = (59.5, 30)   # 30)
    # PLATE_TEMP_HOLD_4 = (67.3, 60)  # 30)
    # # PLATE_TEMP_HOLD_5 = (72, 300)
    # PLATE_TEMP_POST = 4
    # CYCLES = 3

    COVER_TEMP = 105
    PLATE_TEMP_PRE = 4
    PLATE_TEMP_HOLD_1 = (97, 30)  # 30)
    PLATE_TEMP_HOLD_2 = (97, 10)  # 10)
    PLATE_TEMP_HOLD_3 = (59.5, 30)   # 30)
    PLATE_TEMP_HOLD_4 = (67.3, 60)  # 30)
    # PLATE_TEMP_HOLD_5 = (72, 300)
    PLATE_TEMP_POST = 4
    NUM_CYCLES = 3
    CYCLED_STEPS = [
        {
            'temperature': PLATE_TEMP_HOLD_2[0],
            'hold_time_seconds': PLATE_TEMP_HOLD_2[1]},
        {
            'temperature': PLATE_TEMP_HOLD_3[0],
            'hold_time_seconds': PLATE_TEMP_HOLD_3[1]},
        {
            'temperature': PLATE_TEMP_HOLD_4[0],
            'hold_time_seconds': PLATE_TEMP_HOLD_4[1]}]

    # Set PRE temp
    thermocycler.set_block_temperature(PLATE_TEMP_PRE)
    # Set LID temp
    thermocycler.set_lid_temperature(COVER_TEMP)
    thermocycler.close_lid()
    # Set HOLD1 temp
    thermocycler.set_block_temperature(
        PLATE_TEMP_HOLD_1[0], hold_time_seconds=PLATE_TEMP_HOLD_1[1])
    # Loop HOLD2 - HOLD4 temps NUM_CYCLES times
    thermocycler.execute_profile(steps=CYCLED_STEPS, repetitions=NUM_CYCLES)
    # Set HOLD5 temp
    # thermocycler.set_block_temperature(
    #     PLATE_TEMP_HOLD_5[0], hold_time_seconds=PLATE_TEMP_HOLD_5[1])
    # thermocycler.deactivate_lid()
    # Set POST temp
    thermocycler.set_block_temperature(PLATE_TEMP_POST)
    thermocycler.open_lid()

    # PCR purification
    mag_samples = mag_plate.rows_by_name()['C'][1:9]
    # samples = tc_samples[sample_num:sample_num * 2]

    # Transfer samples from thermocycler to magenetic module
    p300.flow_rate.aspirate = 10
    for s, m in zip(pcr_prep_samples, mag_samples):
        p300.pick_up_tip()
        p300.aspirate(50, s)
        p300.dispense(50, m.top(-7))
        p300.blow_out()
        p300.drop_tip()

    # Transfer beads to the samples in PCR strip
    for well in mag_samples:
        p300.pick_up_tip()
        # Slow down speed to aspirate the beads
        p300.flow_rate.aspirate = 10
        p300.flow_rate.dispense = 10
        p300.aspirate(32.5, beads)
        # Slow down the head speed for bead handling
        p300.default_speed = 50
        p300.move_to(well.top(-2))
        # Set the robot speed back to the default
        p300.default_speed = 400
        # Dispense beads to the samples
        p300.dispense(32.5, well.top(-12))
        p300.flow_rate.aspirate = 50
        p300.flow_rate.dispense = 50
        p300.blow_out()
        p300.mix(10, 60, well.top(-13.5))
        p300.move_to(well.top(-12))
        p300.blow_out()
        p300.drop_tip()

    # Incubate for 1 minute
    protocol_context.delay(minutes=1)
    # protocol_context.delay(seconds=5)

    # mag_samples = mag_plate.wells()[sample_num:sample_num * 2]
    # Transfer samples to the PCR plate on the Magnetic Module
    # p300.flow_rate.aspirate = 10
    # for s, m in zip(pcr_prep_samples, mag_samples):
    #     p300.pick_up_tip()
    #     p300.aspirate(82.5, s)
    #     p300.dispense(82.5, m.top(-12))
    #     p300.blow_out()
    #     p300.drop_tip()
    # Place samples on the magnets
    magdeck.engage()
    protocol_context.delay(minutes=3)
    # protocol_context.delay(seconds=5)
    # Aspirate supernatant
    p300.flow_rate.dispense = 50
    for m in mag_samples:
        p300.pick_up_tip()
        p300.aspirate(82.5, m.bottom(2))
        p300.dispense(82.5, waste)  # .top(-14))
        p300.blow_out()
        p300.drop_tip()
    for m in mag_samples:
        p20.pick_up_tip()
        p20.aspirate(20, m)
        p20.dispense(20, waste)  # .top(-14))
        p20.blow_out()
        p20.drop_tip()

    # Set the thermocycler back to 4C  for the final product
    thermocycler.set_block_temperature(4)

    # Wash samples 2X with 180 uL of 80% EtOH
    for _ in range(2):
        for well in mag_samples:
            p300.pick_up_tip()
            p300.aspirate(180, ethanol)
            p300.air_gap(5)
            p300.dispense(180, well.top(-2))
            p300.blow_out()
            p300.drop_tip()
        protocol_context.delay(seconds=30)
        for well in mag_samples:
            p300.pick_up_tip()
            p300.aspirate(180, well)
            p300.air_gap(5)
            p300.dispense(180, waste)
            p300.blow_out()
            p300.drop_tip()

    magdeck.disengage()
    for well in mag_samples:
        p300.pick_up_tip()
        p300.aspirate(22, te)
        p300.dispense(22, well.top(-12))
        p300.blow_out()
        p300.mix(10, 10, well.top(-13.5))
        p300.move_to(well.top(-12))
        p300.blow_out()
        p300.drop_tip()
    # Incubate for 1 minute
    protocol_context.delay(minutes=1)

    # Place samples on the magnets
    magdeck.engage()
    protocol_context.delay(minutes=3)

    # Transfer clean samples to aluminum block plate, new column/8-well strip
    # The clean ligation product will be transfered to column 3 of the PCR
    # plate on the thermocycler

    for s, m in zip(purified_samples, mag_samples):
        p300.pick_up_tip()
        p300.aspirate(22, m)
        p300.dispense(22, s.top(-12))
        p300.blow_out()
        p300.drop_tip()

    # Collect clean product from column 3 of the aluminum block in slot  3
    # Disengage MagDeck for PCR purification protocol
    tempdeck.deactivate()
    magdeck.disengage()
