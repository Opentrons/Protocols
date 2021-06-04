metadata = {
    'protocolName': 'Automated Sample Prep for GNA Octea',
    'author': 'Chaz <chaz@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.9'
}


def run(protocol):
    [mntMulti, mntSingle, numSamps] = get_values(  # noqa: F821
     'mntMulti', 'mntSingle', 'numSamps')

    # load labware
    tips = [
        protocol.load_labware('opentrons_96_filtertiprack_200ul', '10')]
    m300 = protocol.load_instrument(
        'p300_multi_gen2', mntMulti, tip_racks=tips)
    p300 = protocol.load_instrument(
        'p300_single_gen2', mntSingle, tip_racks=tips)

    magDeck = protocol.load_module('magnetic module gen2', '4')
    tempDeck = protocol.load_module('temperature module gen2', '6')
    magPlate = magDeck.load_labware('biorad_96_wellplate_200ul_pcr')
    tempPlate = tempDeck.load_labware(
        'opentrons_96_aluminumblock_biorad_wellplate_200ul')

    rsvr = protocol.load_labware('nest_12_reservoir_15ml', '7')

    deepPlate = protocol.load_labware('nest_96_wellplate_2ml_deep', '8')

    octeaPlate = protocol.load_labware('octea_16_wellplate_40ul', '2')

    # Declare reagents/wells
    wb1 = rsvr['A1']
    hb1 = rsvr['A3']
    waste = rsvr['A12'].top(-2)

    sampsUTM = deepPlate.wells()[:numSamps]
    sampsHB1 = deepPlate.wells()[8:8+numSamps]
    tempSamps = tempPlate.rows()[0][:5]
    magSamps = magPlate.rows()[0][:5]
    rb1 = deepPlate['A12']
    mblyo = deepPlate['D11']
    mmlyo = deepPlate['D12']

    # protocol
    # set temperature module and magdeck
    tempDeck.set_temperature(90)
    magDeck.engage()

    # Transfer 360 HB1 to MB LYO, mix and transfer to deep plate
    p300.pick_up_tip()
    p300.transfer(360, hb1, mblyo.top(-2), new_tip='never')
    p300.mix(5, 180, mblyo)
    # p300.aspirate(180, mblyo)
    p300.distribute(40, mblyo, sampsHB1, new_tip='never')
    p300.drop_tip()

    # Transfer HB1 with multi channel to deep plate and to samples
    m300.pick_up_tip()
    m300.transfer(360, hb1, sampsHB1[0].top(-2), new_tip='never')
    m300.mix(5, 180, sampsHB1[0])
    m300.drop_tip()

    m300.pick_up_tip()
    m300.transfer(300, hb1, sampsUTM[0].top(-2), new_tip='never')
    m300.mix(5, 180, sampsUTM[0])

    for vol in [150, 150, 100]:
        m300.transfer(vol, sampsHB1[0], sampsUTM[0], new_tip='never')

    m300.mix(5, 180, sampsUTM[0])
    m300.drop_tip()

    # Transfer 800ul (160 at a time) to temperature module
    m300.pick_up_tip()
    m300.transfer(160, sampsUTM[0], tempSamps, new_tip='never')

    for well in tempSamps:
        m300.mix(5, 180, well)

    # change temperature and incubate
    tempDeck.set_temperature(80)
    protocol.delay(minutes=2)
    tempDeck.set_temperature(56)

    for well in tempSamps:
        m300.mix(5, 180, well)

    protocol.delay(minutes=3)

    tempDeck.deactivate()

    # Mix and transfer samples from temperature module to magdeck
    for well in tempSamps:
        m300.mix(5, 180, well)

    for src, dest in zip(tempSamps, magSamps):
        m300.transfer(160, src, dest, new_tip='never')

    m300.drop_tip()

    # Incubate on magdeck and transfer supernatant
    protocol.delay(minutes=3)

    m300.pick_up_tip()
    m300.flow_rate.aspirate = 20

    for src in magSamps:
        m300.transfer(160, src, waste, new_tip='never')

    magDeck.disengage()

    m300.drop_tip()

    # Transfer wb1 to samples on the magdeck and re-combine
    m300.pick_up_tip()
    m300.flow_rate.aspirate = 92.86

    m300.transfer(40, wb1, [w.top(-2) for w in magSamps], new_tip='never')
    magLast = magSamps[-1]

    for well in magSamps[:-1]:
        m300.transfer(40, well, magLast, mix_before=(5, 30), new_tip='never')

    m300.mix(5, 160, magLast)

    # Engage magdeck and remove supernatant
    magDeck.engage()
    protocol.delay(minutes=3)

    m300.flow_rate.aspirate = 20
    for _ in range(2):
        m300.transfer(100, magLast, waste, new_tip='never')

    magDeck.disengage()
    m300.drop_tip()
    m300.flow_rate.aspirate = 92.86

    # transfer RB1 to MMLYO and distribute
    magSamps2 = magPlate.wells()[32:32+numSamps]
    p300.pick_up_tip()

    for _ in range(2):
        p300.transfer(175, rb1, mmlyo.top(-2), new_tip='never')

    p300.mix(5, 175, mmlyo)

    p300.transfer(40, mmlyo, [w.top() for w in magSamps2], new_tip='never')
    p300.drop_tip()

    m300.pick_up_tip()
    m300.mix(7, 30, magLast)
    m300.drop_tip()

    # transfer samples to octea plate

    for src, dest in zip(magSamps2, octeaPlate.rows()[0][:numSamps]):
        p300.transfer(40, src, dest)

    # p300.transfer(40, mmlyo, octeaPlate.wells()[numSamps:])
