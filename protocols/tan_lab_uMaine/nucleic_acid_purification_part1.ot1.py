from opentrons import containers, instruments, robot
"""
PART 1: Before spinning to pellet DNA
"""

# Labware setup
plate1 = containers.load('96-deep-well', 'C1')
plate2 = containers.load('96-deep-well', 'D1')
trough = containers.load('trough-12row', 'B1')
tiprack1 = containers.load('tiprack-200ul', 'C2')
tiprack2 = containers.load('tiprack-200ul', 'B2')

extraction_buffer = trough.wells('A1')
isopropanol = trough.wells('A2')

# Instrument setup
m300 = instruments.Pipette(
    axis='A',
    max_volume=300,
    tip_racks=[tiprack1, tiprack2],
    channels=8)

# Transfer DNA extraction buffer
m300.transfer(250, extraction_buffer, plate1.rows())

robot.pause()

# Define height from which the pipette is aspirating from plate1
plate_1_loc = [well.bottom(5) for well in plate1.rows()]

# Transfer supernatent from Plate 1 to Plate 2
m300.transfer(100, plate_1_loc, plate2.rows(), new_tip='always')

# Transfer isopropanol to Plate 2
m300.transfer(100, isopropanol, plate2.rows())
