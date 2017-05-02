from opentrons import robot, containers, instruments


p1000rack = containers.load(
    'tiprack-1000ul', 
    'A3', 
    'p1000rack'
)

plate = containers.load(
    'rigaku-compact-crystallization-plate', # make crystallization plate container and change
    'C2',
    'plate'
)
matrixblock = containers.load(
    '96-PCR-flat', # make matrix block container and change
    'C3',
    'matrixblock'
)
trash = containers.load(
    'point',
    'D1',
    'trash')
p1000 = instruments.Pipette(   
        axis="b",
        max_volume=1000,
        min_volume=1,
        tip_racks=[p1000rack],
        trash_container=trash,
        channels=1,
        name="p1000"
)



p1000.pick_up_tip().aspirate(1000, matrixblock['A1'])
for i in range(96):
    p1000.dispense(1, plate[i]).dispense(plate[i+96])

