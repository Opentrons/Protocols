from opentrons import robot, containers, instruments


p1000rack = containers.load(
    'tiprack-1000ul',
    'A1',
    'p1000rack'
)

vialrack = containers.load(
    'wheaton_vial_rack',
    'C1',
    'vialrack'
)

plate = containers.load(
    '96-deep-well',
    'B1',
    'plate'
)

trash = containers.load(
    'point',
    'B2',
    'trash'
)

p1000 = instruments.Pipette(
    name="p1000",
    trash_container=trash,
    tip_racks=[p1000rack],
    min_volume=100,
    max_volume=1000,
    axis="b",
    channels=1
)

# Creates list of columns on 96 well plate
columns_list = []
for column in plate.cols:
    columns_list.append(iter(column))
    

# Distribute 48 samples to 96 well plate
for i in range(48):
    p1000.pick_up_tip()
    p1000.aspirate(600, vialrack[i])
    p1000.dispense(300, next(columns_list[i % 8]))
    p1000.dispense(300, next(columns_list[i % 8]))
    p1000.drop_tip()
