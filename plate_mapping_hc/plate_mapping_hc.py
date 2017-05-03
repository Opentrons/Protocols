from opentrons import robot, containers, instruments


p200rack = containers.load('tiprack-200ul', 'A2')
trash = containers.load('point', 'B3')

plate1 = containers.load('96-PCR-flat', 'C2')
plate2 = containers.load('96-PCR-flat', 'D1')
plate3 = containers.load('96-PCR-flat', 'D2')
plate4 = containers.load('96-PCR-flat', 'D3')
plate5 = containers.load('96-PCR-flat', 'E1')
plate6 = containers.load('96-PCR-flat', 'E2')
plate7 = containers.load('96-PCR-flat', 'E3')

p200_multi = instruments.Pipette(
    axis="a",
    name='p200_multi',
    max_volume=200,
    min_volume=10,
    channels=8,
    trash_container=trash,
    tip_racks=[p200rack]
)

dest_plates = [plate2, plate3, plate4, plate5, plate6, plate7]

# map 45 uL to all odd rows of all 6 destination plates
for i in range(0, 12, 2):
    target_rows = [plate.rows(i) for plate in dest_plates]
    p200_multi.distribute(45, plate1.rows(i), target_rows)

# map 90 uL to all even rows of all 6 destination plates
for i in range(1, 12, 2):
    target_rows = [d.rows(i) for d in dest_plates]
    p200_multi.distribute(90, plate1.rows(i), target_rows)
