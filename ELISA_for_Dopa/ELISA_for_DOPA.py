from opentrons import robot, containers, instruments
from itertools import chain

standards = containers.load(
    'tube-rack-2ml',
    'C1',
    'standards'
)
# standards['A1'] = STD A 1000 pg/ml
# standards['B1'] = STD B 500 pg/ml
# standards['C1'] = STD C 250 pg/ml
# standards['D1'] = STD D 125 pg/ml
# standards['A2'] = STD E 62.5 pg/ml
# standards['B2'] = STD F 31.5 pg/ml
# standards['C1'] = STD G 0 pg/ml
# standards['D1'] = blank

plate = containers.load(
    '96-PCR-flat',
    'C2',
    'ELISA_plate'
)
trash = containers.load(
    'point',
    'A2',
    'trash'
)
p200rack = containers.load(
    'tiprack-200ul',
    'A1',
    'p200rack'
)
p200rack2 = containers.load(
    'tiprack-200ul',
    'A2',
    'p200rack2'
)
p200rack3 = containers.load(
    'tiprack-200ul',
    'A3',
    'p200rack3'
)
samples1 = containers.load(
    'tube-rack-2ml',
    'E1',
    'samples1'
)

# samples1['A1'] = patient sample 1
# samples1['B1'] = patient sample 2
# samples1['C1'] = patient sample 3
# ...
# samples1['D6'] = patient sample 24

samples2 = containers.load(
    'tube-rack-2ml',
    'E2',
    'samples2'
)

# samples2['A1'] = patient sample 25
# samples2['B1'] = patient sample 26
# samples2['C1'] = patient sample 27
# ...
# samples2['D4'] = patient sample 40

solutions = containers.load(
    'tube-rack-15_50ml',
    'E3',
    'solutions',
)

# solutions['C3'] = HRP Conjugate Solution
# solutions['A4'] = Chromogen A
# solutions['B4'] = Chromogen B
# solutions['C4'] = Stop Solution

p200 = instruments.Pipette(   
        axis="b",
        max_volume=200,
        min_volume=20,
        tip_racks=[p200rack, p200rack2, p200rack3],
        trash_container=trash,
        channels=1,
        name="p200"
)

# Dispense standards in duplicate to last two rows of plate
x = chain(plate.rows[10], plate.rows[11])
for i in range(8):
    p200.pick_up_tip().aspirate(100, standards[i])
    wellone = next(x)
    welltwo = next(x)
    p200.dispense(50, wellone).touch_tip().dispense(50, welltwo).touch_tip().drop_tip()
    
# Dispense patient samples in duplicate to plate
y = chain(samples1, samples2)
for i in range(0, 80, 2):
    tubeone = next(y)
    p200.pick_up_tip().aspirate(100, tubeone).dispense(50, plate[i]).dispense(50, plate[i+1]).drop_tip()

# Dispense 100 uL of HRP Conjugate Solution to all wells
dispense_volume = 100
p200.pick_up_tip()
for i in range(96):
    if p200.current_volume < dispense_volume:
        p200.aspirate(200, solutions['C3'])
    p200.dispense(dispense_volume, plate[i].top())
p200.drop_tip()
    
# pause protocol
# incubate 60 min at 37 C
# automate washing station
# return plate to robot
# resume protocol

# Dispense 50 ul of Chromogen Solution A to all wells
dispense_volume = 50
p200.pick_up_tip()
for i in range(96):
    if p200.current_volume < dispense_volume:
        p200.aspirate(200, solutions['A4'])
    p200.dispense(dispense_volume, plate[i].top())
p200.drop_tip()

# Dispense 50 ul of Chromogen Solution B to all wells
dispense_volume = 50
p200.pick_up_tip()
for i in range(96):
    if p200.current_volume < dispense_volume:
        p200.aspirate(200, solutions['B4'])
    p200.dispense(dispense_volume, plate[i].top())
p200.drop_tip()
    
# pause protocol
# incubate 15 min at 37 C
# return plate to robot
# resume protocol

# Dispense 50 uL of Stop Solution to all wells
dispense_volume = 50
p200.pick_up_tip()
for i in range(96):
    if p200.current_volume < dispense_volume:
        p200.aspirate(200, solutions['C4'])
    p200.dispense(dispense_volume, plate[i].top())
p200.drop_tip()