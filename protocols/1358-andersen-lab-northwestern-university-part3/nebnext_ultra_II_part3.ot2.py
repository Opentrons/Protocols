from opentrons import labware, instruments, robot

"""
Part 3 - PCR Enrichment
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
oligo_beads = trough.wells('A1')
ethanol = trough.wells('A2')
TE_buffer = trough.wells('A3')


m300_tip_count = 0
m10_tip_count = 0
pcr_loc = [col for col in pcr_plate.cols()]
mag_loc = [col for col in mag_plate.cols()]


def update_m300_tip_count(num):
    global m300_tip_count
    m300_tip_count += num
    if m300_tip_count == 12 * len(tipracks_m300):
        print('Reset p300 tip racks')
        robot.pause("Your P300 tips have run out, please refill the tip racks \
        in slot 5, 6, 7, 8, and 9. Resume after you have finished.")
        m300.reset_tip_tracking()
        m300.start_at_tip(tipracks_m300[0].cols('1'))
        m300_tip_count = 0


def update_m10_tip_count(num):
    global m10_tip_count
    m10_tip_count += num
    if m10_tip_count == 12 * len(tipracks_m10):
        print('Reset p10 tip racks')
        robot.pause("Your P10 tips have run out, please refill the tip racks \
        in slot 10, and 11. Resume after you have finished.")
        m10.reset_tip_tracking()
        m10.start_at_tip(tipracks_m10[0].cols('1'))
        m10_tip_count = 0


# Mix content in plate in slot 1
for loc in pcr_loc:
    m10.pick_up_tip()
    m10.mix(20, 10, loc)
    m10.drop_tip()
    update_m10_tip_count(1)

robot.pause("Place the plate in the thermal cycler. Place the plate on the \
MagDeck after the program is complete.")

# Transfer 45 uL Oligo Beads to mag_plate
for loc in mag_loc:
    m300.pick_up_tip()
    m300.transfer(45, oligo_beads, loc, new_tip='never')
    m300.mix(10, 30, loc)
    m300.blow_out(loc)
    m300.drop_tip()
    update_m300_tip_count(1)

robot.pause("Incubate the plate for 5 minutes. Place the plate on the magnet \
in slot 4. Resume after the solution becomes clear.")

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

robot.pause("Air dry the beads for 5 minutes. Place the plate back to slot 1.")

# Suspend beads in 17 uL TE buffer
for loc in pcr_loc:
    m10.pick_up_tip()
    m10.transfer(17, TE_buffer, loc, new_tip='never')
    m10.mix(10, 10, loc)
    m10.blow_out(loc)
    m10.drop_tip()
    update_m10_tip_count(1)

robot.pause("Put the place on the magnet in slot 4. Put a clean plate in slot \
1. Resume when the solution is clear.")

# Transfer supernatant to new plate
for source, dest in zip(mag_loc, pcr_loc):
    m300.pick_up_tip()
    m300.transfer(30, source, dest, new_tip='never')
    m300.blow_out(dest)
    m300.drop_tip()
    update_m300_tip_count(1)
