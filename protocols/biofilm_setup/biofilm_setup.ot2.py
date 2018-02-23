from opentrons import containers, instruments

vol = 100  # in ul, can change

# tip rack for p200 pipette
tip200_rack = containers.load('tiprack-200ul', '1')

# 96 well plate
plate = containers.load('96-PCR-flat', '2')

cells = containers.load('tube-rack-2ml', '3')

# p100 (10 - 100 uL) (single)
p200 = instruments.Pipette(
    mount='right',
    max_volume=200,
    min_volume=20,
    channels=1,
    tip_racks=[tip200_rack])

# dilution steps
for col in cells.cols():
    p200.transfer(vol, col[3:1:-1], col[2:0:-1])

# biofilm setup steps
for col in range(0, 6):
    p200.transfer(vol, cells.cols(col)[3], plate.rows(col)[0:12:3])
    p200.transfer(vol, cells.cols(col)[2], plate.rows(col)[1:12:3])
    p200.transfer(vol, cells.cols(col)[1], plate.rows(col)[2:12:3])
