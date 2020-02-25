metadata = {
    'protocolName': 'BP Genomics RNA Extraction',
    'author': 'Chaz <chaz@opentrons.com',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.2'
}


def run(protocol):
    [samps, mnt20, m1k] = get_values(  # noqa: F821
    'samps', 'mnt20', 'm1k')

    # load labware and pipettes
    if samps > 16:
        raise Exception('This protocol is in review; the maximum number of \
        supported samples is: 16')
    tips1k = [protocol.load_labware('opentrons_96_filtertiprack_1000ul', '6')]
    # tips20 definition needs to be updated - for current version of p.library
    tips20 = [protocol.load_labware('opentrons_96_tiprack_20ul', '3')]

    p20 = protocol.load_instrument('p20_single_gen2', mnt20, tip_racks=tips20)
    p1k = protocol.load_instrument('p1000_single_gen2', m1k, tip_racks=tips1k)

    magdeck = protocol.load_module('magdeck', '4')
    magplate = magdeck.load_labware(
                'usascientific_96_wellplate_2.4ml_deep', 'Deep Well Plate')
    flatplate = protocol.load_labware(
                'nest_96_wellplate_100ul_pcr_full_skirt', '1', 'Elution Plate')
    trough = protocol.load_labware('nest_12_reservoir_15ml', '5', 'Trough')
    liqwaste = protocol.load_labware(
                'nest_1_reservoir_195ml', '8', 'Liquid Waste')
    waste = liqwaste['A1'].top()  # may need to change
    ie_rna = trough['A1']  # may need to change
    bind1 = trough['A2']
    """
    bind2 = trough['A3']
    bind3 = trough['A4']
    """
    washbuffer = trough['A5']
    ethanol = trough['A7']
    water = trough['A9']

    magsamps = magplate.wells()[:samps]
    elutes = flatplate.wells()[:samps]

    # From nCoV - Add 4ul internal extraction control RNA
    p20.pick_up_tip()
    p20.flow_rate.aspirate = 10
    p20.flow_rate.dispense = 20
    p20.flow_rate.blow_out = 500

    for dest in magsamps:
        p20.transfer(4, ie_rna, dest.top(-2), new_tip='never')
        p20.blow_out(dest.top(-2))

    p20.drop_tip()

    # Step 3 - Mix bind buffer, then add to samples
    p1k.pick_up_tip()
    p1k.mix(10, 800, bind1)
    p1k.blow_out(bind1.top())
    p1k.flow_rate.aspirate = 250  # slow down aspirate/dispense rates
    p1k.flow_rate.dispense = 250

    for dest in magsamps:
        if not p1k.hw_pipette['has_tip']:
            p1k.pick_up_tip()
        p1k.transfer(400, bind1, dest, new_tip='never')
        p1k.mix(5, 800, dest)
        p1k.blow_out(dest.top())
        p1k.drop_tip()

    protocol.comment('Inucbating at room temp for 5 minutes.')
    protocol.delay(minutes=5)

    # Step 4 - engate magdeck for 6 minutes
    magdeck.engage()
    protocol.comment('Incubating on MagDeck for 6 minutes')
    protocol.delay(minutes=6)

    # Step 5 - remove supernatant

    for src in magsamps:
        p1k.transfer(804, src, waste)

    magdeck.disengage()

    def wash_step(src, vol, mtimes):
        for dest in magsamps:
            p1k.pick_up_tip()
            p1k.transfer(vol, src, dest, new_tip='never', air_gap=50)
            p1k.mix(mtimes, 750, dest)
            p1k.blow_out(dest.top())
            p1k.drop_tip()

        magdeck.engage()
        protocol.comment('Incubating on MagDeck for 5 minutes.')
        protocol.delay(minutes=5)

        for src in magsamps:
            p1k.transfer(800, src, waste)

        magdeck.disengage()

    # Step 6, 7, 8
    wash_step(washbuffer, 800, 10)

    # Step 9, 10, 11
    wash_step(ethanol, 800, 4)

    # Additional wash step, if needed

    # Step 19 - allow beads to dry for 10 minutes
    protocol.comment('Allowing beads to air dry for 10 minutes.')
    protocol.delay(minutes=10)

    # Step 20 - Add 40 of nuclease free water and incubate for 2 minutes
    for dest in magsamps:
        p20.pick_up_tip()
        p20.transfer(40, water, dest.top(), new_tip='never')
        p20.mix(10, 20, dest)
        p20.blow_out(dest.top())
        p20.drop_tip()

    protocol.comment('Incubating for 2 minutes.')
    protocol.delay(minutes=2)

    # Step 21 - Transfer elutes to clean plate
    magdeck.engage()
    protocol.comment('Incubating on MagDeck for 2 minutes.')
    protocol.delay(minutes=2)

    for src, dest in zip(magsamps, elutes):
        p20.pick_up_tip()
        p20.transfer(40, src, dest, new_tip='never')
        p20.blow_out(dest.top())
        p20.drop_tip()

    protocol.comment('Congratulations, the protocol is complete. You can store \
    the samples or proceed to the next protocol with the samples.')
