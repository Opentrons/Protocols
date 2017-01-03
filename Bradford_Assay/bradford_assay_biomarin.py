from opentrons.robot import Robot
from opentrons import containers, instruments
from itertools import chain

tiprack = containers.load(
    'tiprack-200ul',  
    'B1',             
    'tiprack'         
)

tiprack2 = containers.load(
    'tiprack-200ul',  
    'B1',             
    'tiprack2'        
)

trough = containers.load(
    'trough-12row',
    'C1',
    'trough'
)
plate = containers.load(
    '96-PCR-flat',
    'D1',
    'plate'
)
trash = containers.load(
    'point',
    'B1',
    'trash'
)
tuberack = containers.load(
    'tube-rack-2ml',
    'D2',
    'tuberack'
)
    
p200 = instruments.Pipette(
    name="p200",
    trash_container=trash,
    tip_racks=[tiprack, tiprack2],
    min_volume=50,
    max_volume=300,
    axis="a",
    channels=8
)
p200S = instruments.Pipette(
    name="p200S",
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
    p200S.pick_up_tip().aspirate(60, tuberack[i])
    wellone = plate.cols[i][0]
    welltwo = plate.cols[i][1]
    p200S.dispense(25, wellone).touch_tip().dispense(25, welltwo).touch_tip().drop_tip()
    
# dispense 4 samples from tube rack (C2, D2, A3, B3)
# to row 3 of 96 well plate (duplicates, A3/B3, C3/D3, E3/F3, G3/H3)
x = iter(plate.rows[2])
for i in range(6, 10):
    p200S.pick_up_tip().aspirate(110, tuberack[i])
    wellone = next(x)
    welltwo = next(x)
    p200S.dispense(50, wellone).touch_tip().dispense(50, welltwo).touch_tip().drop_tip()

# fill rows 4 to 11 with 25 uL of diluent each
p200.pick_up_tip(tiprack['A3']).aspirate(200, trough['A1'])
dispense_volume = 25
for i in range(3,11): 
    if p200.current_volume < dispense_volume:
        p200.aspirate(100, trough['A1'])
    p200.dispense(dispense_volume, plate.rows[i]).touch_tip()
p200.drop_tip()

# dilute samples down all rows
p200.pick_up_tip(tiprack['A4'])
for i in range(2, 10):
    p200.aspirate(25, plate.rows[i]).dispense(plate.rows[i + 1]).mix(3, 25, plate.rows[i + 1]).touch_tip()
p200.aspirate(25, plate.rows[10]).drop_tip()

# fill rows 1 to 11 with 200 uL of Bradford reagent
p200.pick_up_tip(tiprack['A5']).aspirate(200, trough['A2'])
dispense_volume = 200
for i in range(0,11): 
    if p200.current_volume < dispense_volume:
        p200.aspirate(200, trough['A1'])
    p200.dispense(dispense_volume, plate.rows[i]).mix(3, 100, plate.rows[i]).touch_tip()
p200.drop_tip()

