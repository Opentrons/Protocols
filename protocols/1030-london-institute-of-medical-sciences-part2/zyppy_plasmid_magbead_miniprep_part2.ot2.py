from opentrons import labware, instruments, modules, robot

"""
Purification of Plasmid DNA
"""
trough_2row_name = 'trough-2row'
if trough_2row_name not in labware.list():
    labware.create(
        trough_2row_name,
        grid=(2, 1),
        spacing=(54, 0),
        diameter=53,
        depth=39.2)

# labware setup
mag_deck = modules.load('magdeck', '1')
mag_plate = labware.load('96-deep-well', '1', share=True)
plate = labware.load('96-deep-well', '2')
trough_2row_1 = labware.load(trough_2row_name, '3')
trough_2row_2 = labware.load(trough_2row_name, '4')
trough_12row = labware.load('trough-12row', '5')
temp_deck = modules.load('tempdeck', '6')
temp_plate = labware.load('96-deep-well', '6', share=True)


# reagent setup
lysis_buffer = trough_12row.wells('A1')
clear_beads = trough_12row.wells('A2')
bind_beads = trough_12row.wells('A3')
zyppy_elution_buffer = trough_12row.wells('A4')

neut_buffer = trough_2row_1.wells('A2')
endo_wash = trough_2row_2.wells('A1')
zyppy_wash_buffer = trough_2row_2.wells('A2')

tipracks300 = [labware.load('tiprack-200ul', slot)
               for slot in ['7', '8', '9', '10', '11']]


# pipette setup
m300 = instruments.P300_Multi(
    mount='left',
    tip_racks=tipracks300)


def vortex_wells(mix_locations, mix_reps):
    m300.set_flow_rate(aspirate=300, dispense=550)
    for well in mix_locations:
        if not m300.tip_attached:
            m300.pick_up_tip()
        m300.mix(mix_reps, 300, well)
        m300.return_tip()
    m300.set_flow_rate(aspirate=150, dispense=300)


# define deep block dispense locations
block_loc = [well for well in mag_plate.rows(0)]
block_top_loc = [well.top() for well in mag_plate.rows(0)]

# Dispense 100 μl of Deep Blue Lysis Buffer to each well containing culture and
# vortex for 10 seconds
m300.pick_up_tip()
vortex_tip = m300.current_tip()
m300.distribute(100, lysis_buffer, block_top_loc, new_tip='never')
vortex_wells(block_loc, 10)

# Let sit for 5 minutes
m300.delay(minutes=5)

# Dispense 450 μl of Neutralization Buffer (yellow) and vortex for 45 seconds
m300.pick_up_tip()
new_tip = next(m300.tip_rack_iter)
m300.transfer(450, neut_buffer, block_top_loc, new_tip='once')
m300.start_at_tip(vortex_tip)
vortex_wells(block_loc, 30)

# Dispense 50 µl MagClearing Beads and vortex for 10 seconds.
m300.start_at_tip(new_tip)
m300.pick_up_tip()
lysate_tip = m300.current_tip()
m300.transfer(50, clear_beads, block_loc, new_tip='always',
              mix_after=(10, 300), trash=False)

# turn on Magnetic Module for 5 minutes
mag_deck.engage(height=15)
m300.delay(minutes=5)

# From a depth of about half the length of the well, aspirate and transfer the
# cleared lysate (~750 µl) to a Collection Plate.
plate_loc = [well for well in plate.rows(0)]
m300.start_at_tip(lysate_tip)
for source, dest in zip(block_loc, plate_loc):
    m300.transfer(750, (source, source.center()), dest)

mag_deck.disengage()
robot.pause("Remove and discard the plate on the MagDeck. Place the plate in \
slot 5 on the MagDeck.")

