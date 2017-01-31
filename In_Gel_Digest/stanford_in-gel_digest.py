# In-Gel Digest Protocol Full Hoodbot / RoasaM @ Stanford University
# Mass Spectrometry / Opentrons
from opentrons import robot, containers, instruments


tip_rack = containers.load('tiprack-200ul', 'D1', 'Tip Rack')
waste = containers.load('point', 'D2', 'Trash')
tube_rack = containers.load('tube-rack-2ml', 'C1', 'Tube Rack')
cold_deck = containers.load('tube-rack-2ml', 'A1', 'Cold Deck')

p200 = instruments.Pipette(
    axis="b",
    channels=1,
    max_volume=200,
    min_volume=20,
    trash_container=waste,
    tip_racks=[tip_rack])

robot.head_speed(6000)

num_tubes = 20

for cold_source in ['A1', 'B1', 'C1', 'C2']:
    p200.distribute(100, cold_deck[cold_source], tube_rack[:num_tubes])
    p200.delay(30 * 60)
    p200.consolidate(
        150, tube_rack[:num_tubes], waste, repeater=False, tips=num_tubes)

# Trypsin Digestion
# (1 ug Trypsin in ProteaseMax and 50 mM Ammonium Bicarbonate)
# Adding Protease (No Tip Change)
p200.distribute(25, cold_deck['D1'], tube_rack[:num_tubes])
p200.delay(10 * 60)

# Covering Gels with 50 mM Ammonium Bicarbonate
p200.distribute(40, cold_deck['D4'], tube_rack[:num_tubes])





# Gel ready for overnight digest at 37C

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