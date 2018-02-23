"""
neut_dilution
@author Opentrons
@date Jan 29th, 2018
OT-2
"""

from opentrons import containers, instruments

# solutions in trough
trough = containers.load('trough-12row', '3')

# tube rack holding reagents
reagents = containers.load('tube-rack-.75ml', '6')

# 96 well plates
flat_plate = containers.load('96-PCR-flat', '2')
deep_plate = containers.load('96-deep-well', '5')

# tip rack for p10 and p50 pipette
tip200_rack = containers.load('tiprack-200ul', '1')
tip200_rack2 = containers.load('tiprack-200ul', '4')
tip200_rack3 = containers.load('tiprack-200ul', '7')

# trash to dispose of tips
trash = containers.load('fixed-trash', 12, 'trash')

# p200 (20 - 200 uL) (single)
p200single = instruments.P300_Single(
    mount='right',
    tip_racks=[tip200_rack])

# p300 (50 - 300 uL) (multi)
p300multi = instruments.P300_Multi(
    mount='left',
    tip_racks=[tip200_rack2, tip200_rack3])

# medium in trough
medium = trough['A1']

# Add 180 uL of medium from trough/basin to first column of deep 96 well plate.
p300multi.transfer(180, medium, deep_plate.columns('1'))

# Add 450 uL of medium from trough/basin to the next 3 columns (2-4)
# of the same deep 96 well plate.
p300multi.distribute(
    450, medium, deep_plate.columns('2', length=3), new_tip='once')

# Remove 20 uL from the first 8 tubes in a 0.75mL tube rack
# and add it to the first 8 wells in the 96 well plate
p200single.transfer(
    20, reagents.wells('A1', length=8), deep_plate.columns('1'), new_tip='always')

# Remove 50 uL from the first column (1) in the 96 well
# and add it to the second column.
# Remove 50 uL from the second column (2) and add it to the third (3).
# Remove 50 ul from the third column (3) and add it to the fourth (4).
p300multi.transfer(
    50, deep_plate.columns('1', length=3), deep_plate.columns('2', length=3))

# Remove 100 uL from the second column (2) of deep 96 well plate
# and add it to columns 1-3 of a second flat 96 well plate.
# Remove 100 uL from the third column of the original 96 well plate
# and add it to columns 4-6 of the second 96 well plate.
# Remove 100 uL from the fourth column of the original 96 well plate
# and add it to columns 7-9 of the second 96 well plate.
p300multi.transfer(
    100,
    deep_plate.columns('2', length=3),
    flat_plate.columns('1', length=9),
    new_tip='always')

# Remove 100 uL of medium from the trough/basin
# and add it to columns 10-12 of the second 96 well plate.
p300multi.transfer(100, medium, flat_plate.columns('10', length=3))
