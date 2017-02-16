from opentrons import robot, containers, instruments
from itertools import chain
import math

p10rack = containers.load(
    'tiprack-10ul',  
    'A1',             
    'p10rack'        
)
p200rack = containers.load(
    'tiprack-200ul',  
    'A2',             
    'p200rack'        
)
trash = containers.load(
    'point', 
    'B2', 
    'trash'
)
output_plate = containers.load(
    '96-PCR-flat',
    'E1',
    'output_plate'
)
mag_plate = containers.load(
    '96-PCR-tall',
    'D2',
    'mag_plate'
)
trough = containers.load(
    'trough-12row',
    'C1',
    'trough'
)

#pipette

p10 = instruments.Pipette(
    name="p10",
    min_volume=1,
    max_volume=10,
    axis="b",
    trash_container=trash,
    tip_racks=[p10rack],
    channels=1
)

p200 = instruments.Pipette(
    name="p200",
    min_volume=20,
    max_volume=200,
    axis="a",
    trash_container=trash,
    tip_racks=[p200rack],
    channels=8
)

mag_deck = instruments.Magbead()

# Variables set by user

# List of DNA volumes
samples = [9, 10, 9, 10]

# Set location for mag bead stock
mag_beads_stock = trough['A1']

# incubation time
mag_incubation_time = 900

# time on magnetic bead station
mag_deck_delay = 120

# location of ethanol stock
ethanol_stock = trough['A2']

# volume of ethanol to add to beads
ethanol_volume = 200

# number ethanol washes
ethanol_washes = 2

# ethanol delay
ethanol_delay = 30

# buffer location
buffer_stock = trough['A3']

# buffer volume
buffer_volume = 20

# buffer delay
buffer_delay = 300

# mag deck buffer delay
mag_deck_buffer_delay = 300

# final volume
final_volume = 20

# Calculate Variables

# Get number of samples to use in loop
num_samples = len(samples)
num_rows = math.ceil(num_samples/8)

# Add beads to samples based on DNA volume
for i in range(num_samples):
    mag_vol = ((samples[i])*8)/10  # calculate volume of mag bead to add based on sample volume
    well = mag_plate[i]  # set location of where DNA is located
    p10.pick_up_tip().aspirate(mag_vol, mag_beads_stock)  # aspirate correct volume from mag bead stock
    p10.dispense(well.top()).blow_out() # dispense mag beads to top of tube, blow out
    p10.mix(5, mag_vol, well.bottom())  # mix at bottom of well
    p10.drop_tip() # drop tip in trash

# Incubate at room temp and engage mag beads

# home robot
#robot.home(enqueue=True)

# incubate at room temp for 15 minutes
p10.delay(mag_incubation_time)

# engage the magnet
mag_deck.engage()
p10.delay(mag_deck_delay)

#Remove supernatent from samples and deposit in trash

for i in range(num_samples):  # for all samples
    well = (mag_plate[i].bottom(1))  # set aspirate position for just above the bottom of the plate
    vol = (((samples[i])*8)/10) + samples[i]  # set volume to DNA + mag bead volume
    
    if vol > p10.max_volume:
        volhalf = vol/2
        p10.pick_up_tip().aspirate(volhalf, well, rate=0.5).blow_out(trash)
        p10.aspirate(volhalf, well, rate=0.5).drop_tip()  # use a new tip for each well
    else:
        p10.pick_up_tip().aspirate(vol, well, rate=0.5).drop_tip()

# dispense ethanol based on wash volume

new_volume = ethanol_volume/2 # divide ethanol volume in two to leave room for air
air_volume = p200.max_volume - new_volume # air volume is difference between ethanol and max volume
    
wash_counter = 0 # set wash counter to 0


while wash_counter < ethanol_washes: # loop through for as many washes as desired
    
    for i in range(num_rows):
        well = mag_plate.rows[i].top() # deposit ethanol to top of mag bead plate
        air = ethanol_stock.top(2) # pull air from right above ethanol stock to minimize loss
        p200.pick_up_tip().aspirate(new_volume, ethanol_stock).aspirate(air_volume, air).dispense(well) # add ethanol to well
        p200.aspirate(new_volume, ethanol_stock).aspirate(air_volume, air).dispense(well) # add ethanol to well
        
        p200.delay(ethanol_delay) # delay
        
        well = mag_plate[i].bottom(1) # pull ethanol from bottom of mag bead plate
        air = mag_plate[i].top() # pull air from right above mag bead plate
        p200.aspirate(new_volume, well).aspirate(air_volume, air).dispense(trash)
        p200.aspirate(new_volume, well).aspirate(air_volume, air).drop_tip()     
        
    wash_counter += 1


# Disengage magnets, resuspend samples, delay 5 min, engage magents 5 min

# release magnets
mag_deck.disengage()

# add resuspension buffer to all samples and mix
for i in range(num_rows):
    well = mag_plate.rows[i]
    p200.pick_up_tip().aspirate(buffer_volume, buffer_stock).dispense(well).mix(5, buffer_volume, well).drop_tip()
    
#robot.home(enqueue=True)
p200.delay(buffer_delay)

mag_deck.engage()
p200.delay(mag_deck_buffer_delay)

# remove 20 uL from mag bead deck and send to output plate
for i in range(num_rows):
    well = mag_plate.rows[i]
    output = output_plate.rows[i]
    p200.pick_up_tip().aspirate(final_volume, well).dispense(output).drop_tip()
