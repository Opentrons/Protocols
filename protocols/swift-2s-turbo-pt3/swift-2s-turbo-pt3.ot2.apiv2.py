metadata = {
    'protocolName': 'NEW NAME DONT FORGET',
    'author': 'Opentrons <protocols@opentrons.com>',
    'source': 'Protocol Library',
    'apiLevel': '2.1'
}


def run(protocol):
    [p300tips, samps] = get_values(  # noqa: F821
    'p300tips', 'samps')

    # Labware Setup
    big_tips = [protocol.load_labware(p300tips, s) for s in ['6', '9']]
    p300 = protocol.load_instrument('p300_multi', 'right', tip_racks=big_tips)

    rt_reagents = protocol.load_labware(
        'nest_12_reservoir_15ml', '2')

    magdeck = protocol.load_module('Magnetic Module', '4')
    mag_plate = magdeck.load_labware('biorad_96_wellplate_200ul_pcr')

    reaction_plate = protocol.load_labware(
        'opentrons_96_aluminumblock_nest_wellplate_100ul', '3')

    # Reagent Setup
    beads = rt_reagents.wells_by_name()['A1']
    ethanol2 = rt_reagents.wells_by_name()['A4']
    te = rt_reagents.wells_by_name()['A6']
    waste2 = rt_reagents.wells_by_name()['A12']

    col_no = [3, 5, 3]

    pcr_prep_samples = [reaction_plate['A3']]
    purified_samples = [reaction_plate['A5']]
    mag_samples = [mag_plate['A3']]

    plate_list = [pcr_prep_samples, purified_samples, mag_samples]

    if samps == '16':
        for n, plate in zip(col_no, plate_list):
            plate.append(reaction_plate.columns()[n][0])

    # PCR Purification

    # Transfer samples to the Magnetic Module
    p300.flow_rate.aspirate = 75
    for pcr_samps, mag_samps in zip(pcr_prep_samples, mag_samples):
        p300.pick_up_tip()
        p300.aspirate(60, pcr_samps)
        p300.dispense(60, mag_samps.top(-4))
        p300.blow_out(mag_samps.top(-4))
        p300.drop_tip()

    # Transfer beads to the samples in PCR strip
    p300.pick_up_tip()
    p300.mix(5, 60, beads)

    for mag_samps in mag_samples:
        if not p300.hw_pipette['has_tip']:
            p300.pick_up_tip()
        p300.flow_rate.aspirate = 10
        p300.flow_rate.dispense = 10
        p300.aspirate(32.5, beads)
        p300.default_speed = 50
        p300.dispense(32.5, mag_samps.top(-12))
        p300.flow_rate.aspirate = 50
        p300.flow_rate.dispense = 50
        p300.blow_out()
        p300.mix(10, 60, mag_samps.top(-13.5))
        p300.blow_out()
        p300.drop_tip()

    # Incubate for 5 minutes, then engage Magnetic Module and incubate
    protocol.comment('Incubating for 5 minutes.')
    protocol.delay(minutes=5)

    magdeck.engage()
    protocol.delay(minutes=5)

    # Aspirate supernatant
    for mag_samps in mag_samples:
        p300.pick_up_tip()
        p300.aspirate(82.5, mag_samps.bottom(2))
        p300.dispense(82.5, waste2)
        p300.drop_tip()

    # Wash samples 2x with 180ul of 80% EtOH
    for _ in range(2):
        for mag_samps in mag_samples:
            if not p300.hw_pipette['has_tip']:
                p300.pick_up_tip()
            p300.air_gap(5)
            p300.aspirate(180, ethanol2)
            p300.air_gap(10)
            p300.dispense(200, mag_samps.top(-2))
        if samps == '8':
            protocol.delay(seconds=15)
        for mag_samps in mag_samples:
            if not p300.hw_pipette['has_tip']:
                p300.pick_up_tip()
            p300.air_gap(5)
            p300.aspirate(190, mag_samps.bottom(1.5))
            p300.air_gap(10)
            p300.dispense(210, waste2)
            p300.drop_tip()

    # Remove residual 80% EtOH
    for mag_samps in mag_samples:
        p300.pick_up_tip()
        p300.aspirate(30, mag_samps.bottom(0.5))
        p300.air_gap(5)
        p300.drop_tip()

    protocol.delay(minutes=2)
    magdeck.disengage()

    # Elute clean product
    for mag_samps in mag_samples:
        p300.pick_up_tip()
        p300.aspirate(22, te)
        p300.dispense(22, mag_samps.top(-12))
        p300.blow_out(mag_samps.top())
        p300.mix(10, 20, mag_samps.top(-13.5))
        p300.blow_out(mag_samps.top())
        p300.drop_tip()

    # Incubate for 2 minutes, then engage Magnetic Module
    protocol.comment("Incubating for 2 minutes, \
    then engaging Magnetic Module.")
    protocol.delay(minutes=2)

    magdeck.engage()
    protocol.delay(minutes=5)

    # Transfer clean samples to aluminum block plate.
    for mag_samps, p_samps in zip(mag_samples, purified_samples):
        p300.pick_up_tip()
        p300.aspirate(20, mag_samps)
        p300.dispense(22, p_samps.top(-12))
        p300.blow_out()
        p300.drop_tip()

    # Collect clean product
    magdeck.disengage()
    protocol.comment("Clean up complete. Store samples in 4C or -20C for \
    long term storage.")
