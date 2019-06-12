from opentrons import labware, instruments, modules, robot

metadata = {
    'protocolName': 'mRNA Isolation, cDNA Synthesis',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# labware and modules
magdeck = modules.load('magdeck', '1')
mag_plate = labware.load('biorad-hardshell-96-PCR', '1', share=True)
trough = labware.load('trough-12row', '2')
trough2 = labware.load('trough-12row', '3')
new_plate = labware.load('biorad-hardshell-96-PCR', '4', 'fresh plate')

tipracks_m10 = [labware.load('tiprack-10ul', slot)
                for slot in ['10', '11']]
tipracks_m300 = [labware.load('opentrons-tiprack-300ul', slot)
                 for slot in ['5', '6', '7', '8', '9']]

# pipette setup
m10 = instruments.P10_Multi(
    mount='left',
    tip_racks=tipracks_m10)

m300 = instruments.P300_Multi(
    mount='right',
    tip_racks=tipracks_m300)

# reagent setup
oligo_beads = trough.wells('A1')
wash_buffer = trough.wells('A2', to='A4')
tris_buffer = trough.wells('A5')
binding_buffer = trough.wells('A6')
first_strand_mastermix = trough.wells('A7')
water = trough.wells('A8')
first_strand_enzymemix = trough.wells('A9')
second_strand_reaction_buffer = trough.wells('A10')
second_strand_enzymemix = trough.wells('A11')
ethanol = trough.wells('A12')
TE_buffer = trough2.wells('A1')


def run_custom_protocol(
        sample_columns_separated_by_commas: str = '1,2,3,4,5,6,7,8,9,10,11,12'
):
    m300_tip_count = 0
    m10_tip_count = 0

    cols = [col.strip()
            for col in sample_columns_separated_by_commas.split(',')]
    # check input columns
    for col in cols:
        if int(col) < 1 or int(col) > 12:
            raise Exception('Invalid column input.')

    mag_loc = [mag_plate.columns(col) for col in cols]
    new_loc = [new_plate.columns(col) for col in cols]

    def update_m300_tip_count(num):
        nonlocal m300_tip_count
        m300_tip_count += num
        if m300_tip_count == 12 * len(tipracks_m300):
            robot.pause("Your P300 tips have run out, please refill the tip "
                        "racks in slot 5, 6, 7, 8, and 9. Resume after you "
                        "have finished.")
            m300.reset()
            m300_tip_count = 0

    def update_m10_tip_count(num):
        nonlocal m10_tip_count
        m10_tip_count += num
        if m10_tip_count == 12 * len(tipracks_m10):
            robot.pause("Your P10 tips have run out, please refill the tip "
                        "racks in slot 10, and 11. Resume after you have "
                        "finished.")
            m10.reset()
            m10_tip_count = 0

    # Transfer 50 uL oligo beads to reaction plate
    for loc in mag_loc:
        m300.pick_up_tip()
        m300.transfer(50, oligo_beads, loc, new_tip='never')
        m300.mix(10, 25, loc)
        m300.blow_out(loc)
        m300.drop_tip()
        update_m300_tip_count(1)

    robot.pause("Place your PCR plate in the thermoycler. Place it back on "
                "the magnetic deck when you are finished.")

    # Resuspend beads in reaction plate
    for loc in mag_loc:
        m300.pick_up_tip()
        m300.mix(10, 30, loc[0].bottom(0.5))
        m300.drop_tip()
        update_m300_tip_count(1)

    m300.delay(minutes=5)

    robot._driver.run_flag.wait()
    magdeck.engage()
    m300.delay(minutes=1)

    # Discard 50 uL supernatant from reaction plate
    for loc in mag_loc:
        m300.transfer(50, loc, m300.trash_container.top())
        update_m300_tip_count(1)

    magdeck.disengage()

    # Wash reaction plate with 200 uL Wash Buffer twice
    for wash_cycle in range(2):
        for loc in mag_loc:
            m300.transfer(
                200,
                wash_buffer[wash_cycle],
                loc,
                mix_after=(6, 100)
                )
            update_m300_tip_count(1)

        magdeck.engage()
        m300.delay(minutes=1)

        for loc in mag_loc:
            m300.transfer(200, loc, m300.trash_container.top())
            update_m300_tip_count(1)
        magdeck.disengage()

    # Transfer 50 uL Tris buffer to reaction plate
    for loc in mag_loc:
        m300.pick_up_tip()
        m300.transfer(50, tris_buffer, loc, new_tip='never')
        m300.mix(6, 25, loc)
        m300.drop_tip()
        update_m300_tip_count(1)

    robot.pause("Place your PCR plate in the thermocycler. Place it back on "
                "the magnetic deck when you are finished.")

    # Transfer 50 uL Binding Buffer to reaction plate
    for loc in mag_loc:
        m300.pick_up_tip()
        m300.transfer(50, binding_buffer, loc, new_tip='never')
        m300.mix(10, 50, loc)
        m300.drop_tip()
        update_m300_tip_count(1)

    m300.delay(minutes=5)
    robot._driver.run_flag.wait()
    magdeck.engage()
    m300.delay(minutes=2)
    robot._driver.run_flag.wait()
    robot.pause("Resume when solution is clear.")

    # Discard 100 uL supernatant from reaction plate
    for loc in mag_loc:
        m300.transfer(100, loc, m300.trash_container.top())
        update_m300_tip_count(1)

    magdeck.disengage()

    # Wash reaction plate with 200 uL Wash Buffer
    for loc in mag_loc:
        m300.pick_up_tip()
        m300.transfer(200, wash_buffer, loc, new_tip='never')
        m300.mix(10, 100, loc)
        m300.drop_tip()
        update_m300_tip_count(1)

    robot.pause("Spin down your plate. Place the plate back on the magnetic "
                "deck before resuming.")
    robot._driver.run_flag.wait()
    magdeck.engage()
    m300.delay(minutes=5)
    robot._driver.run_flag.wait()
    robot.pause("Resume when solution is clear.")

    # Discard 200 uL supernatant from reaction plate
    for loc in mag_loc:
        m300.transfer(200, loc, m300.trash_container.top())
        update_m300_tip_count(1)

    magdeck.disengage()

    # Dispense 11.5 uL First Strand Synthesis Master Mix to reaction plate
    for loc in mag_loc:
        m10.pick_up_tip()
        m10.transfer(
            11.5,
            first_strand_mastermix,
            loc.top(),
            blow_out=True,
            new_tip='never'
            )
        m10.mix(10, 5, loc)
        m10.drop_tip()
        update_m10_tip_count(1)

    robot.pause("Place your PCR plate in the thermocycler and spin down. "
                "Place it back on the magnetic deck when finished.")

    robot._driver.run_flag.wait()
    magdeck.engage()
    robot.pause("Resume after solution in plate is clear.")

    # Transfer 10 uL supernatant to new plate in slot 1
    for source, dest in zip(mag_loc, new_loc):
        m10.transfer(10, source, dest)
        update_m10_tip_count(1)

    # Add 8 uL Nuclease Free Water to plate
    m10.pick_up_tip()
    for loc in new_loc:
        m10.transfer(8, water, loc[0].top(), new_tip='never')
        m10.blow_out(loc[0].top())
    m10.drop_tip()
    update_m10_tip_count(1)

    # Add 2 uL First Strand Synthesis enzyme mix to plate
    for loc in new_loc:
        m10.pick_up_tip()
        m10.transfer(2, first_strand_enzymemix, loc, new_tip='never')
        m10.mix(10, 10, loc)
        m10.blow_out(loc)
        m10.drop_tip()
        update_m10_tip_count(1)

    robot.pause("Place the plate in the thermocycler. Place the plate back in "
                "slot 4when finished.")

    # Add 8 uL NEBNext Second Strand Synthesis Reaction Buffer to plate
    m10.pick_up_tip()
    for loc in new_loc:
        m10.transfer(
            8, second_strand_reaction_buffer, loc[0].top(), new_tip='never')
        m10.blow_out(loc[0].top())
    m10.drop_tip()
    update_m10_tip_count(1)

    # Add 2 uL NEBNext Second Strand Synthesis Enzyme Mix to plate
    m10.pick_up_tip()
    for loc in new_loc:
        m10.transfer(2, second_strand_enzymemix, loc[0].top(), new_tip='never')
        m10.blow_out(loc[0].top())
    m10.drop_tip()
    update_m10_tip_count(1)

    # Transfer 48 uL Nuclease Free Water to plate
    for loc in new_loc:
        m300.pick_up_tip()
        m300.transfer(48, water, loc, new_tip='never')
        m300.mix(10, 30, loc)
        m300.drop_tip()
        update_m300_tip_count(1)

    robot.pause("Place the plate in the thermoycler. Place the plate back in "
                "slot 4 when the program is finished.")

    # Transfer 144 uL oligo_beads to plate
    for loc in new_loc:
        m300.pick_up_tip()
        m300.transfer(144, oligo_beads, loc, new_tip='never')
        m300.mix(10, 100, loc)
        m300.drop_tip()
        update_m300_tip_count(1)

    robot.pause("Transfer the plate in slot 4 to the magnetic deck.")

    robot._driver.run_flag.wait()
    magdeck.engage()
    m300.delay(minutes=1)

    # Discard 224 uL supernatant from plate
    for loc in mag_loc:
        m300.transfer(224, loc, m300.trash_container.top())
        update_m300_tip_count(1)

    # Wash beads with 200 uL 80% Ethanol twice
    for wash_cycle in range(2):
        m300.transfer(200, ethanol, [loc[0].top() for loc in mag_loc])
        update_m300_tip_count(1)
        m300.delay(seconds=30)
        for loc in mag_loc:
            m300.transfer(200, loc, m300.trash_container.top())
            update_m300_tip_count(1)

    m300.delay(minutes=5)
    robot._driver.run_flag.wait()
    magdeck.disengage()

    # Transfer 53 uL 0.1X TE Buffer to plate
    for loc in mag_loc:
        m300.pick_up_tip()
        m300.transfer(53, TE_buffer, loc, new_tip='never')
        m300.mix(10, 25, loc)
        m300.blow_out()
        m300.drop_tip()
        update_m300_tip_count(1)

    magdeck.engage()
    robot.pause("Put a clean plate in slot 4. Resume when solution is clear.")

    # Transfer 50 uL supernatant to new plate
    for source, dest in zip(mag_loc, new_loc):
        m300.pick_up_tip()
        m300.transfer(50, source, dest, new_tip='never')
        m300.blow_out(dest)
        m300.drop_tip()
        update_m300_tip_count(1)
