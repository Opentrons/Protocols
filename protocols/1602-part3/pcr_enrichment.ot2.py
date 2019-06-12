from opentrons import labware, instruments, modules, robot

metadata = {
    'protocolName': 'PCR Enrichment',
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
oligo_beads = trough.wells('A1')
ethanol = trough.wells('A2')
TE_buffer = trough.wells('A3')


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

    # Mix content in plate in slot 1
    for loc in mag_loc:
        m10.pick_up_tip()
        m10.mix(20, 10, loc)
        m10.drop_tip()
        update_m10_tip_count(1)

    robot.pause("Place the plate in the thermal cycler. Place the plate back "
                "on the magdeck when finished")

    # Transfer 45 uL Oligo Beads to mag_plate
    for loc in mag_loc:
        m300.pick_up_tip()
        m300.transfer(45, oligo_beads, loc, new_tip='never')
        m300.mix(10, 25, loc)
        m300.blow_out(loc)
        m300.drop_tip()
        update_m300_tip_count(1)

    m300.delay(minutes=5)
    robot._driver.run_flag.wait()
    robot.pause("Spin down the plate. Place the plate back on the magdeck "
                "when finished.")

    robot._driver.run_flag.wait()
    magdeck.engage()

    # Discard 95 uL supernatant from plate
    for loc in mag_loc:
        m300.transfer(95, loc, m300.trash_container.top())
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

    # Suspend beads in 17 uL TE buffer
    for loc in mag_loc:
        m10.pick_up_tip()
        m10.transfer(17, TE_buffer, loc, new_tip='never')
        m10.mix(10, 10, loc)
        m10.blow_out(loc)
        m10.drop_tip()
        update_m10_tip_count(1)

    magdeck.engage()
    m10.delay(minutes=5)
    robot._driver.run_flag.wait()
    robot.pause("Place a fresh plate in slot 3. Resume when the solution is "
                "clear.")

    # Transfer supernatant to new plate
    for source, dest in zip(mag_loc, new_loc):
        m300.pick_up_tip()
        m300.transfer(20, source, dest, new_tip='never')
        m300.blow_out(dest)
        m300.drop_tip()
        update_m300_tip_count(1)
