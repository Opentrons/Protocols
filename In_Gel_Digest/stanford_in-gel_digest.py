# In-Gel Digest Protocol Full Hoodbot / RoasaM @ Stanford University
# Mass Spectrometry / Opentrons
from opentrons import containers, instruments


tip_rack = containers.load('tiprack-200ul', 'D1', 'Tip Rack')
waste = containers.load('point', 'D2', 'Trash')
tube_rack = containers.load('tube-rack-2ml', 'C1', 'Tube Rack')
cold_deck = containers.load('tube-rack-2ml', 'A1', 'Cold Deck')

p200 = instruments.Pipette(
    axis="b",
    max_volume=200,
    min_volume=20,
    trash_container=waste,
    tip_racks=[tip_rack],
    name="p200")

cold_tubes = cold_deck.wells('A1', 'B1', 'C1', 'C1')

volumes = [100, 150, 100, 100]
delays = [30, 30, 5, 5]
for i in range(4):
    p200.distribute(
        volumes[i],
        cold_tubes[i],
        tube_rack.wells('A1', length=20))
    p200.delay(minutes=delays[i])
    p200.transfer(
        150,
        tube_rack.wells('A1', length=20),
        waste,
        new_tip='always')

# Trypsin Digestion
# (1 ug Trypsin in ProteaseMax and 50 mM Ammonium Bicarbonate)
# Adding Protease (No Tip Change)
p200.distribute(
    25, cold_deck.wells('D1'), tube_rack.wells('A1', length=20))
