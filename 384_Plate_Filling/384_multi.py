from opentrons import robot, instruments, containers


trough = containers.load('trough-12row', 'E1', 'trough')
plate = containers.load('384-plate', 'C1', 'plate')

tiprack = containers.load('tiprack-200ul', 'A1', 'p200rack')
trash = containers.load('point', 'B2', 'trash')
p200 = instruments.Pipette(
    axis='a',
    channels=8,
    trash_container=trash,
    tip_racks=[tiprack],
    min_volume=0.5,
    max_volume=10
)

alternating_wells = []
for row in plate.rows():
    alternating_wells.append(row.wells('A', length=8, step=2))
    alternating_wells.append(row.wells('B', length=8, step=2))

p200.distribute(
    1,
    trough.wells('A1'),
    alternating_wells
)
