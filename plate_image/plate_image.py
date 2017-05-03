"""
Plate Image

Demonstrates drawing an image in a 96 well plate,
by first designing that image in a Python list.
"""

tip_rack = containers.load('tiprack-200ul', 'B1')
trough = containers.load('trough-12row', 'C1')
plate = containers.load('96-PCR-flat', 'D1')

p200 = instruments.Pipette(
    axis="a",
    max_volume=200,
    tip_racks=[tip_rack]
)

# edit the plate map list to draw new images!
_ = None
image = [
    _, _, _, _, _, _, 2, 1,  # 12
    _, _, _, _, 2, 2, 1, _,  # 11
    _, _, _, _, 2, 1, _, _,  # 10
    _, _, 2, 2, 1, 1, 1, 1,  # 9
    _, _, 2, 1, 1, 1, 1, 1,  # 8
    2, 2, 1, 1, 1, 1, 1, _,  # 7
    _, 2, 1, 1, 1, 1, 1, _,  # 6
    2, 2, 1, 1, 1, 1, 1, _,  # 5
    _, 2, 1, 1, 1, 1, 1, 1,  # 4
    _, _, 2, 1, 1, 1, 1, 1,  # 3
    _, _, _, 1, 1, _, _, _,  # 2
    _, _, _, 1, 1, _, _, _   # 1
]
  # A  B  C  D  E  F  G  H

# lists to save the wells
color_1_wells = []
color_2_wells = []

# loop through the numbers 0-95
for i in range(96):
    if image[i] is 1:
        color_1_wells.append(plate.wells(i))  # save the well
    if image[i] is 2:
        color_2_wells.append(plate.wells(i))  # save the well

# distribute the source colors to the saved wells
p200.distribute(50, trough.wells('A1'), color_1_wells)
p200.distribute(50, trough.wells('A2'), color_2_wells)
