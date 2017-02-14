"""
Pixels

Demonstrates drawing an image in a 96 well plate,
by first designing that image in a Python list.
"""

from opentrons import containers, instruments

tip_rack = containers.load('tiprack-200ul', 'B1')
trough = containers.load('trough-12row', 'C1')
plate = containers.load('96-PCR-flat', 'D1')

p200 = instruments.Pipette(
    axis="b",
    max_volume=200,
    tip_racks=[tip_rack]
)

# edit the plate map list to draw new images!
b = trough['A1']
g = trough['A2']
_ = None
plate_image = [[_, _, _, _, _, _, g, b],  # 12
               [_, _, _, _, g, g, b, _],  # 11
               [_, _, _, _, g, b, _, _],  # 10
               [_, _, g, g, b, b, b, b],  # 9
               [_, _, g, b, b, b, b, b],  # 8
               [g, g, b, b, b, b, b, _],  # 7
               [_, g, b, b, b, b, b, _],  # 6
               [g, g, b, b, b, b, b, _],  # 5
               [_, g, b, b, b, b, b, b],  # 4
               [_, _, g, b, b, b, b, b],  # 3
               [_, _, _, b, b, _, _, _],  # 2
               [_, _, _, b, b, _, _, _]]  # 1
              # A  B  C  D  E  F  G  H

# convert "plate_image" lists into one-dimensional "pixels" list
# and reverse the rows so that the bottom row is at index 0
pixels = [pixel for row in reversed(plate_image) for pixel in row]

# find the individual wells for each color source
blue_wells = [plate[i] for i in range(96) if pixels[i] is b]
green_wells = [plate[i] for i in range(96) if pixels[i] is g]

# now draw the pixels, one color at a time
p200.distribute(50, b, blue_wells)
p200.distribute(50, g, green_wells)
