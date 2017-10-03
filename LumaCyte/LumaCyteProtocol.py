from opentrons import containers, instruments

# solutions in trough
trough = containers.load('trough-12row', 'A2')

# tube rack holding reagents
reagents = containers.load('tube-rack-.75ml', 'A1')

# 96 well plates
flat_plate = containers.load('96-PCR-flat', 'C1')
deep_plate = containers.load('96-deep-well', 'C2')

# tip rack for p10 and p50 pipette
tip200_rack = containers.load('tiprack-200ul', 'C3')
tip200_rack2 = containers.load('tiprack-200ul', 'E3')
tip200_rack3 = containers.load('tiprack-200ul', 'E2')

# trash to dispose of tips
trash = containers.load('trash-box', 'A3')

# p200 (20 - 200 uL) (single)
p200single = instruments.Pipette(
    axis='b',
    name='p200',
    max_volume=200,
    min_volume=20,
    channels=1,
    trash_container=trash,
    tip_racks=[tip200_rack])

# p300 (50 - 300 uL) (multi)
p300multi = instruments.Pipette(
    axis='a',
    name='p300',
    max_volume=300,
    min_volume=50,
    channels=8,
    trash_container=trash,
    tip_racks=[tip200_rack2, tip200_rack3])

# medium in trough
medium = trough['A1']

# Add 180 uL of medium from trough/basin to first column of deep 96 well plate.
p300multi.transfer(180, medium, deep_plate.rows('1'))

# Add 450 uL of medium from trough/basin to the next 3 columns (2-4)
# of the same deep 96 well plate.
p300multi.distribute(
    450, medium, deep_plate.rows('2', length=3), new_tip='once')

# Remove 20 uL from the first 8 tubes in a 0.75mL tube rack
# and add it to the first 8 wells in the 96 well plate
p200single.transfer(
    20, reagents.wells('A1', length=8), deep_plate.rows('1'), new_tip='always')

# Remove 50 uL from the first column (1) in the 96 well
# and add it to the second column.
# Remove 50 uL from the second column (2) and add it to the third (3).
# Remove 50 ul from the third column (3) and add it to the fourth (4).
p300multi.transfer(
    50, deep_plate.rows('1', length=3), deep_plate.rows('2', length=3))

# Remove 100 uL from the second column (2) of deep 96 well plate
# and add it to columns 1-3 of a second flat 96 well plate.
# Remove 100 uL from the third column of the original 96 well plate
# and add it to columns 4-6 of the second 96 well plate.
# Remove 100 uL from the fourth column of the original 96 well plate
# and add it to columns 7-9 of the second 96 well plate.
p300multi.transfer(
    100,
    deep_plate.rows('2', length=3),
    flat_plate.rows('1', length=9),
    new_tip='always')

# Remove 100 uL of medium from the trough/basin
# and add it to columns 10-12 of the second 96 well plate.
p300multi.transfer(100, medium, flat_plate.rows('10', length=3))
