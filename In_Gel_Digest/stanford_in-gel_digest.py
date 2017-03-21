# In-Gel Digest Protocol Full Hoodbot / RoasaM @ Stanford University
# Mass Spectrometry / Opentrons
from opentrons import containers, instruments

# add two tube racks
cold_deck = containers.load('tube-rack-2ml', 'A1')
tube_rack = containers.load('tube-rack-2ml', 'C1')

# use p200, with a tiprack and trash
tip_rack = containers.load('tiprack-200ul', 'D1')
waste = containers.load('point', 'D2')
p200 = instruments.Pipette(
    axis="b",
    max_volume=200,
    min_volume=20,
    trash_container=waste,
    tip_racks=[tip_rack])

cold_tubes = cold_deck.wells('A1', 'B1', 'C1', 'C1')
target_tubes = tube_rack.wells('A1', length=20)

p200.distribute(100, cold_tubes['A1'], target_tubes)
p200.delay(minutes=30)
p200.transfer(150, target_tubes, waste, new_tip='always')

p200.distribute(150, cold_tubes['B1'], target_tubes)
p200.delay(minutes=30)
p200.transfer(150, target_tubes, waste, new_tip='always')

p200.distribute(100, cold_tubes['C1'], target_tubes)
p200.delay(minutes=5)
p200.transfer(150, target_tubes, waste, new_tip='always')

p200.distribute(100, cold_tubes['C1'], target_tubes)
p200.delay(minutes=5)
p200.transfer(150, target_tubes, waste, new_tip='always')

p200.distribute(25, cold_deck.wells('D1'), target_tubes)
