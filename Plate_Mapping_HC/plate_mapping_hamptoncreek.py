from opentrons import containers, instruments


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
    channels=8,
    trash_container=trash,
    tip_racks=[p200rack]
)

dest_plates = [plate2, plate3, plate4, plate5, plate6, plate7]

# map 90 uL to all even rows of all 6 destination plates
even_rows = [row for dest in dest_plates for row in dest.rows[0::2]]
p200_multi.transfer(90, plate1.rows[0::2], even_rows)

# map 45 uL to all odd rows of all 6 destination plates
odd_rows = [row for dest in dest_plates for row in dest.rows[1::2]]
p200_multi.transfer(45, plate1.rows[1::2], odd_rows)
