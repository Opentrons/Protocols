from opentrons import labware, instruments

plate1 = labware.load('96-deep-well', '11', 'plate1')
plate2 = labware.load('384-plate', '9', 'plate2')
p10rack = labware.load('tiprack-10ul', '10', 'p10rack')


p10 = instruments.P10_Single(
    tip_racks=[p10rack],
    mount="right"
)

# Transfer 8 master mix solutions from row 1 of 96 well plate
# to all rows on 384 plate (48 wells of each master mix solution on 384).
dest_wells = []
for col in plate2.cols():
    dest_wells.append(col.wells('A', length=8, step=2))
    dest_wells.append(col.wells('B', length=8, step=2))

transfer_vol = 5
source_wells = plate1.cols('1')

p10.distribute(
    transfer_vol,
    source_wells,
    dest_wells,
    blow_out=True
)
