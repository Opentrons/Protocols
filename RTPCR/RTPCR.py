from opentrons import robot, containers, instruments

p50rack = containers.load('tiprack-200ul', 'A1', 'p50rack')
tuberack = containers.load('tube-rack-.75ml', 'D2', 'tuberack')
trash = containers.load('point', 'B2', 'trash')
plate = containers.load('96-flat', 'C1', 'plate')

p50 = instruments.Pipette(
    name="p50",
    trash_container=trash,
    tip_racks=[p50rack],
    min_volume=5,
    max_volume=50,
    axis="b",
    channels=1
)

for i in range(12):
    p50.pick_up_tip()
    for well in plate.rows[i]:
        p50.aspirate(15, tuberack[i]).dispense(well)
    p50.drop_tip()

for i in range(8):
    p50.pick_up_tip()
    for well in plate.cols[i]:
        p50.aspirate(15, tuberack[i + 12]).dispense(well)o
    p50.drop_tip()
