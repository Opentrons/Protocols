from opentrons import labware, instruments, modules

mag_deck = modules.load('magdeck', '1')
temp_deck = modules.load('tempdeck', '7')

trough = labware.load('trough-12row', '3')
mag_plate = labware.load('96-flat', '1', share=True)
temp_plate = labware.load('96-flat', '7', share=True)
fresh_plate = labware.load('96-flat', '2')
tiprack1 = labware.load('tiprack-200ul', '4')
tiprack2 = labware.load('tiprack-200ul', '5')
tiprack3 = labware.load('tiprack-200ul', '6')
tiprack4 = labware.load('tiprack-200ul', '8')
tiprack5 = labware.load('tiprack-200ul', '9')
tiprack6 = labware.load('tiprack-200ul', '11')
liquid_trash = labware.load('point', '10')


beads = trough.wells('A1')
wash_solution = trough.wells('A2')
elution_solution = trough.wells('A3')

m300 = instruments.P300_Multi(
    mount='left',
    tip_racks=[tiprack1, tiprack2, tiprack3, tiprack4, tiprack5, tiprack6])


# Define location to aspirate from when mag deck is engaged
mag_plate_loc = [well.bottom(1)
                 for cols in [mag_plate.cols()] for well in cols]

"""
Initiation:
Place sample plate in the MagDeck, place 300 uL 96-well place on TempDeck
"""
temp_deck.set_temperature(70)

"""
Binding gDNA to beads
"""

# Transfer beads to plate, mix 20x, return tips to reuse
for col in mag_plate.cols():
    m300.pick_up_tip()
    m300.transfer(440, beads, col, new_tip='never')
    m300.mix(20, 300)
    m300.return_tip()

m300.delay(minutes=5)

# Mix 20x, return tips to reuse
m300.reset_tip_tracking()
for col in mag_plate.cols():
    m300.pick_up_tip()
    m300.mix(20, 300, col)
    m300.return_tip()

m300.delay(minutes=5)

# Switch on magnet
mag_deck.engage()

m300.delay(minutes=5)

# Remove supernatent
m300.reset_tip_tracking()
for col in mag_plate_loc:
    m300.transfer(940, col, liquid_trash, new_tip='once')


"""
Wash the DNA binding beads
"""

# Wash the beads 3x, using a new tip rack each wash
for wash_vol in [1000, 1000, 500]:

    mag_deck.disengage()

    # Transfer wash solution to plate, mix 20x, return tips to reuse
    for index, col in enumerate(mag_plate.cols):
        m300.pick_up_tip()

        # Define tip pick up location for ethanol removal
        if index == 0:
            start_loc = m300.current_tip()

        m300.transfer(wash_vol, wash_solution, col, new_tip='never')
        m300.mix(20, 30)
        m300.return_tip()
        # if transferred to the last column, does not pick up new tips

    mag_deck.engage()

    # m300.delay(minutes=5)

    # Set tip pick up location, remove ethanol
    m300.start_at_tip(start_loc)
    for col in mag_plate_loc:
        m300.transfer(wash_vol, col, liquid_trash, new_tip='once')

mag_deck.disengage()


"""
Elute the DNA
"""
for col_index, [mag_col, temp_col] in enumerate(
        zip(mag_plate.cols(), temp_plate.cols())):
    m300.pick_up_tip()
    if col_index == 0:
        start_loc = m300.current_tip()
    m300.transfer(100, elution_solution, mag_col, new_tip='never')
    m300.mix(20, 80)
    m300.transfer(100, mag_col, temp_col, new_tip='never')
    m300.return_tip()

m300.delay(minutes=5)

m300.start_at_tip(start_loc)
for mag_col, temp_col in zip(mag_plate.cols(), temp_plate.cols()):
    m300.transfer(100, temp_col, mag_col, mix_before=(10, 80))

mag_deck.engage()

m300.delay(minutes=5)

m300.transfer(100, mag_plate.cols(), fresh_plate.cols(), new_tip='always')