# Dispense 30 µl of MagBinding Beads1 to each well of the Collection Plate and
# vortex to mix. Incubate at room temperature for 10 minutes, each 30 seconds
# vortex for 5 seconds to re-suspend MagBinding Beads. Transfer the Collection
# Plate onto the magnetic stand for 5 minutes until beads pellet. With the
# Collection Plate still on the magnetic stand, aspirate and discard cleared
# lysates.
m300.pick_up_tip()
discard_tip = m300.current_tip()
m300.transfer(30, bind_beads, block_loc, new_tip='always',
              mix_after=(30, 300), trash=False)
for cycle in range(5):
    m300.delay(minutes=1)
    m300.start_at_tip(new_tip)
    for well in block_loc:
        m300.pick_up_tip()
        m300.mix(5, 300, well)
        m300.return_tip()

mag_deck.engage(height=15)
m300.delay(minutes=5)

m300.start_at_tip(discard_tip)
for well in block_loc:
    m300.transfer(750, well, m300.trash_container.top())

mag_deck.disengage()

# Transfer Collection Plate off magnetic stand and dispense 200 μl of Endo-Wash
# Buffer to each well of the plate. Vortex for 30 seconds to re-suspend beads
# and then transfer Collection Plate back onto magnetic stand for 2 minutes.
# With the Collection Plate still on the magnetic stand, aspirate and discard
# Endo-Wash Buffer
m300.pick_up_tip()
new_tip = m300.current_tip()
m300.transfer(200, endo_wash, block_loc, new_tip='always',
              mix_after=(20, 300), trash=False)

mag_deck.engage(height=15)
m300.delay(minutes=2)

m300.start_at_tip(new_tip)
for well in block_loc:
    m300.transfer(200, well, m300.trash_container.top())

robot.pause("Please replace all of your P300 tipracks. Resume when that all \
tipracks have been replenished.")
m300.reset_tip_tracking()
m300.start_at_tip(tipracks300[0].cols(0))

# Transfer Collection Plate off magnetic stand and dispense 400 μl Zyppy™ Wash
# Buffer to each well. Vortex for 30 seconds to re-suspend beads and then
# transfer Collection Plate back onto magnetic stand for 2 minutes. With the
# Collection Plate still on the magnetic stand, aspirate and discard Zyppy™
# Wash Buffer.
m300.pick_up_tip()
start_tip = m300.current_tip()
for cycle in range(2):
    if not m300.tip_attached:
        m300.start_at_tip(start_tip)
        m300.pick_up_tip()
    m300.transfer(400, zyppy_wash_buffer, block_top_loc, trash=False)
    for index, well in enumerate(block_loc):
        m300.pick_up_tip()
        if index == 0:
            discard_tip = m300.current_tip()
        m300.mix(15, 300, well)
        m300.return_tip()

    mag_deck.engage(height=15)
    m300.delay(minutes=5)

    m300.start_at_tip(discard_tip)
    for well in block_loc:
        m300.transfer(400, well, m300.trash_container.top(), trash=False)

    mag_deck.disengage()

# For the removal of residual ethanol, transfer the Collection Plate onto a
# heating element (65°C) for 30 minutes.
temp_deck.set_temperature(65)
robot.pause("Remove the Collection Plate from the MagDeck and place it on \
the TempDeck for ~30 minutes, or until the bead pellets no longer appear \
glossy.")

m300.pick_up_tip()
start_tip = m300.current_tip()
for well in block_loc:
    if not m300.tip_attached:
        m300.pick_up_tip()
    m300.transfer(40, zyppy_elution_buffer, well, mix_after=(10, 40),
                  trash=False)

for cycle in range(5):
    m300.start_at_tip(start_tip)
    for well in block_loc:
        m300.pick_up_tip()
        m300.mix(20, 40)
        m300.return_tip()

robot.pause("Remove the Collection Plate from the TempDeck and plate it on \
the MagDeck. Place the Elution Plate in slot 2.")

mag_deck.engage(height=15)
m300.delay(minutes=2)

plate_loc = [well for well in plate.rows(0)]
m300.transfer(30, block_loc, plate_loc, new_tip='always')
