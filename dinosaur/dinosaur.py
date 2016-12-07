# Dinosaur

from opentrons import Robot, containers, instruments
from itertools import chain

robot = Robot()

p200rack = containers.load(
    'tiprack-200ul',  
    'B1',             
    'tiprack'         
)
trough = containers.load(
    'trough-12row',
    'C1',
    'trough'
)
plate = containers.load(
    '96-PCR-flat',
    'D1',
    'plate'
)
trash = containers.load(
    'point',
    'D2',
    'trash'
)

p200 = instruments.Pipette(
    name="p200",
    trash_container=trash,
    tip_racks=[p200rack],
    min_volume=20,
    axis="b",
    channels=1
)

p200.set_max_volume(200)


# In[4]:

volume = 200
blue = trough['A1']
green = trough['A2']

# deposit to all blue wells
p200.pick_up_tip(p200rack['A1'])
p200.aspirate(volume, blue)
p200.dispense(50, plate['D1']).dispense(50, plate['E1']).dispense(50, plate['D2']).dispense(50, plate['E2'])
p200.aspirate(volume, blue)
p200.dispense(50, plate['D3']).dispense(50, plate['E3']).dispense(50, plate['F3']).dispense(50, plate['G3'])
p200.aspirate(volume, blue)
p200.dispense(50, plate['H3']).dispense(50, plate['C4']).dispense(50, plate['D4']).dispense(50, plate['E4'])
p200.aspirate(volume, blue)
p200.dispense(50, plate['F4']).dispense(50, plate['G4']).dispense(50, plate['H4']).dispense(50, plate['C5'])
p200.drop_tip(p200rack['A1'])

p200.pick_up_tip(p200rack['B1'])
p200.aspirate(volume, blue)
p200.dispense(50, plate['D5']).dispense(50, plate['E5']).dispense(50, plate['F5']).dispense(50, plate['G5'])
p200.aspirate(volume, blue)
p200.dispense(50, plate['C6']).dispense(50, plate['D6']).dispense(50, plate['E6']).dispense(50, plate['F6'])
p200.aspirate(volume, blue)
p200.dispense(50, plate['G6']).dispense(50, plate['C7']).dispense(50, plate['D7']).dispense(50, plate['E7'])
p200.aspirate(volume, blue)
p200.dispense(50, plate['F7']).dispense(50, plate['G7']).dispense(50, plate['D8']).dispense(50, plate['E8'])
p200.drop_tip(p200rack['B1'])

p200.pick_up_tip(p200rack['C1'])
p200.aspirate(volume, blue)
p200.dispense(50, plate['F8']).dispense(50, plate['G8']).dispense(50, plate['H8']).dispense(50, plate['E9'])
p200.aspirate(volume, blue)
p200.dispense(50, plate['F9']).dispense(50, plate['G9']).dispense(50, plate['H9']).dispense(50, plate['F10'])
p200.aspirate(volume, blue)
p200.dispense(50, plate['G11']).dispense(50, plate['H12']).dispense(50, plate['F3']).dispense(50, plate['G3'])
p200.drop_tip(p200rack['C1'])
              
# deposit to all green wells
p200.pick_up_tip(p200rack['D1'])
p200.aspirate(volume, green)
p200.dispense(50, plate['C3']).dispense(50, plate['B4']).dispense(50, plate['A5']).dispense(50, plate['B5'])
p200.aspirate(volume, green)
p200.dispense(50, plate['B6']).dispense(50, plate['A7']).dispense(50, plate['B7']).dispense(50, plate['C8'])              
p200.aspirate(volume, green)
p200.dispense(50, plate['C9']).dispense(50, plate['D9']).dispense(50, plate['E10']).dispense(50, plate['E11'])              
p200.aspirate(volume, green)
p200.dispense(50, plate['F11']).dispense(50, plate['G12'])
p200.drop_tip(p200rack['D1'])



