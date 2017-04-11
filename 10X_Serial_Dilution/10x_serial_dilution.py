from opentrons import containers, instruments


# trough and 96-well plate
trough = containers.load('trough-12row', 'D2')
plate = containers.load('96-PCR-flat', 'C1')

# 8-channel 200uL pipette, with a tiprack and trash
m200rack = containers.load('tiprack-200ul', 'A1')
trash = containers.load('point', 'B2')
m200 = instruments.Pipette(
    axis='a',
    name='m200',
    trash_container=trash,
    tip_racks=[m200rack],
    max_volume=200,
    min_volume=20,
    channels=8
)

m200.distribute(180, trough['A1'], plate.rows('2', to='7'))

m200.transfer(
    20,
    plate.rows('1', to='6'),
    plate.rows('2', to='7'),
    mix_after=(3, 20)
)
