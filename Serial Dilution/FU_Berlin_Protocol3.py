from opentrons import containers, instruments


p200rack1 = containers.load('tiprack-200ul', 'A2')
p200rack2 = containers.load('tiprack-200ul', 'B2')
trash = containers.load('trash-box', 'E2')
trough = containers.load('trough-12row', 'C2')
tuberack = containers.load('tube-rack-15_50ml', 'D2')
plate1 = containers.load('384-plate', 'A1')
plate2 = containers.load('384-plate', 'B1')
plate3 = containers.load('384-plate', 'C1')
plate4 = containers.load('384-plate', 'D1')
plate5 = containers.load('384-plate', 'E1')


p200s = instruments.Pipette(
    axis="b",
    max_volume=200,
    tip_racks=[p200rack1],
    trash_container=trash
)

p200m = instruments.Pipette(
    axis="a",
    max_volume=200,
    tip_racks=[p200rack2],
    trash_container=trash
)

#Step 1
p200m.transfer(
    50,
    trough.wells('A1'),
    plate1.wells('A1', length=24),
    new_tips='once'
)

p200m.transfer(
    50,
    trough.wells('A1'),
    plate1.wells('B1', length=24),
    new_tips='never'
)

p200m.transfer(
    50,
    trough.wells('A1'),
    plate2.wells('A1', length=24),
    new_tips='once'
)

p200m.transfer(
    50,
    trough.wells('A1'),
    plate2.wells('B1', length=24),
    new_tips='never'
)

p200m.transfer(
    50,
    trough.wells('A1'),
    plate3.wells('A1', length=24),
    new_tips='once'
)

p200m.transfer(
    50,
    trough.wells('A1'),
    plate3.wells('B1', length=24),
    new_tips='never'
)

p200m.transfer(
    50,
    trough.wells('A1'),
    plate4.wells('A1', length=24),
    new_tips='once'
)

p200m.transfer(
    50,
    trough.wells('A1'),
    plate4.wells('B1', length=24),
    new_tips='never'
)

p200m.transfer(
    50,
    trough.wells('A1'),
    plate5.wells('A1', length=24),
    new_tips='once'
)

p200m.transfer(
    50,
    trough.wells('A1'),
    plate5.wells('B1', length=24),
    new_tips='never'
)

#Step 2
p200s.transfer(
    50,
    tuberack.wells('A1'),
    plate1.wells('A1', to='A22'),
    new_tips='once'
)

p200s.transfer(
    50,
    tuberack.wells('A1'),
    plate2.wells('A1', to='A22'),
    new_tips='once'
)

p200s.transfer(
    50,
    tuberack.wells('A1'),
    plate3.wells('A1', to='A22'),
    new_tips='once'
)

p200s.transfer(
    50,
    tuberack.wells('A1'),
    plate4.wells('A1', to='A22'),
    new_tips='once'
)

p200s.transfer(
    50,
    tuberack.wells('A1'),
    plate5.wells('A1', to='A22'),
    new_tips='once'
)

#Step 3
p200m.transfer(
    50,
    trough.wells('A1'),
    plate1.wells('A24'),
    new_tips='once'
)

p200m.transfer(
    50,
    trough.wells('A1'),
    plate2.wells('A24'),
    new_tips='once'
)

p200m.transfer(
    50,
    trough.wells('A1'),
    plate3.wells('A24'),
    new_tips='once'
)

p200m.transfer(
    50,
    trough.wells('A1'),
    plate4.wells('A24'),
    new_tips='once'
)

p200m.transfer(
    50,
    trough.wells('A1'),
    plate5.wells('A24'),
    new_tips='once'
)

#Step 4
p200m.transfer(
    50,
    trough.wells('A1'),
    plate1.wells('A1', to='A22'),
    new_tips='once'
)

p200m.transfer(
    50,
    trough.wells('A1'),
    plate2.wells('A1', to='A22'),
    new_tips='once'
)

p200m.transfer(
    50,
    trough.wells('A1'),
    plate3.wells('A1', to='A22'),
    new_tips='once'
)

p200m.transfer(
    50,
    trough.wells('A1'),
    plate4.wells('A1', to='A22'),
    new_tips='once'
)

p200m.transfer(
    50,
    trough.wells('A1'),
    plate5.wells('A1', to='A22'),
    new_tips='once'
)
