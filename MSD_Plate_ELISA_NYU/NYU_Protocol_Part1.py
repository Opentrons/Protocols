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
    min_volume=20,
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

# coat plate with 25 uL PBS
dispense_volume = 25
p200.pick_up_tip()
for i in range(12):
    if p200.current_volume < dispense_volume:
        p200.aspirate(200, PBS)
    p200.dispense(dispense_volume, plate.rows[i])

# incubate RT for 20 min
p200.delay(1200)

# remove PBS
for i in range(12):
    p200.aspirate(40, plate.rows[i]).dispense(trash['A1'])
p200.drop_tip()

# add 30 uL coating solution to entire plate
dispense_volume = 30
p200.pick_up_tip()
for i in range(12):
    if p200.current_volume < dispense_volume:
        p200.aspirate(180, gp120)
    p200.dispense(dispense_volume, plate.rows[i])
p200.drop_tip()