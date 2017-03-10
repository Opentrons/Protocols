from opentrons import robot, containers, instruments

tiprack = containers.load('tiprack-200ul', 'A1','tiprack')
tiprack2 = containers.load('tiprack-200ul', 'A2','tiprack2')
DNA_plate = containers.load('96-flat', 'C1','DNA_plate') 
PCR_plate = containers.load('96-flat', 'C2','PCR_plate') 
trough = containers.load('trough-12row', 'D1', 'trough')
trash = containers.load('point','A3','trash')

p50 = instruments.Pipette(
        axis="a",
        max_volume=50,
        min_volume=5,
        tip_racks=[tiprack, tiprack2],
        trash_container=trash,
        channels=8,
        name="p50"
)

target_MM = trough['A1']
control_MM = trough['A2']

# add target gene master mix to PCR plate
p50.pick_up_tip()
for i in range(6):
	if p50.current_volume < 20:
		p50.aspirate(target_MM)
	p50.dispense(20, PCR_plate.rows[i])
p50.drop_tip()

# add control gene master mix to PCR plate
p50.pick_up_tip()
for i in range(7,12):
	if p50.current_volume < 15:
		p50.aspirate(control_MM)
	p50.dispense(15, PCR_plate.rows[i])
p50.drop_tip()

# transfer samples from DNA plate to PCR plate, changing tips each time you pick up a sample
for i in range(6):
	p50.pick_up_tip()
	p50.aspirate(10, DNA_plate.rows[i])
	p50.dispense(5, PCR_plate.rows[i]).dispense(5, PCR_plate.rows[i+6])
	p50.drop_tip()


	
	
