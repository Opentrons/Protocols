from opentrons import containers, instruments

# volume to dispense
vol = 10  # change here

# 384 well plate
destination_plate = containers.load('384-plate', 'C1')

# tip rack for p50 pipette
tip200_rack = containers.load('tiprack-200ul', 'A2')

# trough with matrigel + cell
matrigelcell_trough = containers.load('trough-12row', 'C2')

# trash to dispose of tips
trash = containers.load('point', 'D2', 'trash')

# p10 (1 - 10 uL) (multi)
p50multi = instruments.Pipette(
    axis='a',
    name='p50multi',
    max_volume=50,
    min_volume=5,
    channels=8,
    trash_container=trash,
    tip_racks=[tip200_rack])

# location of matrigel + cell in trough
matcell = matrigelcell_trough['A1']  # can change here

# rows of 384 plate
platerows = []

for row in destination_plate.rows():
    platerows.append(row.wells('A', length=8, step=2))
    platerows.append(row.wells('B', length=8, step=2))

# distribute 10ul/well in 384 plate
p50multi.distribute(10, matcell, platerows, new_tip='once')
