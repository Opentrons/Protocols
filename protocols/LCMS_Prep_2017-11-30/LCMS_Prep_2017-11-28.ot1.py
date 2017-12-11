from opentrons import containers, instruments

# LCMS prep

# containers
containers.create(
    'tube-rack-4ml',                    # name of you container
    grid=(6, 8),                    # specify amount of (columns, rows)
    spacing=(13.25, 13.5),          # distances (mm) between each (column, row)
    diameter=6.5,                     # diameter (mm) of each well on the plate
    depth=44)                       # depth (mm) of each well on the plate

containers.create(
    'resevoir-2',                    # name of you container
    grid=(1, 2),                    # specify amount of (columns, rows)
    spacing=(0, 54),               # distances (mm) between each (column, row)
    diameter=6.5,                     # diameter (mm) of each well on the plate
    depth=39.22)                       # depth (mm) of each well on the plate

containers.create(
    'vial-rack',                    # name of you container
    grid=(6, 9),                    # specify amount of (columns, rows)
    spacing=(12.25, 12.5),         # distances (mm) between each (column, row)
    diameter=6.5,                     # diameter (mm) of each well on the plate
    depth=39.22)                       # depth (mm) of each well on the plate
"""
    Change num_samples before uploading to the OT app
"""


def run_custom_protocol(number_of_samples: int=96):
    num_samples = number_of_samples

    # Plates/Tube racks
    if (num_samples > 96 or num_samples < 1):
        raise Exception(print("Error - too many samples"))

    tube_A1 = containers.load('tube-rack-4ml', 'A1', 'vial-rack-A1')
    vialrack1 = containers.load('vial-rack', 'B1', 'output 1')

    resevoir = containers.load('resevoir-2', 'C2', 'resevoir')

    vialrack2 = containers.load('vial-rack', 'D1', 'vial-rack-D1')
    tube_E1 = containers.load('tube-rack-4ml', 'E1', 'tube-rack-E1')

    all_dest_wells = vialrack1.wells(0, length=48) \
        + vialrack2.wells(0, length=48)
    all_source_wells = tube_A1.wells() + tube_E1.wells()
    all_dest_rows = vialrack1.rows(0, length=8) + vialrack2.rows(0, length=8)

    source_wells = all_source_wells[:num_samples]
    dest_wells = all_dest_wells[:num_samples]
    dest_rows = all_dest_rows

    if num_samples <= 49:
        dest_rows = all_dest_rows[:6]
    elif num_samples <= 97:
        dest_rows = all_dest_rows[:12]

    # Tips
    p300rack_B2 = containers.load('tiprack-200ul', 'B2')
    p300rack_D2 = containers.load('tiprack-200ul', 'D2')

    trash = containers.load('point', 'C1', 'trash')
    # instruments
    p300single = instruments.Pipette(
        name="P300 Single-channel",
        trash_container=trash,
        tip_racks=[p300rack_B2, p300rack_D2],
        min_volume=96,
        max_volume=300,
        axis="b"
    )

    # variables list
    IS_soln = resevoir.wells('A1')

    p300single.transfer(125, IS_soln, dest_rows, new_tip='once')

    p300single.transfer(125, source_wells, dest_wells)
