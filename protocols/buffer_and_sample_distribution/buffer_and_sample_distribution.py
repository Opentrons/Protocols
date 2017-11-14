from opentrons import containers, instruments

trough = containers.load('trough-12row', 'D2', 'trough')

plate1 = containers.load('96-PCR-flat', 'C1', 'plate1')
plate2 = containers.load('96-PCR-flat', 'D1', 'plate2')

m200rack = containers.load('tiprack-200ul', 'E2', 'm200rack')
p10rack = containers.load('tiprack-10ul', 'A1', 'p10rack')

trash = containers.load('point', 'B2', 'trash')

m300 = instruments.Pipette(
    name="m300",
    trash_container=trash,
    tip_racks=[m200rack],
    min_volume=50,
    max_volume=300,
    axis="a",
    channels=8
)

p10 = instruments.Pipette(
    name="p10",
    trash_container=trash,
    tip_racks=[p10rack],
    min_volume=1,
    max_volume=10,
    axis="b",
    channels=1

)

# Transfer 20uL of buffer (first row of trough)
# to rows with sample (1-4) on plate1
m300.transfer(20, trough['A1'], plate1.rows('1', to='4'))

# Transfer 2uL of each sample row (1-4) on plate1 to 3 rows of each on plate2.
# Mix 5 times.

# TODO (Ian 2017-09-11) rewrite this to be more readable
#   (and, does it work right?):
for i in range(4):
    for j in range(3):
        p10.transfer(
            2,
            plate1.rows(i),
            plate2.rows(j),
            mix_after=(5, 2)
        )
    p10.drop_tip()
