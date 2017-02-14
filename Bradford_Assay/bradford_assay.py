from opentrons import containers, instruments
import itertools


tiprack = containers.load('tiprack-200ul', 'B1')
tiprack2 = containers.load('tiprack-200ul', 'B2')
trash = containers.load('point', 'C2')

trough = containers.load('trough-12row', 'C1')
plate = containers.load('96-PCR-flat', 'D1')
tuberack = containers.load('tube-rack-2ml', 'D2')

p300_multi = instruments.Pipette(
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
    p200.distribute(25, tuberack[i], plate.cols[i].wells('1', '2'))

# dispense 4 samples from tube rack (C2, D2, A3, B3)
# to row 3 of 96 well plate (duplicates, A3/B3, C3/D3, E3/F3, G3/H3)
target_wells = itertools.chain(plate.rows['3'])
for source in tuberack.wells('C2', length=4):
    target = [next(target_wells), next(target_wells)]
    p200.distribute(50, source, target)

# fill rows 4 to 11 with 25 uL of dilutent each
p300_multi.distribute(
    25,
    trough['A1'],
    plate.rows.get('4', length=8))

# dilute samples down all rows
p300_multi.transfer(
    25,
    plate.rows.get('3', length=8),
    plate.rows.get('4', length=8),
    mix_after=(3, 25))

# fill rows 1 to 11 with 200 uL of Bradford reagent
for target in plate.rows.get('1', length=11):
    p300_multi.transfer(200, trough['A2'], target, mix_after=(3, 100))
