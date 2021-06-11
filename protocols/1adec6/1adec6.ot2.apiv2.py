metadata = {
    'protocolName': 'Small Molecule Library Prep (Updated)',
    'author': 'Chaz <chaz@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.9'
}


def run(protocol):
    [mnt20, numPlates] = get_values(  # noqa: F821
     'mnt20', 'numPlates')

    # load labware
    tips = [
        protocol.load_labware('opentrons_96_tiprack_20ul', s) for s in [7, 10]]

    m20 = protocol.load_instrument('p20_multi_gen2', mnt20, tip_racks=tips)

    rsvr = protocol.load_labware('nest_12_reservoir_15ml', '6')

    srcPlate = protocol.load_labware('thermofast_96_wellplate_200ul', '4')
    destPlate = protocol.load_labware('thermofast_96_wellplate_200ul', '5')
    finalPlates = [
        protocol.load_labware(
            'spl_96_wellplate_200ul_flat', s) for s in [1, 2, 3]
        ][:numPlates]

    # Create variables
    dmso = rsvr['A1']
    pbs = rsvr['A2']

    # Add 10µL of PBS to columns 1-4 + A5, B5
    m20.pick_up_tip()

    for dest in destPlate.rows()[0][:4]:
        m20.transfer(10, pbs, dest, new_tip='never')

    m20.drop_tip()

    m20.pick_up_tip(tips[0]['G2'])
    m20.transfer(10, pbs, destPlate['A5'], new_tip='never')
    m20.drop_tip()

    # Add 20µL of DMSO to columns 6-10 (neglecting F-H in 10)

    m20.pick_up_tip()

    for dest in destPlate.rows()[0][5:9]:
        m20.transfer(20, dmso, dest, new_tip='never')

    m20.drop_tip()

    m20.pick_up_tip(tips[0]['E2'])
    m20.transfer(20, dmso, destPlate['A10'], new_tip='never')
    m20.drop_tip()

    # Transfer 20uL from source to destination
    for src, dest in zip([p.rows()[0][:4] for p in [srcPlate, destPlate]]):
        m20.transfer(20, src, dest, mix_after=(4, 20))

    m20.pick_up_tip(tips[0]['C2'])
    m20.transfer(20, srcPlate['A5'], destPlate['A5'],
                 mix_after=(4, 20), new_tip='never')
    m20.drop_tip()

    for src, dest in zip([p.rows()[0][5:9] for p in [srcPlate, destPlate]]):
        m20.transfer(20, src, dest, mix_after=(4, 20))

    m20.pick_up_tip(tips[0]['A2'])
    m20.transfer(20, srcPlate['A5'], destPlate['A10'],
                 mix_after=(4, 20), new_tip='never')
    m20.drop_tip()

    for _ in range(6):
        protocol.set_rail_lights(not protocol.rail_lights_on)
        protocol.delay(seconds=1)

    protocol.pause('Please manually add reagents. When ready, click RESUME.')

    # Transfer aliquots to destination plate
    for i in range(10):
        m20.pick_up_tip()
        for plate in finalPlates:
            m20.aspirate(10, destPlate.rows()[0][i])
            m20.dispense(10, plate.rows()[0][i])

    protocol.comment('\nProtocol complete!')
