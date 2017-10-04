from opentrons import containers, instruments

p300rack = containers.load('tiprack-200ul', 'A1', 'p300rack')
trough = containers.load('trough-12row', 'E1', 'trough')
plate = containers.load('96-PCR-flat', 'C1', 'plate')
top_plate = containers.load('96-PCR-flat', 'C2', 'top_plate')
trash = containers.load('point', 'B2', 'trash')

p300_multi = instruments.Pipette(
    name="p300_multi",
    trash_container=trash,
    tip_racks=[p300rack],
    min_volume=50,
    max_volume=300,
    axis="a",
    channels=8
)

# Reagent locations in trough:

# trough row 1 = buffer
# trough row 2 = Ph-Ch-Iso-Amyl mix
# trough row 3 = isopropanol
# trough row 4 = ethanol


# Transfer 300uL of L buffer from trough to 96 well deep plate with same tips
p300_multi.transfer(300, trough('A1'), plate.rows('1', to='12'))

# Transfer 180uL of Ph-Ch-Iso-Amyl mixture to 96 well deep plate
p300_multi.transfer(180, trough('A2'), plate.rows('1', to='12'))

# Transfer top layer (200uL) from 96 well deep plate to new 96 deep well plate
p300_multi.transfer(
    200, plate.rows('1', to='12').top(-2), top_plate.rows('1', to='12'))

# Transfer 280uL of isopropanol to this new plate with top layer
p300_multi.transfer(280, trough('A3'), top_plate.rows('1', to='12'))

# Remove the isopropanol and discard.
p300_multi.transfer(280, top_plate.rows('1', to='12').top(-2), trash)

# Transfer 450uL of ethanol and wash the pellet.
p300_multi.transfer(
    450, trough('A4'), top_plate.rows('1', to='12')).mix(5, 300)

# Remove the ethanol and discard
p300_multi.transfer(450, top_plate.rows('1', to='12').top(-2), trash)
