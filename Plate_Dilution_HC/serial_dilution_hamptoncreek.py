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
target_wells = [w for col in plate.cols.get('B', to='H') for w in col]
p1000.distribute(300, trough.well('A1'), target_wells)

# distribute samples in duplicate to columns A and E, 1 tube to 2 wells
for i in range(12):
    p1000.distribute(300, tube.well(i), plate.rows[i].wells('A', 'E'))

# dilute down all rows
for row in plate.rows:
    p1000.transfer(
        300,
        row.wells('A', length=3),
        row.wells('B', length=3),
        mix_after=(3, 300))
    p1000.transfer(
        300,
        row.wells('E', length=3),
        row.wells('F', length=3),
        mix_after=(3, 300))

# dispense 200 uL to every even row
p200_multi.distribute(
    200, trough.well('A1'), plate.rows.get('2', to='12', step=2))
