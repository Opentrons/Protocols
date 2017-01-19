from opentrons import robot, containers, instruments

p50rack = containers.load(
    'tiprack-200ul', # make p20 rack container and change
    'A1', 
    'p50rack'
)
p50rack2 = containers.load(
    'tiprack-200ul', # make p20 rack container and change
    'A2', 
    'p50rack'
)
plate = containers.load(
	'96-PCR-flat',
	'C1',
	'plate'
)
pcr_plate = containers.load(
	'96-PCR-flat',
	'C2',
	'pcr_plate'
)
trash = containers.load(
	'point',
	'A1',
	'trash'
)
p50 = instruments.Pipette(   
        axis="a",
        max_volume=50,
        min_volume=5,
        tip_racks=[p50rack],
        trash_container=trash,
        channels=8,
        name="p50"
)
p50S = instruments.Pipette(   
        axis="b",
        max_volume=5,
        min_volume=50,
        tip_racks=[p50rack2],
        trash_container=trash,
        channels=1,
        name="p50"
)

binding_buffer = trough['A1']
wash_buffer = trough['A2']
elution_buffer = trough['A3']

PCR_vol = 5 # same volume for all?  import from CSV file?

# add normalization buffer
p50S.pick_up_tip()
for i in range (96):
	dispense_volume = PCR_vol
	if p50S.current_volume < dispense_volume:
		p50S.aspirate(binding_buffer)
	p50S.dispense(dispense_volume, plate[i])
p50S.drop_tip()

# add PCR products to normalization plate
for i in range(96):
	p50S.pick_up_tip().aspirate(PCR_vol, pcr_plate[i]).dispense(plate[i]).mix(2, PCR_vol, plate[i]).drop_tip()

# delay 1 hour
p50S.delay(3600)

# aspirate all liquid
for i in range(12):
	p50.pick_up_tip().p50.aspirate(50, plate.rows[i]).dispense(trash['A1'])
	p50.aspirate(50, wash_buffer).dispense(plate.rows[i]).mix(2, 30, plate[i])
	p50.aspirate(50, plate.rows[i]).dispense(trash['A1']).drop_tip()

# sequential elution
p50.pick_up_tip()
for i in range(11):
	p50.aspirate(20, elution_buffer).dispense(plate.rows[i]).mix(5, 20, plate.rows[i])
	p50.aspirate(20, plate.rows[i]).dispense(plate.rows[i+1])

# final plate dispense?
p50.aspirate(20, plate.rows[12]).dispense()


