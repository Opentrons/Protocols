from opentrons import containers, instruments

vol = 100  # in ul, can change

# tip rack for p200 pipette
tip200_rack = containers.load('tiprack-200ul', 'A1')

# 96 well plate
plate = containers.load('96-PCR-flat', 'C1')

# trash to dispose of tips
trash = containers.load('trash-box', 'A2')

cells = containers.load('tube-rack-2ml', 'C2')

# p100 (10 - 100 uL) (single)
p200 = instruments.Pipette(
    axis='b',
    max_volume=200,
    min_volume=20,
    channels=1,
    trash_container=trash,
    tip_racks=[tip200_rack])

# dilution steps
for row in cells.rows():
    p200.transfer(vol, row[3:1:-1], row[2:0:-1])

# biofilm setup steps
for row in range(0, 6):
    p200.transfer(vol, cells.rows(row)[3], plate.cols(row)[0:12:3])
    p200.transfer(vol, cells.rows(row)[2], plate.cols(row)[1:12:3])
    p200.transfer(vol, cells.rows(row)[1], plate.cols(row)[2:12:3])
