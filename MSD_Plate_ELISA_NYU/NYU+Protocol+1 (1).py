
from opentrons import robot, containers, instruments

trough = containers.load(
    'trough-12row',
    'C1',
    'trough'
)
tuberack = containers.load(
    'tube-rack-15_50ml',
    'D1',
    'tuberack'
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
trash = containers.load(
    'point',
    'B2',
    'trash'
)
plate = containers.load(
    '96-PCR-flat',
    'D2',
    'plate')

p200 = instruments.Pipette(
    name="p200",
    trash_container=trash,
    tip_racks=[p200rack, p200rack2, p200rack3],
    min_volume=50,
    max_volume=200,
    axis="a",
    channels=8
)
p200S = instruments.Pipette(
    name="p200S",
    trash_container=trash,
    tip_racks=[p200rack, p200rack2, p200rack3],
    min_volume=20,
    max_volume=200,
    axis="b",
    channels=1
)


PBS = trough['A1']
gp120 = trough['A2']
BSA = trough['A3']
PBST = trough['A4']
macaqueSRCR = trough['A5']
antibody1527 = tuberack['A1']
antirabbit = tuberack['A2']
readbuffer = trough['A6']

# incubate RT for 20 min
p200.delay(1500)

# coat plate with 25 uL PBS
dispense_volume = 25
p200.pick_up_tip()
for i in range(12):
    if p200.current_volume < dispense_volume:
        p200.aspirate(200, PBS)
    p200.dispense(dispense_volume, plate.rows[i])
p200.drop_tip()

# coat plates with 30 uL of coating solution
dispense_volume = 30
p200.pick_up_tip()
for i in range(12):
    if p200.current_volume < dispense_volume:
        p200.aspirate(180, gp120)
    p200.dispense(dispense_volume, plate.rows[i])

# seal plates and shake for 20 min
p200.delay(1200)

# empty out coating solution
for i in range(12):
    p200.aspirate(30, plate.rows[i]).dispense(trash['A1'])
p200.drop_tip()

# add 200 uL per well of BSA
p200.pick_up_tip()
for i in range(12):
    p200.aspirate(200, BSA).dispense(plate.rows[i])
p200.drop_tip()

# seal and incubate for2 hours
p200.delay(7200)

# wash plate 3X with PBST
p200.pick_up_tip()
while (i < 3):
    for i in range(12):
        p200.aspirate(175, PBST).dispense(plate.rows[i])
        p200.delay(15)
        p200.aspirate(200, plate.rows[i]) # add well edge
        p200.dispense(trash['A1']) 
    i = i+1
p200.drop_tip()

# add 25 uL of purified macaqueSRCR
dispense_volume = 25
p200S.pick_up_tip()
for i in range(96):
    if p200S.current_volume < dispense_volume:
        p200S.aspirate(200, macaqueSRCR)
    p200S.dispense(dispense_volume, plate[i])
p200S.drop_tip()

# seal and incubate for 1.5 hours
p200.delay(5400)

# wash plate 3X with PBST
p200.pick_up_tip()
while (i < 3):
    for i in range(12):
        p200.aspirate(175, PBST).dispense(plate.rows[i])
        p200.delay(15)
        p200.aspirate(200, plate.rows[i]) # add well edge
        p200.dispense(trash['A1']) 
    i = i+1
p200.drop_tip()

# add 25 uL 1527 antibody
dispense_volume = 25
p200S.pick_up_tip()
for i in range(96):
    if p200S.current_volume < dispense_volume:
        p200S.aspirate(200, antibody1527)
    p200S.dispense(dispense_volume, plate[i])
p200S.drop_tip()

# seal and incubate 1 hour
p200.delay(3600)

# wash plate 3X with PBST
p200.pick_up_tip()
while (i < 3):
    for i in range(12):
        p200.aspirate(175, PBST).dispense(plate.rows[i])
        p200.delay(15)
        p200.aspirate(200, plate.rows[i]) # add well edge
        p200.dispense(trash['A1']) 
    i = i+1
p200.drop_tip()

# add 25 uL MSD SulfoTag
p200S.pick_up_tip()
for i in range(96):
    p200S.aspirate(25, antirabbit).dispense(plate[i])
p200S.drop_tip()

# wash plate 3X with PBST
p200.pick_up_tip()
while (i < 3):
    for i in range(12):
        p200.aspirate(175, PBST).dispense(plate.rows[i])
        p200.delay(15)
        p200.aspirate(200, plate.rows[i]) # add well edge
        p200.dispense(trash['A1']) 
    i = i+1
p200.drop_tip()

# add 150 uL read buffer
p200.pick_up_tip()
for i in range(12):
    p200.aspirate(150, readbuffer).dispense(plate.rows[i])
p200.drop_tip()

