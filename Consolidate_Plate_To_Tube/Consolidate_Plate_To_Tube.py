from opentrons import robot, containers, instruments

plate = containers.load(
    '96-PCR-tall', 
    'C1', 
    'plate'
)
tube_rack = containers.load(
    'tube-rack-2ml', 
    'D1', 
    'tube_rack'
)
p200rack = containers.load(
    'tiprack-200ul', 
    'A1', 
    'p200rack'
)
trash = containers.load(
    'point',
    'B2',
    'trash'
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

# Explanation:
# Pull 20 uL from each well in a 96 well plate and consolidate in one 1.5 mL tube.
# No need to change tips when picking up from a new well.
# Pick up liquid until pipette is full, then deposit in tube.  Change tips and repeat until end of plate.
# Currently is 20 uL, but would like to be able to change volume to any other volume.

# split the plate into chunks based on how many wells can fit into the pipette at a time
def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]

# volume being pulled from each well
volume = 20

# destination tube
tube = tube_rack['A1']

# how many wells can fit into each pipette
samples_per_pipette = p200.max_volume // volume      

# this function will aspirate from each well in the chunk and deposit it into the tube
# then it will go to the next chunk, using a new pipette tip every time
for chunk in chunks(plate, samples_per_pipette):
    p200.pick_up_tip()
    for well in chunk:
        p200.aspirate(volume, well)
        
    p200.dispense(tube)
    p200.drop_tip()