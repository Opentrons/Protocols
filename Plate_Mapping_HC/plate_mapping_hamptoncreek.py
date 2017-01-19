from opentrons import robot, containers, instruments
from itertools import chain

p200rack = containers.load(
    'tiprack-200ul',  # container type
    'A2',             # slot
    'p200-rack'         # user-defined name, optional for now
)
plate1 = containers.load(
    '96-PCR-flat',
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
    'B3',
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

dest_plates = [plate2, plate3, plate4, plate5, plate6, plate7]

# map 90 uL to all even rows of all 6 destination plates
dispense_volume = 90
for i in range(1,12,2):
    source = plate1.rows[i]
    tip = p200rack.rows[i]
    p200.pick_up_tip(tip).aspirate(180, source)
    for plate in dest_plates:
        dest = plate.rows[i]
        if p200.current_volume < dispense_volume:
            p200.aspirate(180, source) 
        p200.dispense(dispense_volume, dest)
    p200.drop_tip(tip)
    
# map 45 uL to all odd rows of all 6 destination plates
dispense_volume = 45
for i in range(0,11,2):
    source = plate1.rows[i]
    tip = p200rack.rows[i]
    p200.pick_up_tip(tip).aspirate(200)
    for dest in dest_plates:
        dest = dest.rows[i]
        print(dest)
        if p200.current_volume < dispense_volume:
            p200.aspirate(180, source)
        p200.dispense(dispense_volume, dest)
    p200.drop_tip(tip)


