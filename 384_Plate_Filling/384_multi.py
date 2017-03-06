from opentrons import robot, instruments, containers

robot.head_speed(5500)

tiprack = containers.load('tiprack-200ul', 'A1', 'p200rack')
trough = containers.load('trough-12row', 'E1', 'trough')
plate = containers.load('384-plate', 'C1', 'plate')
trash = containers.load('point', 'B2', 'trash')

p200 = instruments.Pipette(
	name = 'p200',
	trash_container = trash,
	tip_racks = [tiprack],
	min_volume = 0.5,
	max_volume = 10,
	axis = 'a',
	channels = 8
)

p200.pick_up_tip()
dispense_volume = 1
for i in range(24):
	if p200.current_volume < dispense_volume:
		p200.aspirate(trough['A1'])
	p200.dispense(dispense_volume, plate.rows[i][0])#.touch_tip(-5)
	p200.dispense(dispense_volume, plate.rows[i][1])#.touch_tip(-5)
p200.drop_tip()