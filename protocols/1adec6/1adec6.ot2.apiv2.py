metadata = {
    'protocolName': 'Small Molecule Library Prep',
    'author': 'Chaz <chaz@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.9'
}


def run(protocol):
    [mnt300, numPlates, dmsovol, avol] = get_values(  # noqa: F821
     'mnt300', 'numPlates', 'dmsovol', 'avol')

    # load labware
    tips = [
        protocol.load_labware('opentrons_96_tiprack_300ul', s) for s in [7, 8]]

    m300 = protocol.load_instrument('p300_multi_gen2', mnt300, tip_racks=tips)

    rsvr = protocol.load_labware('nest_12_reservoir_15ml', '9')

    plates = [
        protocol.load_labware('spl_96_wellplate_200ul', s) for s in [1, 2, 3]
        ][:numPlates]

    p1 = plates[0]

    # Add dmsovol of DMSO to columns 6-10 (neglecting F-H in 10)
    dmso = rsvr['A1']

    m300.pick_up_tip()

    for dest in p1.rows()[0][5:9]:
        m300.transfer(dmsovol, dmso, dest, new_tip='never')

    m300.return_tip()

    m300.pick_up_tip(tips[0]['D1'])
    m300.transfer(dmsovol, dmso, p1['A10'], new_tip='never')
    m300.drop_tip(tips[0]['D1'])

    # Transfer 33uL between columns

    for i in range(4):
        m300.pick_up_tip()
        m300.transfer(33, p1.rows()[0][i], p1.rows()[0][i+5], new_tip='never')
        m300.mix(4, 67, p1.rows()[0][i+5])
        m300.return_tip()

    m300.pick_up_tip(tips[0]['F6'])
    m300.transfer(dmsovol, p1['A5'], p1['A10'], new_tip='never')
    m300.mix(4, 67, p1['A10'])
    m300.drop_tip(tips[0]['F6'])

    for _ in range(6):
        protocol.set_rail_lights(not protocol.rail_lights_on)
        protocol.delay(seconds=1)

    protocol.pause('Please manually add reagents. When ready, click RESUME.')

    # Transfer aliquots to destination plate
    m300.starting_tip = tips[0]['A7']
    wells = [plate.rows()[0] for plate in plates]

    for i in range(12):
        m300.pick_up_tip()
        m300.transfer(avol, wells[0][i], wells[1][i], new_tip='never')
        if numPlates == 3:
            m300.transfer(avol, wells[0][i], wells[2][i], new_tip='never')
        m300.return_tip()

    protocol.comment('\nProtocol complete!')
