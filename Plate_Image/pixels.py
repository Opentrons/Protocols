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

# how many uL to put in each well
distribute_volume = 50

# the source of our blue, yellow, and green food coloring
blue_source = trough['A1']
yellow_source = trough['A2']
green_source = trough['A3']

# edit the plate map list to draw new images!
b = blue_source
y = yellow_source
g = green_source
_ = None
pixels = [[_, _, _, _, _, _, y, b],  # 12
          [_, _, _, _, y, y, b, _],  # 11
          [_, _, _, _, y, b, _, _],  # 10
          [_, _, y, y, b, b, b, g],  # 9
          [_, _, y, b, b, b, b, g],  # 8
          [y, y, b, b, b, b, b, _],  # 7
          [_, y, b, b, b, b, b, _],  # 6
          [y, y, b, b, b, b, b, _],  # 5
          [_, y, b, b, b, b, b, g],  # 4
          [_, _, y, b, b, b, b, g],  # 3
          [_, _, _, b, b, _, _, _],  # 2
          [_, _, _, b, b, _, _, _]]  # 1
         # A  B  C  D  E  F  G  H

# convert list of row lists into single pixels list
pixels = [pixel for row in reversed(pixels) for pixel in row]


# define a function to spread any given color
def spread_color(color_source, volume):
    global pixels, plate, p200

    # find the target wells for this color
    target_wells = [plate[i] for i in range(96) if pixels[i] is color_source]

    # get a new tip, and distribute the color
    p200.pick_up_tip()
    for t_well in target_wells:
        if p200.current_volume < volume:
            p200.aspirate(color_source).delay(1).touch_tip()
        p200.dispense(volume, t_well).touch_tip()
    p200.blow_out(color_source).return_tip()


# now draw the pixels, one color at a time
spread_color(blue_source, 50)
spread_color(yellow_source, 50)
spread_color(green_source, 50)
