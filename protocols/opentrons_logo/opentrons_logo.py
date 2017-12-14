"""
@author Opentrons
@date November 11th, 2017
@version 1.0
"""

from opentrons import containers, instruments, robot
# from collections import defaultdict

robot.reset()

"""
Column A
"""
tiprack = containers.load('tiprack-200ul', 'A1')

# dye1 = containers.load('point', 'A3', 'Dye 1 Container')
# want this to be 'A4' jupyter notebook does not like
"""
Column B
"""
output = containers.load('96-flat', 'B1')

trough = containers.load('trough-12row', 'B3')
"""
Column C
"""
# dye2 = containers.load('point', 'C1', 'Dye 2 Container')
# want this to be 'C4' jupyter notebook does not like
trash = containers.load('fixed-trash', 'C4')


"""
Instruments
"""
p200 = instruments.Pipette(
    mount='right',
    name='p300single',
    max_volume=300,
    min_volume=20,
    channels=1,
    tip_racks=[tiprack],
    trash_container=trash,
    aspirate_speed=120,
    dispense_speed=120)

"""
Well location set-up
"""

dye1_wells = ['A5', 'A6', 'A8', 'A9', 'B4', 'B10', 'C3', 'C11', 'D3', 'D11',
              'E3', 'E11', 'F3', 'F11', 'G4', 'G10', 'H5', 'H6', 'H7', 'H8',
              'H9']

dye2_wells = ['C7', 'D6', 'D7', 'D8', 'E5', 'E6', 'E7', 'E8',
              'E9', 'F5', 'F6', 'F7', 'F8', 'F9', 'G6', 'G7', 'G8']

"""
To use a CSV

dye_coordinates = 'C:\\Users\\Laura\\Documents\\OpentronsLogo.csv'

locations_dict = defaultdict(list)
keys = []
with open(dye_coordinates) as my_file:
    temp_lines = []
    for line in my_file.read().splitlines():
        temp_lines.append(line.split(','))
        keys = keys + line.split(',')
    for col in range(len(temp_lines)):
        for well in range(len(temp_lines[col])):
            locations_dict[temp_lines[col][well].strip()].append(col + well*8)

while '' in keys: keys.remove('')
"""
dye2 = trough.wells('A1')
dye1 = trough.wells('A2')

for d1 in dye1_wells:
    p200.transfer(
        50,
        dye1,
        output.wells(d1).bottom(),
        new_tip='once',
        blow_out=True)

robot.home()
