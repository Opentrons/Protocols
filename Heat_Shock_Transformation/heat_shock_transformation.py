
# coding: utf-8

# In[ ]:

# This cell loads in the API
# and then prints out the serial ports

#!pip install --upgrade opentrons

from opentrons import robot, containers, instruments

robot = Robot()


# In[ ]:

# this cell connects to a robot and immediately homes
# if .connect() is called without a port, the smoothieboard is simulated

#robot.connect()
# robot.connect('/dev/tty.usbmodem1421')
#robot.home()


# In[ ]:

# this cells is similar to the Deck and Head sections in a JSON protocol

# Create a JSON protocol with the exact same containers and pipettes as here
# They must be the same type, have the same user-defined names, and pipette's on the same axis (a or b)

tiprack200 = containers.load(
    'tiprack-200ul',  
    'A2',             
    'tiprack200'         
)
tiprack10 = containers.load(
    'tiprack-10ul',  
    'B1',             
    'tiprack10'         
)
tube_rack = containers.load(
    'tube-rack-2ml',
    'D1',
    'trough'
)
cold_deck = containers.load(
    'tube-rack-2ml',
    'D3',
    'cold_deck'
)
trash = containers.load(
    'point',
    'B2',
    'trash'
)
heat_deck = containers.load(
    'tube-rack-2ml',
    'B3',
    'heat_deck'
)
    

p200 = instruments.Pipette(
    name="p200",
    trash_container=trash,
    tip_racks=[tiprack200],
    min_volume=50,
    axis="b",
    channels=1
)

p10 = instruments.Pipette(
    name="p10",
    trash_container=trash,
    tip_racks=[tiprack10],
    min_volume=1,
    axis="a",
    channels=1
)

p200.set_max_volume(200)  # volume calibration, can be called whenever you want
p200L.set_max_volume(200)


# In[ ]:

DNA_delay = 1800
heat_shock_delay = 60
cold_delay = 300

DNA_vol = 2
cell_vol = 25
total_vol = DNA_volume + Cell_vol
LB_vol = 200

# two sample protocol

# add DNA from tube B to tube A in cold deck
p10.pick_up_tip()
p10.aspirate(DNA_vol, cold_deck['B1']).dispense(cold_deck['A1']).touch_tip().mix(3, 10, cold_deck['A1'])
p10.drop_tip()

p10.pick_up_tip()
p10.aspirate(DNA_vol, cold_deck['B2']).dispense(cold_deck['A2']).touch_tip().mix(3, 10, cold_deck['A2'])
p10.drop_tip()

# delay after adding DNA
p10.delay(DNA_delay)

# move dna/cells from cold deck to heat deck and then back
p200.pick_up_tip()
p200.aspirate(total_vol, cold_deck['A1']).dispense(heat_deck['A1']).touch_tip()
p200.delay(heat_shock_delay)
p200.aspirate(total_vol, heat_deck['A1']).dispense(cold_deck['A1']).touch_tip()
p200.drop_tip()

p200.pick_up_tip()
p200.aspirate(total_vol, cold_deck['A2']).dispense(heat_deck['A2']).touch_tip()
p200.delay(heat_shock_delay)
p200.aspirate(total_vol, heat_deck['A2']).dispense(cold_deck['A2']).touch_tip()
p200.drop_tip()

# delay after heat shock
p200.delay(cold_delay)

# add LB to dna/cells
p200.pick_up_tip()
p200.aspirate(LB_vol, tube_rack['A1']).dispense(cold_deck['A1'])
p200.drop_tip()

p200.pick_up_tip()
p200.aspirate(LB_vol, tube_rack['A2']).dispense(cold_deck['A2'])
p200.drop_tip()

