from opentrons import instruments, containers

# trough and 384-well plate
trough = containers.load('trough-12row', 'E1', 'trough')
plate = containers.load('384-plate', 'C1', 'plate')

# 8-channel 10uL pipette, with tip rack and trash
tiprack = containers.load('tiprack-200ul', 'A1', 'p200rack')
trash = containers.load('point', 'B2', 'trash')
m200 = instruments.Pipette(
    axis='a',
    trash_container=trash,
    tip_racks=[tiprack],
    max_volume=10,
    min_volume=0.5,
    channels=8,
)


def run_custom_protocol(well_volume: float=1.0):
    alternating_wells = []
    for row in plate.rows():
        alternating_wells.append(row.wells('A', length=8, step=2))
        alternating_wells.append(row.wells('B', length=8, step=2))

    m200.distribute(well_volume, trough.wells('A1'), alternating_wells)
