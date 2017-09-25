from opentrons import containers, instruments


cooldeck = containers.load('alum-block-pcr-strips', 'C3')
plate = containers.load('rigaku-compact-crystallization-plate', 'C1')
plate2 = containers.load('rigaku-compact-crystallization-plate', 'C2')
matrix_index = containers.load('hampton-1ml-deep-block', 'B1')
matrix_peg = containers.load('hampton-1ml-deep-block', 'B2')

p20rack = containers.load('tiprack-10ul', 'E1')
p20rack2 = containers.load('tiprack-10ul', 'E2')
p20rack3 = containers.load('tiprack-10ul', 'E3')

p1000rack = containers.load('tiprack-1000ul', 'A1')
p1000rack2 = containers.load('tiprack-1000ul', 'A2')

trash = containers.load('trash-box', 'A3')

p1000 = instruments.Pipette(
    axis="b",
    max_volume=1000,
    min_volume=100,
    tip_racks=[p1000rack, p1000rack2],
    trash_container=trash,
    channels=1,
    name="p1000"
)

m10 = instruments.Pipette(
    axis="a",
    max_volume=10,
    min_volume=0.5,
    tip_racks=[p20rack, p20rack2, p20rack3],
    trash_container=trash,
    channels=8,
    name="m10"
)

p1000.transfer(
    100, matrix_index.wells(length=96), plate.wells(96, length=96),
    new_tip='always')

m10.distribute(1, cooldeck.wells('A1'), plate.rows('1', to='12'))

m10.transfer(1, plate.rows('1', to='12'), plate.rows('13', to='24'))

p1000.transfer(
    100, matrix_peg.wells(0, length=96), plate2.wells(96, length=96),
    new_tip='always')

m10.distribute(1, cooldeck.wells('A1'), plate.rows('1', to='12'))

m10.transfer(1, plate2.rows('1', to='12'), plate2.rows('13', to='24'))
