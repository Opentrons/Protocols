from opentrons import containers, instruments


trough = containers.load('trough-12row', 'D2', 'trough')
plate = containers.load('96-PCR-flat', 'C1', 'plate')

m200rack = containers.load('tiprack-200ul', 'A1', 'm200-rack')
trash = containers.load('point', 'B2', 'trash')

m200 = instruments.Pipette(
    name="m200",
    trash_container=trash,
    tip_racks=[m200rack],
    min_volume=20,
    max_volume=200,
    axis="a",
    channels=8
)

m200.distribute(180, trough['A1'], plate.rows('2', to='7'))

m200.transfer(
    20,
    plate.rows('1', to='6'),
    plate.rows('2', to='7'),
    mix_after=(3, 20)
)
