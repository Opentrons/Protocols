from opentrons import containers, instruments


p10rack = containers.load('tiprack-10ul', 'E1', 'p10-rack')
p200rack = containers.load('tiprack-200ul', 'A1', 'p200-rack')
tuberack = containers.load('tube-rack-2ml', 'C1', 'tube rack')
output = containers.load('96-PCR-flat', 'B2', 'output')
trash = containers.load('point', 'D2', 'trash')

p10 = instruments.Pipette(
    name="p10",
    trash_container=trash,
    tip_racks=[p10rack],
    max_volume=10,
    axis="a"
)

p200 = instruments.Pipette(
    name="p200",
    trash_container=trash,
    tip_racks=[p200rack],
    max_volume=200,
    axis="b"
)

total_volume = 25
DNA_volume = 3
MM_volume = total_volume - DNA_volume

DNA_local = tuberack.wells('A1')
MM_local = tuberack.wells('D2')

sources = {
    tuberack.well('B1'): 3 * total_volume,
    tuberack.well('C1'): 2.5,
    tuberack.well('D1'): 2.5,
    tuberack.well('A2'): 2,
    tuberack.well('B2'): 2
}
# final well is whatever is left-over from total_volume
sources[tuberack.well('C2')] = total_volume - sum(sources.values())

num_samples = len(sources.keys())

# create master mix
p200.transfer(
    list(sources.values()),
    list(sources.keys()),
    [MM_local] * num_samples,
    new_tip='always')

# distribute master mix
# Master Mix Location
p200.distribute(MM_volume, MM_local, output.wells(length=num_samples))
p10.distribute(DNA_volume, DNA_local, output.wells(length=num_samples))

from opentrons import robot
for c in robot.commands():
    print(c)
