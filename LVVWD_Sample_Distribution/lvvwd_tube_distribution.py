from opentrons import robot, containers, instruments

p1000rack = containers.load('tiprack-1000ul', 'A1', 'p1000rack')

vialrack = containers.load('wheaton_vial_rack', 'D1', 'vialrack')

plate = containers.load('96-deep-well', 'B2', 'plate')

trash = containers.load('point', 'B1', 'trash')

p1000 = instruments.Pipette(
	name="p1000",
    trash_container=trash,
    tip_racks=[p1000rack],
    min_volume=100,
    max_volume=1000,
    axis="b",
    channels=1)
    
# Distribute 48 samples to 96 well plate
for i in range(48):
	wellone = plate.cols[i][0]
    welltwo = plate.cols[i][1]
	p1000.pick_up_tip().aspirate(600, plate[i])
	p1000.dispense(300, wellone).dispense(300, welltwo)
	p1000.drop_tip()