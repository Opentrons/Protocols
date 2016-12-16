
# coding: utf-8


# In[1]:

# # This cell loads in the API
# # and then prints out the serial ports

# # !pip install --upgrade git+git://github.com/OpenTrons/opentrons-api.git@master#egg=opentrons

from opentrons import robot, containers, instruments
from itertools import chain
# # robot.get_serial_ports_list()


# In[ ]:

# this cell connects to a robot and immediately homes
# if .connect() is called without a port, the smoothieboard is simulated

# robot.connect() # virtual smoothieboard
# robot.connect('/dev/tty.usbmodem1421')
# robot.home(now=True)
# robot


# In[2]:

# robot.reset()
# this cells is similar to the Deck and Head sections in a JSON protocol

# Create a JSON protocol with the exact same containers and pipettes as here
# They must be the same type, have the same user-defined names, and pipette's on the same axis (a or b)

p1000rack = containers.load(
    'tiprack-1000ul',  # container type
    'A1',             # slot
    'p1000-rack'         # user-defined name, optional for now
)
p200rack = containers.load(
    'tiprack-200ul',  # container type
    'A2',             # slot
    'p200-rack'         # user-defined name, optional for now
)
trough = containers.load(
    'trough-12row',
    'C1',
    'trough'
)
tube = containers.load(
    'tube-rack-2ml',
    'D1',
    'tube rack'
)
plate1 = containers.load(
    '96-PCR-flat',
    'D2',
    'plate1'
)
plate2 = containers.load(
    '96-PCR-flat',
    'E2',
    'plate2'
)
plate3 = containers.load(
    '96-PCR-flat',
    'A3',
    'plate3'
)
plate4 = containers.load(
    '96-PCR-flat',
    'B3',
    'plate4'
)
plate5 = containers.load(
    '96-PCR-flat',
    'C3',
    'plate5'
)
plate6 = containers.load(
    '96-PCR-flat',
    'D3',
    'plate6'
)
plate7 = containers.load(
    '96-PCR-flat',
    'E3',
    'plate7'
)
trash = containers.load(
    'point',
    'B2',
    'trash'
)
    
p200 = instruments.Pipette(
    name="p200", # optional
    trash_container=trash,
    tip_racks=[p200rack],
    min_volume=20, # actual minimum volume of the pipette
    axis="a",
    channels=8 # 
)

p200.set_max_volume(200)  # volume calibration, can be called whenever you want

p1000 = instruments.Pipette(
    name="p1000", # optional
    trash_container=trash,
    tip_racks=[p1000rack],
    min_volume=1, # actual minimum volume of the pipette
    axis="b",
    channels=1 # 1 o
)
    
p1000.set_max_volume(1000)

robot.head_speed(5000)
# In[7]:

# distrubte samples in duplicate to A and E, 1 tube to 2 wells

# ----------------------------------------
# dispense tubes into A and E
dest_iter = chain(plate1.cols['A'], plate1.cols['E'])

for well in tube[:12]:
    p1000.aspirate(600, well)
    p1000.dispense(300, next(dest_iter))
    p1000.dispense(300, next(dest_iter))


# ----------------------------------------

# distribute buffer to all non A/E wells
p1000.pick_up_tip()
dispense_volume = 300
for char in 'BCDFGH':
    for well in plate1.cols[char]:
        if p1000.current_volume < dispense_volume:
            p1000.aspirate(900, trough['A1'])
        p1000.dispense(300, well)
p1000.drop_tip()

# ----------------------------------------

# dilute down rows from A to D
for i in range(12):
    p1000.pick_up_tip()
    for j in range(3):
        p1000.aspirate(300, plate1.rows[i][j]).dispense(plate1.rows[i][j+1]).mix(3, 300, plate1.rows[i][j+1])
    p1000.drop_tip()

# dilute down rows from E to H
for i in range(12):
    p1000.pick_up_tip()
    for j in range(4,7):
        p1000.aspirate(300, plate1.rows[i][j]).dispense(plate1.rows[i][j+1]).mix(3, 300, plate1.rows[i][j+1])
    p1000.drop_tip()

# ----------------------------------------

# dispense 200 uL to every even row
for i in range(1,12,2):
    well = plate1.rows[i]
    tip = p200rack.rows[i]
    p200.pick_up_tip(tip).aspirate(200, trough['A1']).dispense(well).drop_tip(tip)





