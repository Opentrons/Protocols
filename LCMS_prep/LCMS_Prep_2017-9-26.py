from opentrons import containers, instruments

# LCMS prep

# containers
containers.create(
    'tube-rack-4ml',                    # name of you container
    grid=(6, 8),                    # specify amount of (columns, rows)
    spacing=(13.25, 13.5),               # distances (mm) between (column, row)
    diameter=6.5,                     # diameter (mm) of each well on the plate
    depth=44)                       # depth (mm) of each well on the plate

containers.create(
    'resevoir-2',                    # name of you container
    grid=(1, 2),                    # specify amount of (columns, rows)
    spacing=(0, 54),               # distances (mm) between each (column, row)
    diameter=6.5,                     # diameter (mm) of each well on the plate
    depth=39.22)                       # depth (mm) of each well on the plate
"""
    Change num_samples before uploading to the OT app.
    If you input incorrect amount you will receive an error.
"""
num_samples = 100


# Plates/Tube racks
if (num_samples > 128 or num_samples < 1):
    raise Exception(print("Error - too many samples"))


tube_B2 = containers.load('tube-rack-4ml', 'B2', 'tube-rack-B2')
WP_500ul = containers.load('96-PCR-flat', 'C1', 'output 1')
resevoir = containers.load('resevoir-2', 'B1', 'resevoir')
tube_C2 = containers.load('tube-rack-4ml', 'C2', 'tube-rack-C2')

tube_D2 = containers.load('tube-rack-4ml', 'D2', 'tube-rack-D2')
WP_1ml = containers.load('96-PCR-flat', 'E1', 'output 2')


all_dest_wells = WP_500ul.wells(0, length=80) + WP_1ml.wells(0, length=48)

all_source_wells = tube_B2.wells(0, length=40) \
    + tube_C2.wells(0, length=40) + tube_D2.wells()

all_dest_rows = WP_500ul.rows(0, length=12) + WP_1ml.rows(0, length=12)

source_wells = all_source_wells[:num_samples]
dest_wells = all_dest_wells[:num_samples]
dest_rows = all_dest_rows

if num_samples <= 40:
    dest_rows = all_dest_rows[:6]
elif num_samples <= 80:
    dest_rows = all_dest_rows[:12]

# Tips
p300rack_B2 = containers.load('tiprack-200ul', 'B3')
p300rack_A2 = containers.load('tiprack-200ul', 'A2')
p300rack_A1 = containers.load('tiprack-200ul', 'A1')

trash = containers.load('point', 'D1', 'trash')

# insruments
p300multi = instruments.Pipette(
    name="P300 Multi-channel",
    trash_container=trash,
    tip_racks=[p300rack_B2],
    min_volume=96,
    max_volume=300,
    channels=8,
    axis="a"
)

p300single = instruments.Pipette(
    name="P300 Multi-channel",
    trash_container=trash,
    tip_racks=[p300rack_A1, p300rack_A2],
    min_volume=96,
    max_volume=300,
    axis="b"
)


# variables list
IS_soln = resevoir.wells('A1')


p300multi.transfer(200, IS_soln, dest_rows)


p300single.transfer(25, source_wells, dest_wells)
