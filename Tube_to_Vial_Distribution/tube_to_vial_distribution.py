from opentrons import containers, instruments

p1000rack = containers.load('tiprack-1000ul','A1','p1000rack')
falcon_tubes = containers.load('tube-rack-15_50ml','C1','tuberack')
vial_rack = containers.load('tube-rack-2ml','D1','vialrack')
trash = containers.load('point','B2','trash')

p1000 = instruments.Pipette(
    name="p1000",
    trash_container=trash,
    tip_racks=[p1000rack],
    max_volume=1000,
    min_volume=100, 
    axis="b",
    channels=1
)

for i in range(6):
	p1000.pick_up_tip(falcon_tubes[i]).dispense(vial_rack[i]).drop_tip()