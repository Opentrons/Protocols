import math

metadata = {
    'protocolName': 'PCR Prep with 384-Well Plate and Temperature Module',
    'author': 'Chaz <chaz@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.9'
}


def run(protocol):
    [numSamps, pipMnt, tipTrash] = get_values(  # noqa: F821
     'numSamps', 'pipMnt', 'tipTrash')

    # load labware
    tips = [
        protocol.load_labware('opentrons_96_filtertiprack_20ul', s) for s in [
            '5', '6', '8', '9', '11']]
    pip = protocol.load_instrument('p20_multi_gen2', pipMnt, tip_racks=tips)

    tempDeck = protocol.load_module('temperature module gen2', '3')
    tempDeck.set_temperature(4)
    tempPlate = tempDeck.load_labware(
        'opentrons_96_aluminumblock_generic_pcr_strip_200ul')
    sampPlates = [
        protocol.load_labware(
            'kingfisher_96_deepwell_plate_2ml',
            s,
            n) for s, n in zip(
                ['2', '4', '7', '10'],
                ['KF Deepwell-96 Sample Plate 1',
                 'KF Deepwell-96 Sample Plate 2',
                 'KF Deepwell-96 Sample Plate 3',
                 'KF Deepwell-96 Sample Plate 4'])][:math.ceil(numSamps/96)]

    destPlate = protocol.load_labware(
        'microampoptical_384_wellplate_30ul', '1',)

    # Create Variables
    water = [well for well in tempPlate.rows()[0][:4] for _ in range(12)]
    primer = [tempPlate['A5'] for row in range(48)]
    mm = [well for well in tempPlate.rows()[0][5:7] for _ in range(24)]
    tipLocs = [w for rack in tips for w in rack.rows()[0]]

    sampCols = math.ceil(numSamps/8)
    samps = [w for plate in sampPlates for w in plate.rows()[0]][:sampCols]
    dests = [well for row in destPlate.rows()[:2] for well in row][:sampCols]

    # function for transferring reaction mix reagents
    def mm_creation(reagent, vol, rename):
        """
        This is a simple function for transferring reagents to the wells
        of the 384-well plate for the reaction mix step.
        reagent: location of reagent (declared above)
        vol: the volume of the reagent to be added
        rename: string input of the reagent name (for protocol.comment)
        """

        pip.pick_up_tip()
        protocol.comment(f'\nTransferring {vol}uL of {rename} to \
        {sampCols*8} wells in 384-Well Plate...')

        for well, re in zip(dests, reagent):
            pip.aspirate(vol, re)
            pip.aspirate(2, re.top())
            pip.dispense(vol+2, well.top(-3))
            pip.blow_out()
            # p20.touch_tip()

        pip.drop_tip()

    # function for dropping tips in old tip rack
    tipNum = 0

    def drop_tip_rack():
        """
        This function drops used tip in empty tiprack.
        """
        nonlocal tipNum

        pip.drop_tip(tipLocs[tipNum])
        tipNum += 1

    # Transfer 8.5uL of water to corresponding wells
    mm_creation(water, 8.5, 'water')

    # Transfer 1.5uL of Primer/Probe Mix to corresponding wells
    mm_creation(primer, 1.5, 'Primer/Probe Mix')

    # Transfer 5uL of Master Mix to corresponding wells
    mm_creation(mm, 5, 'Master Mix')

    # Transfer samples to wells with mastermix
    protocol.comment('\nTransferring samples to plate...')
    for src, dest, in zip(samps, dests):
        pip.pick_up_tip()

        pip.mix(2, 5, src)
        pip.aspirate(5, src)
        pip.dispense(5, dest)
        pip.mix(3, 10, dest)
        # pip.blow_out(dest.top(-2))
        # pip.touch_tip(dest)

        if tipTrash:
            pip.drop_tip()
        else:
            drop_tip_rack()

    protocol.comment('\nProtocol is complete!')
