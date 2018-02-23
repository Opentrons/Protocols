from opentrons import containers, instruments

vol = 100  # in ul, can change

# tip rack for p300 pipette
tip300_rack = containers.load('tiprack-200ul', '1')

# 96 well plate
plate = containers.load('96-PCR-flat', '2')

cells = containers.load('tube-rack-2ml', '3')

# p100 (10 - 100 uL) (single)
p300 = instruments.P300_Single(
    mount='right',
    tip_racks=[tip300_rack])

p300.pick_up_tip()

# dilution steps
for col in cells.cols():
    p300.transfer(vol, col[3:1:-1], col[2:0:-1])

# biofilm setup steps
for col in range(0, 6):
    p300.transfer(vol, cells.cols(col)[3], plate.rows(col)[0:12:3])
    p300.transfer(vol, cells.cols(col)[2], plate.rows(col)[1:12:3])
    p300.transfer(vol, cells.cols(col)[1], plate.rows(col)[2:12:3])
