from opentrons import labware, instruments

# labware setup
plate = labware.load('96-flat', '2')
trough = labware.load('trough-12row', '1')
tiprack = labware.load('tiprack-200ul', '4')

# Reagents in trough
NaOAc_buffer = trough.wells('A1')
enzyme_std = trough.wells('A2')
substrate_1 = trough.wells('A3')
substrate_4 = trough.wells('A4')

# Pipette setup
m300 = instruments.P300_Multi(
    mount='left',
    tip_racks=[tiprack])

# Transfer 200 uL sodium acetate buffer to cols 1-3
m300.transfer(200, NaOAc_buffer, plate.cols('1', to='3'))

# Transfer 50 uL sodium acetate buffer to cols 1, 4, 7, 10
m300.transfer(50, NaOAc_buffer, plate.cols('1', to='10', step=3))

# Transfer 50 uL enzyme standard to cols 2, 5, 6, 11
m300.transfer(50, enzyme_std, plate.cols('2', to='11', step=3))

# Transfer 50 uL enzyme substrate type 1 to cols 3, 6, 9, 12
m300.transfer(50, substrate_1, plate.cols('3', to='12', step=3))

# Transfer 50 uL enzyme substrate type 2 to cols 3, 6, 9, 12
m300.transfer(50, substrate_4, plate.cols('3', to='12', step=3))
