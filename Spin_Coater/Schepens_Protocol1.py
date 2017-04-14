from opentrons import containers, instruments

p200rack = containers.load('tiprack-200ul', 'A1')
tuberack = containers.load('tube-rack-2ml', 'A2')
trash = containers.load('trash-box', 'A3')
coater = containers.load('point', 'D1')

p200 = instruments.Pipette(
	axis='b',
	max_volume=200,
	tip_racks=[p200rack],
	trash_container=trash
)

#Aspirates 50uL from the tube in the tube rack
#and dispenses the liquid onto the coater
#The amount of liquid to be transferred can
#be changed by adjusting the first number in the
#following code 
p200.transfer(
	50,
	tuberack.wells('A1'),
	coater,
	new_tips='once'
)
