metadata = {
    'protocolName': 'Promega MagneSil Purification',
    'author': 'Chaz <protocols@opentrons.com',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.7'
}


def run(protocol):

    # load labware and pipettes
    tips = [protocol.load_labware(
        'opentrons_96_tiprack_300ul', str(s)) for s in range(7, 9)]

    dwp500 = protocol.load_labware(
        'eppendorf_96_deepwellplate_500ul', '5', 'Eppendorf DWP 500ul')

    corning = protocol.load_labware('corning_96_wellplate_360ul_flat', '6')

    magdeck = protocol.load_module('magdeck', '4')
    magplate = magdeck.load_labware(
        'eppendorf_96_deepwellplate_2000ul', 'Eppendorf DWP 2000ul')
    maght = 14.94

    res = protocol.load_labware('usascientific_12_reservoir_22ml', '2')

    p300 = protocol.load_instrument('p300_multi', 'left', tip_racks=tips)

    # reagents
    rb, lysis, neutr, magblue, magred, etoh, elution = res.wells()[:7]
    waste = res.wells()[-1].top(-2)
    samps = dwp500['A1']
    magsamps = magplate['A1']
    elutes = corning['A1']

    protocol.set_rail_lights(True)

    # transfers
    protocol.comment('\nTransferring 90uL of Resuspension Buffer\n')
    p300.transfer(90, rb, samps, mix_after=(10, 70))

    protocol.comment('\nTransferring 120uL of Lysis Solution\n')
    p300.transfer(120, lysis, samps, mix_after=(5, 150))

    protocol.comment('Pausing operation for 2 minutes.')
    protocol.delay(minutes=2)

    protocol.comment('\nTransferring 120µL of Neutralization Buffer\n')
    p300.transfer(120, neutr, samps, mix_after=(5, 250))

    protocol.comment('\nTransferring 30µL of MagneSil Blue\n')
    p300.transfer(30, magblue, samps, mix_before=(7, 50), mix_after=(5, 50))

    protocol.comment('Pausing operation for 10 minutes.')
    protocol.delay(minutes=10)

    protocol.comment('\nTransferring 250uL from 500µL Plate to 2mL Plate\n')
    p300.transfer(250, samps, magsamps)

    protocol.comment('\nTransferring 50µL of MagneSil Red\n')
    p300.transfer(50, magred, magsamps, mix_before=(7, 50), mix_after=(5, 200))

    magdeck.engage(height=maght)
    protocol.comment('Incubating for 10 minutes.')
    protocol.delay(minutes=10)

    protocol.comment('\nDiscarding 250µL to waste\n')
    p300.transfer(250, magsamps, waste)

    magdeck.disengage()

    for i in range(1, 4):
        protocol.comment(f'\nPerforming EtOH Wash {i}\n')
        p300.transfer(100, etoh, magsamps, mix_after=(5, 75))

        magdeck.engage(height=maght)
        protocol.comment('Incubating for 2 minutes.')
        protocol.delay(minutes=2)

        protocol.comment('\nDiscarding 100µL to waste\n')
        p300.transfer(100, magsamps, waste)

        magdeck.disengage()

    protocol.comment('Drying for 10 minutes.')
    protocol.delay(minutes=10)

    for _ in range(9):
        protocol.set_rail_lights(not protocol.rail_lights_on)
        protocol.delay(seconds=0.2)

    protocol.pause('Please ensure elution plate is on deck. \n\
                    When ready, click RESUME')
    protocol.set_rail_lights(True)

    protocol.comment('\nTransferring 100µL Elution Buffer\n')
    p300.transfer(100, elution, magsamps, mix_after=(5, 70))

    magdeck.engage(height=maght)
    protocol.comment('Incubating for 10 minutes.')
    protocol.delay(minutes=10)

    protocol.comment('\nTransferring 100µL Elution to Elution Plate\n')
    p300.transfer(100, magsamps, elutes)

    protocol.comment('\nProtocol Complete.')
