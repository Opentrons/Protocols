
# coding: utf-8

# In[ ]:

#!pip install --upgrade opentrons


# In[1]:

from opentrons import robot, containers, instruments


# In[2]:


p200rack = containers.load(
    'tiprack-200ul', 
    'A1',
    'p200rack')

trash = containers.load(
    'point',
    'A2',
    'trash'
)
tube_rack = containers.load(
    'tube-rack-2ml',
    'C2',
    'tube_rack'
)
plate = containers.load(
    '384-plate',
    'C1',
    'plate'
)

p200 = instruments.Pipette(
        axis="b",
        max_volume=200,
        min_volume=20,
        tip_racks=[p200rack],
        trash_container=trash,
        channels=1,
        name="p200"
)


# In[3]:

# dispense 40 uL from tube to plate, for 24 tubes
for i in range(24):
    p200.pick_up_tip().aspirate(40, tube_rack[i]).dispense(plate[i]).drop_tip()


