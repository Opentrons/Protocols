#In-Gel Digest Protocol Full Hoodbot / RoasaM @ Stanford University Mass Spectrometry / Opentrons
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
    tip_racks=[tip_rack])

robot.head_speed(6000)

#Reduction
#(0.2 mL 50 mM DTT in 1.8 mL 50 mM Ammonium Bicarbonate)
p200.pick_up_tip()
dispense_volume = 100
for i in range(20):
    if p200.current_volume < dispense_volume:
        p200.aspirate(100, cold_deck['A1']).dispense(100,tube_rack[i].top()).blow_out(tube_rack[i].top())
p200.drop_tip().delay(1800)

#Alkylation
#(0.2 mL 100 mM Acrylamide in 1.8 mL 50 mM Ammonium Bicarbonate)
#Removing DTT/AB (Tip Change)
for i in range(20):
    p200.pick_up_tip()
    p200.aspirate(150, tube_rack[i].bottom()).dispense(waste)
    p200.drop_tip()
    
#Adding Acrylamide/AB (No Tip Change)  
p200.pick_up_tip()
dispense_volume = 100
for i in range(20):
    if p200.current_volume < dispense_volume:
        p200.aspirate(100, cold_deck['B1']).dispense(100,tube_rack[i].top()).blow_out(tube_rack[i].top())
p200.drop_tip().delay(1800)


#Wash Steps
#(1 mL Acetonitrile in 1 mL 50 mM Ammonium Bicarbonate)

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
        p200.aspirate(100, cold_deck['C1']).dispense(100,tube_rack[i].top()).blow_out(tube_rack[i].top())
p200.drop_tip().delay(600)

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
        p200.aspirate(100, cold_deck['C2']).dispense(100,tube_rack[i].top()).blow_out(tube_rack[i].top())
p200.drop_tip().delay(600)

#Removing Wash2 (Tip Change)
for i in range(20):
    p200.pick_up_tip()
    p200.aspirate(150,tube_rack[i]).dispense(waste)
p200.drop_tip().delay(1800)

#Trypsin Digestion
#(1 ug Trypsin in ProteaseMax and 50 mM Ammonium Bicarbonate)
#Adding Protease (No Tip Change)
p200.pick_up_tip()
dispense_volume = 25
for i in range(20):
    if p200.current_volume < dispense_volume:
        p200.aspirate(25, cold_deck['D1']).dispense(25,tube_rack[i].top()).blow_out(tube_rack[i].top())
p200.drop_tip().delay(600)

#Covering Gels with 50 mM Ammonium Bicarbonate
p200.pick_up_tip()
dispense_volume = 40
for i in range(20):
    if p200.current_volume < dispense_volume:
        p200.aspirate(40, cold_deck['D4']).dispense(40,tube_rack[i].top()).blow_out(tube_rack[i].top())
p200.drop_tip()

#Gel ready for overnight digest at 37C

#Next Day
#Extraction1
#Only to add Extraction Solution *Need to remove peptides by hand
#p200.pick_up_tip()
#dispense_volume = 50
#for i in range(20):
  #  if p200.current_volume < dispense_volume:
     #   p200.aspirate(50,cold_deck['A6']).dispense(50,tube_rack[i])
#p200.drop_tip().delay(1800)

#Extraction2
#Only to add Extraction Solution *Need to remove peptides by hand
#p200.pick_up_tip()
#dispense_volume = 100
#for i in range(20):
  #  if p200.current_volume < dispense_volume:
    #    p200.aspirate(100,cold_deck['A6']).dispense(100,tube_rack[i])
#p200.drop_tip()

#Peptides ready for Speedvac