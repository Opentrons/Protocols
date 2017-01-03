
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

p200rack = containers.load(
    'tiprack-200ul',  # container type
    'A2',             # slot
    'p200-rack'         # user-defined name, optional for now
)
plate1 = containers.load(
    '96-PCR-flat',
    'C2',
    'plate1'
)
plate2 = containers.load(
    '96-PCR-flat',
    'D1',
    'plate2'
)
plate3 = containers.load(
    '96-PCR-flat',
    'D2',
    'plate3'
)
plate4 = containers.load(
    '96-PCR-flat',
    'D3',
    'plate4'
)
plate5 = containers.load(
    '96-PCR-flat',
    'E1',
    'plate5'
)
plate6 = containers.load(
    '96-PCR-flat',
    'E2',
    'plate6'
)
plate7 = containers.load(
    '96-PCR-flat',
    'E3',
    'plate7'
)
trash = containers.load(
    'point',
    'B3',
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

dest_plates = [plate2, plate3, plate4, plate5, plate6, plate7]

# map 90 uL to all even rows of all 6 destination plates
dispense_volume = 90
for i in range(1,12,2):
    source = plate1.rows[i]
    tip = p200rack.rows[i]
    p200.pick_up_tip(tip).aspirate(180, source)
    for plate in dest_plates:
        dest = plate.rows[i]
        if p200.current_volume < dispense_volume:
            p200.aspirate(180, source) 
        p200.dispense(dispense_volume, dest)
    p200.drop_tip(tip)
    
# map 45 uL to all odd rows of all 6 destination plates
dispense_volume = 45
for i in range(0,11,2):
    source = plate1.rows[i]
    tip = p200rack.rows[i]
    p200.pick_up_tip(tip).aspirate(200)
    for dest in dest_plates:
        dest = dest.rows[i]
        print(dest)
        if p200.current_volume < dispense_volume:
            p200.aspirate(180, source)
        p200.dispense(dispense_volume, dest)
    p200.drop_tip(tip)


