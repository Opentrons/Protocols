from opentrons import containers, instruments


p10rack = containers.load('tiprack-10ul', 'A1')
p200rack = containers.load('tiprack-200ul', 'A1')
output_plate = containers.load('96-PCR-flat', 'B1')
mag_plate = containers.load('96-PCR-tall', 'C1')
trough = containers.load('trough-12row', 'B1')
trash = containers.load('point', 'A2')

mag_deck = instruments.Magbead()

p10 = instruments.Pipette(
    axis="b",
    max_volume=10,
    trash_container=trash,
    tip_racks=[p10rack]
)

p200_multi = instruments.Pipette(
    axis="a",
    max_volume=200,
    trash_container=trash,
    tip_racks=[p200rack],
    channels=8
)

mag_deck = instruments.Magbead()

samples = [9, 10, 9, 10]  # already present in wells
bead_volumes = [s * (8 / 10) for s in samples]
num_samples = len(samples)
num_rows = int(num_samples / 8) + 1

# Step 1: transfer buffer to magbead plate
p10.distribute(
    bead_volumes,
    trough.wells('A1'),
    mag_plate.wells('A1', length=num_samples)
)

# Step 2: engage magnets and wait
mag_deck.delay(minutes=15).engage().delay(minutes=2)

# Step 3: (slowly) remove supernatent from plate
total_volumes = [samples[i] + bead_volumes[i] for i in range(num_samples)]
p10.consolidate(
    total_volumes,
    mag_plate.wells('A1', length=num_samples),
    trash,
    rate=0.5
)

# Step 4: wash each sample (twice) with ethanol
num_washes = 2
for n in range(num_washes):
    for i in range(num_rows):
        p200_multi.pick_up_tip()

        p200_multi.transfer(
            200,
            trough['A2'],
            mag_plate.rows(i),
            air_gap=100,
            new_tip='never')

        p200_multi.delay(seconds=30)

        p200_multi.transfer(
            200,
            mag_plate.rows(i).bottom(1),
            trash,
            air_gap=100,
            new_tip='never')

        p200_multi.drop_tip()

# Step 5: remove magnets
mag_deck.disengage()

# Step 6: add buffer to samples
p200_multi.distribute(
    20,
    trough['A3'],
    mag_plate.rows('1', length=num_rows),
    mix_after=(5, 20)
)

# Step 7: turn on magnets and wait
mag_deck.delay(minutes=5).engage().delay(minutes=5)

# Step 8: transfer final samples to separate plate
p200_multi.transfer(
    20,
    mag_plate.rows('1', length=num_rows),
    output_plate.rows('1', length=num_rows)
)

# Step 9: remove magnets
mag_deck.disengage()
ue)

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
