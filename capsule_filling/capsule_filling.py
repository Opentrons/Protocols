from opentrons import containers, instruments

# 15x50ml tube rack
liquid1 = containers.load('tube-rack-15_50ml', 'C3')
liquid2 = containers.load('tube-rack-15_50ml', 'D3')

# HACK: need to explicitly load each container like this
# instead of using a for loop, so that deck map can be parsed out
# for protocol library
plates = [
    containers.load('96-PCR-flat', 'A1'),
    containers.load('96-PCR-flat', 'B1'),
    containers.load('96-PCR-flat', 'C1'),
    containers.load('96-PCR-flat', 'D1'),
    containers.load('96-PCR-flat', 'A2'),
    containers.load('96-PCR-flat', 'B2'),
    containers.load('96-PCR-flat', 'C2'),
    containers.load('96-PCR-flat', 'D2')
]

# tip rack for p1000
tip1000_rack = containers.load('tiprack-1000ul', 'B3')

# trash to dispose of tips
trash = containers.load('trash-box', 'A3')

# p1000 (100 - 1000 uL) (single)
p1000single = instruments.Pipette(
    axis='b',
    name='p1000single',
    max_volume=1000,
    min_volume=100,
    channels=1,
    trash_container=trash,
    tip_racks=[tip1000_rack])

# Workflow description: We fill a vessel (in this case we were thinking
# the 12 well or the 15x50ml would be a good vessel to hold our fluid
# to be filled into the capsules.

# The purpose of the robot is to fill capsules all day so we would like the
# number of plates to both liquid and capsules to be optimized for performance.
wells50mltube = []
wells15mltube = []

for plate in plates[0:6:]:
    wells50mltube += [well for well in plate.wells()]
for plate in plates[6:8:]:
    wells15mltube += [well for well in plate.wells()]

tubes50ml = [well for well in liquid1.wells('A3', 'A4', 'B3', 'B4')] + \
    [well for well in liquid2.wells('A3', 'A4', 'B3', 'B4')]

tubes15ml = [
    well for well
    in liquid1.wells('A1', 'A2', 'B1', 'B2', 'C1', 'C2')] + \
    [well for well in liquid2.wells('A1', 'A2', 'B1', 'B2', 'C1', 'C2')]

# We will fill 96 well plates with "00" capsules (we are hoping this will work
# see capsule specs here: https://www.capsuline.com/empty-capsule-size-chart/).
# We will load the plates of empty capsules into the robot to be filled.
# Each capsule will need to be filled with exactly .7ml.

p1000single.transfer(700, tubes50ml, wells50mltube)
p1000single.transfer(700, tubes15ml, wells15mltube)

# Once filled we will remove the plates, close the capsules, remove them from
# the plates, refill with empty capsules and replaced into production
