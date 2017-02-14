from opentrons import containers, instruments


trough = containers.load('trough-12row', 'D2', 'trough')
plate = containers.load('96-PCR-flat', 'C1', 'plate')

p200Mrack = containers.load('tiprack-200ul', 'A1', 'p200M-rack')
trash = containers.load('point', 'B2', 'trash')

p200M = instruments.Pipette(
    name="p200M",
    trash_container=trash,
    tip_racks=[p200Mrack],
    min_volume=20,
    max_volume=200,
    axis="a",
    channels=8
)

p200M.distribute(
    180,
    trough['A1'],
    plate.rows.get('2', length=6)
)

p200M.transfer(
    20,
    plate.rows.get('1', length=6),
    plate.rows.get('2', length=6),
    mix_after=(3, 20)
)
