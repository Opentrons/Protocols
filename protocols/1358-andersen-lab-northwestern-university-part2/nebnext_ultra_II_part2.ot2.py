from opentrons import labware, instruments, robot

"""
Part 2 - End Prep of cDNA Library, Adaptor Ligation
"""

# custom labware
pcr_plate_name = 'biorad-hardshell-semiskirted-96-PCR'
mag_plate_name = 'biorad-hardhsell-semiskirted-96-PCR-with-magnet'

for plate_name in [pcr_plate_name, mag_plate_name]:
    if plate_name not in labware.list():
        labware.create(
            plate_name,
            grid=(12, 8),
            spacing=(9, 9),
            diameter=5.5,
            depth=20.75)

# labware setup
pcr_plate = labware.load(pcr_plate_name, '1')
trough = labware.load('trough-12row', '2')
trough2 = labware.load('trough-12row', '3')
mag_plate = labware.load(mag_plate_name, '4')

tipracks_m10 = [labware.load('tiprack-10ul', slot)
                for slot in ['10', '11']]
tipracks_m300 = [labware.load('tiprack-200ul', slot)
                 for slot in ['5', '6', '7', '8', '9']]

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

m300_tip_count = 0
m10_tip_count = 0
pcr_loc = [col for col in pcr_plate.cols()]
mag_loc = [col for col in mag_plate.cols()]


def update_m300_tip_count(num):
    global m300_tip_count
    m300_tip_count += num
    if m300_tip_count == 12 * len(tipracks_m300):
        robot.pause("Your P300 tips have run out, please refill the tip racks \
        in slot 5, 6, 7, 8, and 9. Resume after you have finished.")
        m300.reset_tip_tracking()
        m300.start_at_tip(tipracks_m300[0].cols('1'))
        m300_tip_count = 0


def update_m10_tip_count(num):
    global m10_tip_count
    m10_tip_count += num
    if m10_tip_count == 12 * len(tipracks_m10):
        robot.pause("Your P10 tips have run out, please refill the tip racks \
        in slot 10, and 11. Resume after you have finished.")
        m10.reset_tip_tracking()
        m10.start_at_tip(tipracks_m10[0].cols('1'))
        m10_tip_count = 0


# Transfer 7 uL NEBNext Ultra II End Prep Reaction Buffer to plate
m10.transfer(7, end_prep_reaction_buffer, [loc[0].top() for loc in pcr_loc])
update_m10_tip_count(1)

# Transfer 3 uL NEBNext Ultra II End Prep Enzyme to plate
for loc in pcr_loc:
    m10.pick_up_tip()
    m10.transfer(3, end_prep_enzyme, loc, new_tip='never')
    m10.mix(10, 10, loc)
    m10.blow_out(loc)
    m10.drop_tip()
    update_m10_tip_count(1)

robot.pause("Place the plate in the thermal cycler. Place it back in slot 1.")

# Transfer 2.5 uL Diluted Adapter to plate
m10.distribute(2.5, diluted_adapter, [loc[0].top() for loc in pcr_loc])
update_m10_tip_count(1)

# Transfer 1 uL NEBNext Ligation Enhancer to plate
m10.distribute(1, ligation_enhancer, [loc[0].top() for loc in pcr_loc])
update_m10_tip_count(1)

# Transfer 30 uL of NEBNext Ultra II Ligation Master Mix to plate
for loc in pcr_loc:
    m300.pick_up_tip()
    m300.transfer(30, ligation_mastermix, loc, new_tip='never')
    m300.mix(10, 80, loc)
    m300.blow_out(loc)
    m300.drop_tip()
    update_m300_tip_count(1)

robot.pause("Place the plate in the thermal cycler. Place it back in slot 1.")

# Transfer 3 uL USER Enzyme to plate
for loc in pcr_loc:
    m10.pick_up_tip()
    m10.transfer(3, USER_enzyme, loc, new_tip='never')
    m10.mix(20, 10, loc)
    m10.blow_out(loc)
    m10.drop_tip()
    update_m10_tip_count(1)

robot.pause("Place the plate in the thermal cycler. Place it back in slot 1.")

# Transfer 87 uL oligo beads to plate on the MagDeck
for loc in pcr_loc:
    m300.pick_up_tip()
    m300.transfer(87, oligo_beads, loc, new_tip='never')
    m300.mix(10, 50, loc)
    m300.blow_out(loc)
    m300.drop_tip()
    update_m300_tip_count(1)

robot.pause("Incubate the plate for 5 minutes. Place the plate on the magnet \
in slot 4. Resume after solution becomes clear.")

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

robot.pause("Air dry beads for 5 minutes. Place plate in slot 1.")

# Transfer 17 uL TE Buffer to plate
for loc in pcr_loc:
    m10.pick_up_tip()
    m10.transfer(17, TE_buffer, loc, new_tip='never')
    m10.mix(10, 10, loc)
    m10.blow_out(loc)
    m10.drop_tip()
    update_m10_tip_count(1)

robot.pause("Place the plate on the magnet in slot 4. Place a new clean plate \
in slot 1. Resume after solution becomes clear.")

# Transfer supernatant to new plate in slot 1
for source, dest in zip(mag_loc, pcr_loc):
    m300.pick_up_tip()
    m300.transfer(30, source, dest, new_tip='never')
    m300.blow_out(dest)
    m300.drop_tip()
    update_m300_tip_count(1)
