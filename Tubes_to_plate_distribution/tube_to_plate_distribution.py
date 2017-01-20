from opentrons import robot, containers, instruments

tiprack200 = containers.load(
    'tiprack-200ul',  
    'A1',             
    'tiprack200'         
)
plate = containers.load(
    '96-PCR-flat',  
    'B1',             
    'plate'         
)
tuberack = containers.load(
    'tube-rack-2ml',  
    'C1',             
    'tuberack'         
)
tuberack2 = containers.load(
    'tube-rack-2ml',  
    'D1',             
    'tuberack2'         
)
tuberack3 = containers.load(
    'tube-rack-2ml',  
    'C2',             
    'tuberack3'         
)
tuberack4 = containers.load(
    'tube-rack-2ml',  
    'D2',             
    'tuberack4'         
)
trash = containers.load(
	'point',
	'A3',
	'trash'
)

p200 = instruments.Pipette(
    name="p200",
    trash_container=trash,
    tip_racks=[tiprack200],
    min_volume=50,
    max_volume=200,
    axis="b",
    channels=1
)

for i in range(24):
	p200.pick_up_tip().aspirate(100, tuberack[i]).dispense(plate[i]).drop_tip()

for i in range(24):
	p200.pick_up_tip().aspirate(100, tuberack2[i]).dispense(plate[i+24]).drop_tip()

for i in range(24):
	p200.pick_up_tip().aspirate(100, tuberack3[i]).dispense(plate[i+48]).drop_tip()

for i in range(24):
	p200.pick_up_tip().aspirate(100, tuberack4[i]).dispense(plate[i+72]).drop_tip()
