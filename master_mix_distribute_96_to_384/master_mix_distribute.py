from opentrons import containers, instruments

plate1 = containers.load('96-deep-well', 'C1', 'plate1')
plate2 = containers.load('384-plate', 'E1', 'plate2')
m10rack = containers.load('tiprack-10ul', 'A1', 'm10rack')
trash = containers.load('point', 'B2', 'trash')

m10 = instruments.Pipette(
    name="m10",
    trash_container=trash,
    tip_racks=[m10rack],
    min_volume=0.5,
    max_volume=10,
    axis="a",
    channels=8
)

# Transfer 8 master mix solutions from row 1 of 96 well plate
# to all rows on 384 plate (48 wells of each master mix solution on 384).
dest_wells = []
for row in plate2.rows():
    dest_wells.append(row.wells('A', length=8, step=2))
    dest_wells.append(row.wells('B', length=8, step=2))

transfer_vol = 5
source_wells = plate1.rows('1')

m10.distribute(
    transfer_vol,
    source_wells,
    dest_wells,
    blow_out=True
)
