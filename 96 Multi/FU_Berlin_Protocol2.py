from opentrons import containers, instruments


p200rack = containers.load('tiprack-200ul', 'D2')
trash = containers.load('trash-box', 'E2')
trough = containers.load('trough-12row', 'C2')
plate1 = containers.load('96-PCR-flat', 'A1')
plate2 = containers.load('96-PCR-flat', 'A2')
plate3 = containers.load('96-PCR-flat', 'B1')
plate4 = containers.load('96-PCR-flat', 'B2')
plate5 = containers.load('96-PCR-flat', 'C1')
plate6 = containers.load('96-PCR-flat', 'D1')
plate7 = containers.load('96-PCR-flat', 'E1')

p200 = instruments.Pipette(
    axis="b",
    max_volume=200,
    tip_racks=[p200rack],
    trash_container=trash
)

# dispense 100 uL from trough to plate
p200.transfer(
    100,
    trough.wells('A1'),
    plate1.wells('A1', length=12),
    new_tips='once'
)

p200.transfer(
    100,
    trough.wells('A1'),
    plate2.wells('A1', length=12),
    new_tips='once'
)

p200.transfer(
    100,
    trough.wells('A1'),
    plate3.wells('A1', length=12),
    new_tips='once'
)

p200.transfer(
    100,
    trough.wells('A1'),
    plate4.wells('A1', length=12),
    new_tips='once'
)

p200.transfer(
    100,
    trough.wells('A1'),
    plate5.wells('A1', length=12),
    new_tips='once'
)

p200.transfer(
    100,
    trough.wells('A1'),
    plate6.wells('A1', length=12),
    new_tips='once'
)

p200.transfer(
    100,
    trough.wells('A1'),
    plate7.wells('A1', length=12),
    new_tips='once'
)
