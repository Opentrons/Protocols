from opentrons import labware, instruments

# volume to dispense
vol = 10  # change here

# 384 well plate
destination_plate = labware.load('384-plate', '2')

# tip rack for p50 pipette
tip200_rack = labware.load('tiprack-200ul', '1')

# trough with matrigel + cell
matrigelcell_trough = labware.load('trough-12row', '3')

# p10 (1 - 10 uL) (multi)
p50multi = instruments.Pipette(
    mount='left',
    name='p50multi',
    max_volume=50,
    min_volume=5,
    channels=8,
    tip_racks=[tip200_rack])

# location of matrigel + cell in trough
matcell = matrigelcell_trough['A1']  # can change here

# rows of 384 plate
platecols = []

for col in destination_plate.cols():
    platecols.append(col.wells('A', length=8, step=2))
    platecols.append(col.wells('B', length=8, step=2))

# distribute 10ul/well in 384 plate
p50multi.distribute(10, matcell, platecols, new_tip='once')
