from opentrons import robot, containers, instruments
from itertools import chain

p1000rack = containers.load(
    'tiprack-1000ul',  # container type
    'B1',              # slot
    'p1000-rack'       # user-defined name, optional for now
)
p200rack = containers.load(
    'tiprack-200ul',  # container type
    'A2',             # slot
    'p200-rack'       # user-defined name, optional for now
)
trough = containers.load(
    'trough-12row',
    'A3',
    'trough'
)
tube = containers.load(
    'tube-rack-2ml',
    'A1',
    'tube rack'
)
plate1 = containers.load(
    '96-deep-well',
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
    'B2',
    'trash'
)
    
p200 = instruments.Pipette(
    name="p200", # optional
    trash_container=trash,
    tip_racks=[p200rack],
    min_volume=20, # actual minimum volume of the pipette
    max_volume=200,
    axis="a",
    channels=8 # 
)
p1000 = instruments.Pipette(
    name="p1000", # optional
    trash_container=trash,
    tip_racks=[p1000rack],
    min_volume=1, # actual minimum volume of the pipette
    max_volume=1000,
    axis="b",
    channels=1 # 1 o
)

# distrubte samples in duplicate to A and E, 1 tube to 2 wells

# ----------------------------------------
# dispense tubes into A and E
dest_iter = chain(plate1.cols['A'], plate1.cols['E'])

for well in tube[:12]:
    p1000.pick_up_tip()
    p1000.aspirate(600, well)
    p1000.dispense(600, next(dest_iter))
    p1000.aspirate(600, well)
    p1000.dispense(600, next(dest_iter))
    p1000.drop_tip()


# ----------------------------------------

# distribute buffer to all non A/E wells
p1000.pick_up_tip()
dispense_volume = 300
for char in 'BCDFGH':
    for well in plate1.cols[char]:
        if p1000.current_volume < dispense_volume:
            p1000.aspirate(900, trough['A1'])
        p1000.dispense(300, well)
p1000.drop_tip()

# ----------------------------------------

# dilute down rows from A to D
for i in range(12):
    p1000.pick_up_tip()
    for j in range(3):
        p1000.aspirate(300, plate1.rows[i][j]).dispense(plate1.rows[i][j+1]).mix(3, 300, plate1.rows[i][j+1])
    p1000.drop_tip()

# dilute down rows from E to H
for i in range(12):
    p1000.pick_up_tip()
    for j in range(4,7):
        p1000.aspirate(300, plate1.rows[i][j]).dispense(plate1.rows[i][j+1]).mix(3, 300, plate1.rows[i][j+1])
    p1000.drop_tip()

# ----------------------------------------

# dispense 200 uL to every even row
for i in range(1,12,2):
    well = plate1.rows[i]
    tip = p200rack.rows[i]
    p200.pick_up_tip(tip).aspirate(200, trough['A1']).dispense(well).drop_tip(tip)





