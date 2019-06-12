from opentrons import labware, instruments, modules, robot

metadata = {
    'protocolName': 'End Prep of cDNA Library, Adaptor Ligation',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# labware and modules
magdeck = modules.load('magdeck', '1')
mag_plate = labware.load('biorad-hardshell-96-PCR', '1', share=True)
trough = labware.load('trough-12row', '2')
new_plate = labware.load('biorad-hardshell-96-PCR', '3', 'fresh plate')

tipracks_m10 = [labware.load('tiprack-10ul', slot)
                for slot in ['9', '10', '11']]
tipracks_m300 = [labware.load('tiprack-200ul', slot)
                 for slot in ['4', '5', '6', '7', '8']]

# pipette setup
m10 = instruments.P10_Multi(
    mount='left',
    tip_racks=tipracks_m10)

m300 = instruments.P300_Multi(
    mount='right',
    tip_racks=tipracks_m300)

# reagent setup
end_prep_reaction_buffer = trough.wells('A1')
end_prep_enzyme = trough.wells('A2')
diluted_adapter = trough.wells('A3')
ligation_enhancer = trough.wells('A4')
ligation_mastermix = trough.wells('A5')
USER_enzyme = trough.wells('A6')
oligo_beads = trough.wells('A7')
ethanol = trough.wells('A8')
TE_buffer = trough.wells('A9')


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
                        "racks in slot 4, 5, 6, 7, and 8. Resume after you "
                        "have finished.")
            m300.reset()
            m300_tip_count = 0

    def update_m10_tip_count(num):
        nonlocal m10_tip_count
        m10_tip_count += num
        if m10_tip_count == 12 * len(tipracks_m10):
            robot.pause("Your P10 tips have run out, please refill the tip "
                        "racks in slot 9, 10, and 11. Resume after you have "
                        "finished.")
            m10.reset()
            m10_tip_count = 0

    # Transfer 7 uL NEBNext Ultra II End Prep Reaction Buffer to plate
    m10.transfer(
        7,
        end_prep_reaction_buffer,
        [loc[0].top() for loc in mag_loc]
        )
    update_m10_tip_count(1)

    # Transfer 3 uL NEBNext Ultra II End Prep Enzyme to plate
    for loc in mag_loc:
        m10.pick_up_tip()
        m10.transfer(3, end_prep_enzyme, loc, new_tip='never')
        m10.mix(10, 10, loc)
        m10.blow_out(loc)
        m10.drop_tip()
        update_m10_tip_count(1)

    robot.pause("Place the plate in the thermal cycler. Place it back on the "
                "magdeck when finished.")

    # Transfer 2.5 uL Diluted Adapter to plate
    m10.distribute(2.5, diluted_adapter, [loc[0].top() for loc in mag_loc])
    update_m10_tip_count(1)

    # Transfer 1 uL NEBNext Ligation Enhancer to plate
    m10.distribute(1, ligation_enhancer, [loc[0].top() for loc in mag_loc])
    update_m10_tip_count(1)

    # Transfer 30 uL of NEBNext Ultra II Ligation Master Mix to plate
    for loc in mag_loc:
        m300.pick_up_tip()
        m300.transfer(30, ligation_mastermix, loc, new_tip='never')
        m300.mix(10, 80, loc)
        m300.blow_out(loc)
        m300.drop_tip()
        update_m300_tip_count(1)

    robot.pause("Place the plate in the thermal cycler. Place it back on the "
                "magdeck when finished.")

    # Transfer 3 uL USER Enzyme to plate
    for loc in mag_loc:
        m10.pick_up_tip()
        m10.transfer(3, USER_enzyme, loc, new_tip='never')
        m10.mix(20, 10, loc)
        m10.blow_out(loc)
        m10.drop_tip()
        update_m10_tip_count(1)

    robot.pause("Place the plate in the thermal cycler. Place it back on the "
                "magdeck when finished.")

    # Transfer 87 uL oligo beads to plate on the MagDeck
    for loc in mag_loc:
        m300.pick_up_tip()
        m300.transfer(87, oligo_beads, loc, new_tip='never')
        m300.mix(10, 50, loc)
        m300.blow_out(loc)
        m300.drop_tip()
        update_m300_tip_count(1)

    m300.delay(minutes=5)
    robot._driver.run_flag.wait()
    magdeck.engage()
    robot.pause("Resume after solution becomes clear.")

    # Discard 183 uL supernatant
    for loc in mag_loc:
        m300.transfer(183, loc, m300.trash_container.top())
        update_m300_tip_count(1)

    # Wash plate with 200 uL 80% Ethanol twice
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

    # Transfer 17 uL TE Buffer to plate
    for loc in mag_loc:
        m10.pick_up_tip()
        m10.transfer(17, TE_buffer, loc, new_tip='never')
        m10.mix(10, 10, loc)
        m10.blow_out(loc)
        m10.drop_tip()
        update_m10_tip_count(1)

    magdeck.engage()
    robot.pause("Place a new clean plate in slot 3. Resume after solution"
                "becomes clear.")

    # Transfer supernatant to new plate in slot 3
    for source, dest in zip(mag_loc, new_loc):
        m300.pick_up_tip()
        m300.transfer(30, source, dest, new_tip='never')
        m300.blow_out(dest)
        m300.drop_tip()
        update_m300_tip_count(1)
