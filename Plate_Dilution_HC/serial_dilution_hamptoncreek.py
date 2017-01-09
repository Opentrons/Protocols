from opentrons import containers, instruments


p1000rack = containers.load('tiprack-1000ul', 'A1')
p200rack = containers.load('tiprack-200ul', 'A2')
trough = containers.load('trough-12row', 'C1')
tube = containers.load('tube-rack-2ml', 'D1')
plate = containers.load('96-PCR-flat', 'D2')
trash = containers.load('point', 'B2')

p200_multi = instruments.Pipette(
    axis="a",
    max_volume=200,
    trash_container=trash,
    tip_racks=[p200rack],
    channels=8
)
p1000 = instruments.Pipette(
    axis="b",
    max_volume=1000,
    trash_container=trash,
    tip_racks=[p1000rack]
)

# distribute buffer to all wells, except columns A and E
target_wells = [w for c in 'BCDFGH' for w in plate.cols[c]]
p1000.transfer(300, trough['A1'], target_wells)

# distribute samples in duplicate to columns A and E, 1 tube to 2 wells
for i in range(12):
    p1000.transfer(300, tube[i], plate.rows[i][0::4])

# dilute down all rows
for row in plate.rows:
    p1000.transfer(300, row[0:3], row[1:4], mix=(3, 300))
    p1000.transfer(300, row[4:7], row[5:8], mix=(3, 300))

# dispense 200 uL to every even row
p200_multi.transfer(200, trough['A1'], plate.rows[1:12:2])
