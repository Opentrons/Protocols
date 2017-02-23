#In-Gel Digest Protocol Full Hoodbot_RM @ Stanford University Mass Spectrometry_DC @ Opentrons
from opentrons import robot, containers, instruments

#Containers
tip_rack = containers.load('tiprack-200ul', 'D1', 'Tip Rack')
waste = containers.load('point', 'D2', 'Trash')
tube_rack = containers.load('tube-rack-2ml','C1', 'Tube Rack')
cold_deck = containers.load('tube-rack-2ml', 'A1', 'Cold Deck')

#Pipette
p200 = instruments.Pipette(
    axis="b",
    channels=1,
    max_volume = 200,
    min_volume = 20,
    trash_container=waste,
    tip_racks=[tip_rack],
    name="p200")

robot.head_speed(6000)

#Reduction
p200.pick_up_tip()
dispense_volume = 100
for i in range(20):
    if p200.current_volume < dispense_volume:
        p200.aspirate(100,cold_deck['A1']).dispense(100,tube_rack[i].top())
p200.drop_tip().delay(1800)

#Alkylation
#Removing DTT/AB (Tip Change)
for i in range(20):
    p200.pick_up_tip()
    p200.aspirate(150, tube_rack[i].bottom()).dispense(waste)
    p200.drop_tip()
    
#Adding Acrylamide/AB (No Tip Change)  
p200.pick_up_tip()
dispense_volume = 150
for i in range(20):
    if p200.current_volume < dispense_volume:
        p200.aspirate(150, cold_deck['B1']).dispense(150, tube_rack[i].top())
p200.drop_tip().delay(1800)

#Wash1
#Removing Acrylamide/AB (Tip Change)
for i in range(20):
    p200.pick_up_tip()
    p200.aspirate(150,tube_rack[i].bottom()).dispense(waste)
    p200.drop_tip()

#Adding Wash1 (No Tip Change)
p200.pick_up_tip()
dispense_volume = 100
for i in range(20):
    if p200.current_volume < dispense_volume:
        p200.aspirate(100, cold_deck['C1']).dispense(100,tube_rack[i].top())
p200.drop_tip().delay(300)

#Wash2
#Removing Wash1 (Tip Change)
for i in range(20):
    p200.pick_up_tip()
    p200.aspirate(150,tube_rack[i]).dispense(waste)
    p200.drop_tip()

#Adding Wash2 (No Tip Change)
p200.pick_up_tip()
dispense_volume = 100
for i in range(20):
    if p200.current_volume < dispense_volume:
        p200.aspirate(100, cold_deck['C1']).dispense(100,tube_rack[i].top())
p200.drop_tip().delay(300)

#Removing Wash2 (Tip Change)
for i in range(20):
    p200.pick_up_tip()
    p200.aspirate(150,tube_rack[i]).dispense(waste)
    p200.drop_tip()


# In[7]:

#Trypsin Digestion
#Adding Protease (No Tip Change)
p200.pick_up_tip()
dispense_volume = 25
for i in range(20):
    if p200.current_volume < dispense_volume:
        p200.aspirate(25,cold_deck['D1']).dispense(25,tube_rack[i].top())
p200.drop_tip()

#Gel ready for overnight digest at 37C


#Next Day
#Extraction1
#Only to add Extraction Solution *Need to remove peptides by hand
#p200.pick_up_tip()
#dispense_volume = 50
#for i in range(4):
  #  if p200.current_volume < dispense_volume:
     #   p200.aspirate(50,cold_deck['A6']).dispense(50,tube_rack[i])
#p200.drop_tip().delay(1800)

#Extraction2
#Only to add Extraction Solution *Need to remove peptides by hand
#p200.pick_up_tip()
#dispense_volume = 100
#for i in range(4):
  #  if p200.current_volume < dispense_volume:
    #    p200.aspirate(100,cold_deck['A6']).dispense(100,tube_rack[i])
#p200.drop_tip()

#Peptides ready for Speedvac
