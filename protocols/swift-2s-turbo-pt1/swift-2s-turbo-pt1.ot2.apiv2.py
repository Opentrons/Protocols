metadata = {
    'protocolName': 'Swift 2S Turbo DNA Library Kit Protocol: Part 1/3 - \
    Enzymatic Prep & Ligation',
    'author': 'Opentrons <protocols@opentrons.com>',
    'source': 'Protocol Library',
    'apiLevel': '2.1'
}


def run(protocol):
    [pip_type, tip_name, samps] = get_values(  # noqa: F821
    'pip_type', 'tip_name', 'samps')

    # Labware Setup
    small_tips = protocol.load_labware(tip_name, '5')

    small_pip = protocol.load_instrument(
        pip_type, 'left', tip_racks=[small_tips])

    tempdeck = protocol.load_module('Temperature Module', '1')

    cool_reagents = tempdeck.load_labware(
        'opentrons_24_aluminumblock_generic_2ml_screwcap',
        'Opentrons 24-Well Aluminum Block')

    reaction_plate = protocol.load_labware(
        'opentrons_96_aluminumblock_nest_wellplate_100ul', '3')

    # Reagent Setup
    enzymatic_prep_mm = cool_reagents.wells_by_name()['A1']
    ligation_mm = cool_reagents.wells_by_name()['A2']

    # Destination of input DNA samples and samples on the magnetic module
    enzymatic_prep_samples = reaction_plate.columns()[0]
    if samps == '16':
        enzymatic_prep_samples += reaction_plate.columns()[1]

    # Actively cool the samples and enzymes
    tempdeck.set_temperature(4)

    # Make sure to vortex mastermix right before the run
    # Custom transfer function for accounting for various volumes
    tip_count = 0

    def pick_up():
        nonlocal tip_count

        if tip_count == 96:
            small_pip.home()
            protocol.pause('Out of tips. Please replace tips in slot 5 and \
            click RESUME.')
            small_tips.reset()

        small_pip.pick_up_tip()

        tip_count += 1

    def vol_trans(vol, src, dest):
        if pip_type[1:3] == '50':
            if not small_pip.hw_pipette['has_tip']:
                pick_up()
            small_pip.transfer(vol, src, dest, new_tip='never')
        else:
            if tip_name[-4:-2] == '20':
                if vol < 20:
                    pick_up()
                    small_pip.transfer(vol, src, dest, new_tip='never')
                else:
                    while vol >= 15:
                        if not small_pip.hw_pipette['has_tip']:
                            pick_up()
                        small_pip.transfer(15, src, dest, new_tip='never')
                        vol -= 15
                        if vol >= 15:
                            small_pip.drop_tip()
            else:
                while vol > 8:
                    if not small_pip.hw_pipette['has_tip']:
                        pick_up()
                    small_pip.transfer(8, src, dest, new_tip='never')
                    small_pip.drop_tip()
                    vol -= 8
                pick_up()
                small_pip.transfer(vol, src, dest, new_tip='never')

    # Dispense Enzymatic Prep Master Mix to the samples
    for well in enzymatic_prep_samples:
        vol_trans(10.5, enzymatic_prep_mm.bottom(0.2), well.top(-12))
        small_pip.blow_out()
        small_pip.mix(2, small_pip.max_volume/2, well.top(-13.5))
        small_pip.move_to(well.top(-12))
        protocol.delay(seconds=0.5)
        small_pip.blow_out()
        small_pip.drop_tip()

    # Run Enzymatic Prep Profile
    protocol.pause('Enzymatic prep complete. Please place sample plate in \
    thermocycler and run program according to Swift 2S Turbo manual. When \
    complete, return samples to OT-2 deck for ligation prep and click RESUME.')

    # Transfer Ligation Master Mix to the samples

    pick_up()
    small_pip.mix(10, small_pip.max_volume/2, ligation_mm)
    small_pip.blow_out(ligation_mm.top())

    for well in enzymatic_prep_samples:
        vol_trans(30, ligation_mm, well.top(-7))
        small_pip.blow_out()
        small_pip.mix(2, small_pip.max_volume/2, well.top(-13.5))
        small_pip.blow_out(well.top(-7))
        small_pip.drop_tip()

    protocol.comment("Add samples to the thermocycler for ligation. \
    Temp deck will remain on at 4C")
