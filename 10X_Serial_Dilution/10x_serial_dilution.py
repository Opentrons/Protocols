from opentrons import robot, containers, instruments
from itertools import chain

p200rack = containers.load(
    'tiprack-200ul',  
    'A1',            
    'p200-rack'         
)
trough = containers.load(
    'trough-12row',
    'D2',
    'trough'
)
plate = containers.load(
    '96-PCR-flat',
    'C1',
    'plate'
)
trash = containers.load(
    'point',
    'B2',
    'trash'
)
    
p200 = instruments.Pipette(
    name="p200", 
    trash_container=trash,
    tip_racks=[p200rack],
    min_volume=20, 
    max_volume=200,
    axis="a",
    channels=8 
)

sample_numbers = 3 # number of samples
sample_location = plate.rows[0] # first row of plate
diluent_location = trough['A1'] # what the samples are diluted with

dilution_number = 6 # how many dilutions
dilution_factor = 10 # dilution factor 10X

sample_volume = 20
diluent_volume = 180

p200.pick_up_tip()
for i in range(1, dilution_number + 1):
    if p200.current_volume < diluent_volume:
        p200.aspirate(trough['A1'])
    p200.dispense(plate.rows[i])
p200.drop_tip()

p200.pick_up_tip()
for row in range(0, dilution_number):
    p200.aspirate(sample_volume, plate.rows[row][0]).dispense(plate.rows[row + 1][0]).mix(3, sample_volume, plate.rows[row + 1][0])
p200.drop_tip() 