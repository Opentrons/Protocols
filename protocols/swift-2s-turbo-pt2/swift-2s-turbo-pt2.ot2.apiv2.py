metadata = {
    'protocolName': 'NEW NAME DONT FORGET',
    'author': 'Opentrons <protocols@opentrons.com>',
    'source': 'Protocol Library',
    'apiLevel': '2.1'
}


def run(protocol):
    [pip_type, tip_name, p300tips, samps] = get_values(  # noqa: F821
    'pip_type', 'tip_name', 'p300tips', 'samps')

    # Labware Setup
    sm_tips = [protocol.load_labware(tip_name, '5')]
    big_tips = [protocol.load_labware(p300tips, s) for s in ['6', '9']]
    if tip_name == p300tips:
        sm_tips += big_tips
        big_tips = sm_tips

    small_pip = protocol.load_instrument(pip_type, 'left', tip_racks=sm_tips)
    p300 = protocol.load_instrument('p300_multi', 'right', tip_racks=big_tips)

    rt_reagents = protocol.load_labware(
        'nest_12_reservoir_15ml', '2')

    tempdeck = protocol.load_module('Temperature Module', '1')

    cool_reagents = tempdeck.load_labware(
        'opentrons_24_aluminumblock_generic_2ml_screwcap',
        'Opentrons 24-Well Aluminum Block')

    magdeck = protocol.load_module('Magnetic Module', '4')
    mag_plate = magdeck.load_labware(
        'nest_96_wellplate_100ul_pcr_full_skirt', 'NEST 96-Well Plate')

    reaction_plate = protocol.load_labware(
        'opentrons_96_aluminumblock_nest_wellplate_100ul', '3')

    # Reagent Setup

    pcr_mm = cool_reagents.wells_by_name()['A3']

    beads = rt_reagents.wells_by_name()['A1']
    ethanol = rt_reagents.wells_by_name()['A3']
    te = rt_reagents.wells_by_name()['A6']
    waste = rt_reagents.wells_by_name()['A11']

    ezp = 0
    pps = 2
    ms = 0

    enzymatic_prep_samples = reaction_plate.columns()[ezp]
    pcr_prep_samples = reaction_plate.columns()[pps]
    mag_samples = mag_plate.columns()[ms]

    enzymatic_300 = [enzymatic_prep_samples[0]]
    pcr_300 = [pcr_prep_samples[0]]
    mag_300 = [mag_samples[0]]

    samp_l = [enzymatic_prep_samples, pcr_prep_samples, mag_samples]
    samp_pl = [reaction_plate, reaction_plate, mag_plate]
    samp_300 = [enzymatic_300, pcr_300, mag_300]

    if samps == '16':
        for s, t, plate, n in zip(samp_l, samp_300, samp_pl, [ezp, pps, ms]):
            s += plate.columns()[n+1]
            t.append(plate.columns()[n+1][0])

    # Actively cool the samples and enzymes
    tempdeck.set_temperature(4)

    # Ligation Purification
    # Transfer samples to the Magnetic Module
    p300.flow_rate.aspirate = 75
    for enz_samp, mag_samp in zip(enzymatic_300, mag_300):
        p300.pick_up_tip()
        p300.aspirate(60, enz_samp)
        p300.dispense(60, mag_samp.top(-4))
        p300.blow_out(mag_samp.top(-4))
        p300.drop_tip()

    # Transfer beads to the samples on the Magnetic Module
    p300.pick_up_tip()
    p300.mix(10, 200, beads)

    for mag_samp in mag_300:
        if not p300.hw_pipette['has_tip']:
            p300.pick_up_tip()
        p300.flow_rate.aspirate = 47
        p300.flow_rate.dispense = 10
        p300.aspirate(48, beads)
        p300.default_speed = 50
        p300.move_to(mag_samp.top(-2))
        p300.default_speed = 400
        p300.dispense(48, mag_samp.top(-5))
        p300.blow_out()
        p300.flow_rate.aspirate = 50
        p300.flow_rate.dispense = 50
        p300.mix(10, 80, mag_samp.top(-13.5))
        p300.blow_out(mag_samp.top(-5))
        p300.drop_tip()

    # Incubating for 5 minutes
    protocol.comment("Incubating for 5 minutes.")
    protocol.delay(minutes=5)

    # Engage Magnetic Module
    magdeck.engage()
    protocol.comment("Engaging Magnetic Module and incubating for 6 minutes.")
    protocol.delay(minutes=6)

    # Remove supernatant
    p300.flow_rate.aspirate = 20
    p300.flow_rate.dispense = 50

    for mag_samp in mag_300:
        p300.pick_up_tip()
        p300.aspirate(108, mag_samp.bottom(2))
        p300.dispense(108, waste.bottom(1.5))
        p300.drop_tip()

    # Wash samples 2X with 180uL of 80% EtOH
    p300.default_speed = 200
    p300.flow_rate.aspirate = 75
    p300.flow_rate.dispense = 50

    for _ in range(2):
        for mag_samp in mag_300:
            if not p300.hw_pipette['has_tip']:
                p300.pick_up_tip()
            p300.air_gap(10)
            p300.aspirate(180, ethanol)
            p300.air_gap(5)
            p300.dispense(210, mag_samp.top(-2))
        if samps == '8':
            protocol.delay(seconds=15)
        for mag_samp in mag_300:
            if not p300.hw_pipette['has_tip']:
                p300.pick_up_tip()
            p300.air_gap(10)
            p300.aspirate(190, mag_samp)
            p300.air_gap(5)
            p300.dispense(210, waste.bottom(1.5))
            p300.drop_tip()

    # remove residual ethanol
    for mag_samp in mag_300:
        p300.pick_up_tip()
        p300.aspirate(30, mag_samp.bottom(-0.5))
        p300.air_gap(5)
        p300.drop_tip()

    protocol.comment("Letting beads dry for 3 minutes.")
    protocol.delay(minutes=3)
    magdeck.disengage()

    # Elute clean ligation product
    for mag_samp in mag_300:
        p300.pick_up_tip()
        p300.aspirate(22, te)
        p300.dispense(22, mag_samp.top(-12))
        p300.blow_out(mag_samp.top())
        p300.flow_rate.aspirate = 100
        p300.flow_rate.dispense = 200
        p300.mix(10, 20, mag_samp.top(-13.5))
        p300.blow_out(mag_samp.top())
        p300.flow_rate.aspirate = 75
        p300.flow_rate.dispense = 50
        p300.drop_tip()

    # Incubate for 2 minutes
    protocol.comment("Incubating for 2 minutes.")
    protocol.delay(minutes=2)

    # Engage Magnetic Module
    protocol.comment("Engaging Magnetic Module and incubating for 6 minutes.")
    magdeck.engage()
    protocol.delay(minutes=6)

    # Transfer clean samples to aluminum block plate.
    for mag_samp, pcr_samp in zip(mag_300, pcr_300):
        p300.pick_up_tip()
        p300.aspirate(22, mag_samp.bottom(0.25))
        p300.dispense(22, pcr_samp)
        p300.blow_out(pcr_samp.top())
        p300.drop_tip()

    # Disengage Magnetic Module ofr PCR purification protocol
    magdeck.disengage()

    # PCR Prep
    # Transfer Dual Indexes to the samples
    primers = [well for row in cool_reagents.rows()[1:] for well in row]

    for primer, well in zip(primers, pcr_prep_samples):
        small_pip.pick_up_tip()
        small_pip.aspirate(5, primer.top(-24))
        small_pip.dispense(5, well)
        small_pip.drop_tip()

    # Transfer PCR Master Mix to the samples
    small_pip.pick_up_tip()

    if tip_name == 'opentrons_96_filtertiprack_10ul':
        mix_vol = 10
    else:
        mix_vol = small_pip.max_volume

    small_pip.mix(6, mix_vol, pcr_mm)
    small_pip.blow_out()

    def small_pip_trans(vol, src, dest):
        if vol > small_pip.max_volume:
            while vol > mix_vol:
                if not small_pip.hw_pipette['has_tip']:
                    small_pip.pick_up_tip()
                small_pip.aspirate(mix_vol*0.9, src)
                small_pip.dispense(mix_vol*0.9, dest)
                small_pip.blow_out()
                small_pip.drop_tip()
                vol -= mix_vol*0.9
            small_pip.pick_up_tip()
            small_pip.aspirate(vol, src)
            small_pip.dispense(vol, dest)
        else:
            small_pip.aspirate(vol, src)
            small_pip.dispense(vol, dest)

    for well in pcr_prep_samples:
        if not small_pip.hw_pipette['has_tip']:
            small_pip.pick_up_tip()
        """small_pip.aspirate(25, pcr_mm)
        small_pip.dispense(25, well.top(-12))"""
        small_pip_trans(25, pcr_mm, well.top(-12))
        small_pip.blow_out()
        small_pip.mix(10, 10, well.top(-13.5))
        small_pip.blow_out(well.top(-12))
        small_pip.drop_tip()

    tempdeck.deactivate()
    protocol.comment("Place samples in thermocycler for PCR. \
    Temp deck is turned off. Put reagents on temp deck back in the -20")
