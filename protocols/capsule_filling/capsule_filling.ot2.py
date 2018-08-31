from opentrons import labware, instruments

# 15x50ml tube rack
liquid1 = labware.load('tube-rack-15_50ml', '7')
liquid2 = labware.load('tube-rack-15_50ml', '10')

# HACK: need to explicitly load each container like this
# instead of using a for loop, so that deck map can be parsed out
# for protocol library
plates = [
    labware.load('96-PCR-flat', '1'),
    labware.load('96-PCR-flat', '2'),
    labware.load('96-PCR-flat', '3'),
    labware.load('96-PCR-flat', '6'),
    labware.load('96-PCR-flat', '5'),
    labware.load('96-PCR-flat', '8'),
    labware.load('96-PCR-flat', '11'),
    labware.load('96-PCR-flat', '9')
]

# tip rack for p1000
tip1000_rack = labware.load('tiprack-1000ul', '4')

# p1000 (100 - 1000 uL) (single)
p1000single = instruments.P1000_Single(
    mount='right',
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
def run_custom_protocol(fill_volume: float=700):
    p1000single.transfer(fill_volume, tubes50ml, wells50mltube)
    p1000single.transfer(fill_volume, tubes15ml, wells15mltube)

# Once filled we will remove the plates, close the capsules, remove them from
# the plates, refill with empty capsules and replaced into production
