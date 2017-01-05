from opentrons import containers, instruments


tiprack = containers.load('tiprack-200ul', 'B1')
tiprack2 = containers.load('tiprack-200ul', 'B1')
trough = containers.load('trough-12row', 'C1')
plate = containers.load('96-PCR-flat', 'D1')
trash = containers.load('point', 'B1')
tuberack = containers.load('tube-rack-2ml', 'D2')

p200_multi = instruments.Pipette(
    name="p200",
    trash_container=trash,
    tip_racks=[tiprack, tiprack2],
    max_volume=300,
    axis="a",
    channels=8
)

p200 = instruments.Pipette(
    name="p200S",
    trash_container=trash,
    tip_racks=[tiprack],
    max_volume=200,
    axis="b"
)

# dispense 6 standards from tube racks (A1, B1, C1, D1, A2, B2)
# to first two rows of 96 well plate (duplicates, A1/A2, B1/B2 etc.)
for i in range(6):
    p200.transfer(25, tuberack[i], plate.cols[i][:2])

# dispense 4 samples from tube rack (C2, D2, A3, B3)
# to row 3 of 96 well plate (duplicates, A3/B3, C3/D3, E3/F3, G3/H3)
for i in range(4):
    source = tuberack[i + 6]
    targets = plate.rows[2][i * 2:][:2]
    p200.transfer(50, source, targets)

# fill rows 4 to 11 with 25 uL of dilutent each
p200_multi.transfer(25, trough['A1'], plate.rows[3:11])

# dilute samples down all rows
p200_multi.transfer(25, plate.rows[2:10], plate.rows[3:11], mix=(3, 25))

# fill rows 1 to 11 with 200 uL of Bradford reagent
p200_multi.transfer(200, trough['A2'], plate.rows[:11], mix=(3, 100))
