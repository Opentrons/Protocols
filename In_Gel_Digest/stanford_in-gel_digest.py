# In-Gel Digest Protocol Full Hoodbot / RoasaM @ Stanford University
# Mass Spectrometry / Opentrons
from opentrons import containers, instruments


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
    tip_racks=[tip_rack],
    name="p200")

target_tubes = tube_rack.wells(length=20)

for cold_source in cold_deck.wells(['A1', 'B1', 'C1', 'C2']):
    p200.distribute(100, cold_source, target_tubes)
    p200.delay(30 * 60)
    p200.consolidate(
        150, target_tubes, waste, repeater=False, new_tip='always')

# Trypsin Digestion
# (1 ug Trypsin in ProteaseMax and 50 mM Ammonium Bicarbonate)
# Adding Protease (No Tip Change)
p200.distribute(25, cold_deck.wells('D1'), target_tubes)

p200.delay(10 * 60)

# Covering Gels with 50 mM Ammonium Bicarbonate
p200.distribute(40, cold_deck.wells('D4'), target_tubes)





# Gel ready for overnight digest at 37C


# # Next Day
# # Extraction1
# # Only to add Extraction Solution *Need to remove peptides by hand
# p200.distribute(50, cold_deck.wells('A6'), tube_rack.wells('A1', length=4))
# p200.delay(1800)

# # Extraction2
# # Only to add Extraction Solution *Need to remove peptides by hand
# p200.distribute(100, cold_deck.wells('A6'), tube_rack.wells('A1', length=4))

# # Peptides ready for Speedvac
