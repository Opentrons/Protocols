from opentrons import containers, instruments, robot
"""
PART 2: After spinning to pellet DNA
"""

# Labware setup
plate2 = containers.load('96-deep-well', 'D1')
liquid_trash = containers.load('trough-12row', 'A1').wells('A1')
trough = containers.load('trough-12row', 'B1')
tiprack1 = containers.load('tiprack-200ul', 'C2')
tiprack2 = containers.load('tiprack-200ul', 'B2')
tiprack3 = containers.load('tiprack-200ul', 'D2')

extraction_buffer = trough.wells('A1')
isopropanol = trough.wells('A2')
ethanol = trough.wells('A3')
te_buffer = trough.wells('A4')

# Instrument setup
m300 = instruments.Pipette(
    axis='A',
    max_volume=300,
    tip_racks=[tiprack1, tiprack2, tiprack3],
    channels=8)

# Remove supernatent
m300.transfer(199, plate2.rows(), liquid_trash, new_tip='always')

# Transfer ethanol
m300.transfer(200, ethanol, plate2.rows())

# Remove supernatent
m300.transfer(199, plate2.rows(), liquid_trash, new_tip='always')

robot.pause()

# Add TE buffer
m300.transfer(50, te_buffer, plate2.rows())
