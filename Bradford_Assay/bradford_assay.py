from opentrons.robot import Robot
from opentrons import containers, instruments
from itertools import chain

tiprack = containers.load(
    'tiprack-200ul',  
    'A1',             
    'tiprack'         
)
tiprack50 = containers.load(
    'tiprack-200ul',  
    'A2',             
    'tiprack50'         
)
trough = containers.load(
    'trough-12row',
    'B2',
    'trough'
)
plate = containers.load(
    '96-PCR-flat',
    'C1',
    'plate'
)
trash = containers.load(
    'point',
    'C2',
    'trash'
)
tuberack = containers.load(
    'tube-rack-2ml',
    'D2',
    'tuberack'
)
    
p50 = instruments.Pipette(
    name="p200", # change to p50 after testing
    trash_container=trash,
    tip_racks=[tiprack50],
    min_volume=25,
    max_volume=200,
    axis="a",
    channels=8
)
p200 = instruments.Pipette(
    name="p200S", # change to p200 after testing
    trash_container=trash,
    tip_racks=[tiprack],
    min_volume=20,
    max_volume=200,
    axis="b",
    channels=1
)

# dispense 6 standards from tube racks (A1, B1, C1, D1, A2, B2) 
# to first two rows of 96 well plate (duplicates, A1/A2, B1/B2 etc.)
for i in range(6):
    p200.pick_up_tip().aspirate(60, tuberack[i])
    wellone = plate.cols[i][0]
    welltwo = plate.cols[i][1]
    p200.dispense(25, wellone).touch_tip().dispense(25, welltwo).touch_tip().drop_tip()
    
# dispense 4 samples from tube rack (C2, D2, A3, B3)
# to row 3 of 96 well plate (duplicates, A3/B3, C3/D3, E3/F3, G3/H3)
x = iter(plate.rows[2])
for i in range(6, 10):
    p200.pick_up_tip().aspirate(110, tuberack[i])
    wellone = next(x)
    welltwo = next(x)
    p200.dispense(50, wellone).touch_tip().dispense(50, welltwo).touch_tip().drop_tip()

# fill rows 4 to 11 with 25 uL of diluent each
p50.pick_up_tip().aspirate(50, trough['A1'])
dispense_volume = 25
for i in range(3,11):
    if p50.current_volume < dispense_volume:
        p50.aspirate(50, trough['A1'])
    p50.dispense(dispense_volume, plate.rows[i]).touch_tip()
p50.drop_tip()

# dilute samples down all rows
p50.pick_up_tip()
for i in range(2, 10):
    p50.aspirate(25, plate.rows[i]).dispense(plate.rows[i + 1]).mix(3, 25, plate.rows[i + 1]).touch_tip()
p50.aspirate(25, plate.rows[10]).drop_tip()

# fill rows 1 to 11 with 200 uL of Bradford reagent
p50.pick_up_tip().aspirate(50, trough['A2'])
for i in range(0,11): 
    p50.aspirate(50, trough['A2']).dispense(plate.rows[i].top())
    p50.aspirate(50, trough['A2']).dispense(plate.rows[i].top())
    p50.aspirate(50, trough['A2']).dispense(plate.rows[i].top())
    p50.aspirate(50, trough['A2']).dispense(plate.rows[i].top())
p50.drop_tip()

