from opentrons import robot, containers, instruments
import math

p10rack = containers.load('tiprack-10ul', 'A1')
p200rack = containers.load('tiprack-200ul', 'A1')
output_plate = containers.load('96-PCR-flat', 'B1')
mag_plate = containers.load('96-PCR-tall', 'C1')
trough = containers.load('trough-12row', 'B1')
trash = containers.load('point', 'A2')

p10 = instruments.Pipette(
    axis="b",
    max_volume=10,
    trash_container=trash,
    tip_racks=[p10rack]
)

p200 = instruments.Pipette(
    axis="a",
    max_volume=200,
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
num_rows = math.ceil(num_samples / 8)


def distribute_volumes(source, targets, volumes, pipette):
    pipette.pick_up_tip()
    for i, well in enumerate(targets):
        if pipette.current_volume < volumes[i]:

            # find the amount to aspirate next based on future volumes
            aspirate_volume = volumes[i]
            n = i + 1
            while n >= len(volumes):
                if pipette.current_volume + volumes[n] > pipette.max_volume:
                    break
                aspirate_volume += volumes[n]
                n += 1

            pipette.aspirate(aspirate_volume).delay(1).touch_tip()
        pipette.dispense(volumes[i], well).touch_tip()
    pipette.blow_out().drop_tip()


# Add beads to samples based on DNA volume
mag_vols = [(s * 8) / 10 for s in samples]
distribute_volumes(mag_beads_stock, mag_plate[:len(samples)], mag_vols, p10)

# Incubate at room temp and engage mag beads

robot.home(enqueue=True)
mag_deck.delay(mag_incubation_time).engage().delay(mag_deck_delay)

# Remove supernatent from samples and deposit in trash

# pull up at a slower rate than usual in order to not disturbe magnets
# This would be easier with a set volume
# do they have any idea of how much supernatent they actually
# pick up per added mag bead volume?

for i in range(len(samples)):
    well = mag_plate[i].bottom(1)
    vol = (((samples[i]) * 8) / 10) + samples[i]
    p10.pick_up_tip()
    while vol > 0:
        aspirate_volume = min(p10.max_volume, vol)
        p10.aspirate(aspirate_volume, well, rate=0.5)
        p10.blow_out(trash)
        vol -= aspirate_volume
    p10.drop_tip()


for i in range(ethanol_washes):
    for i in range(num_rows):
        well = mag_plate.rows[i].top()
        p200.pick_up_tip()

        p200.aspirate(ethanol_volume / 2, ethanol_stock)
        p200.aspirate(ethanol_stock.top(2))
        p200.dispense(well)

        p200.aspirate(ethanol_volume / 2, ethanol_stock)
        p200.aspirate(ethanol_stock.top(2))
        p200.dispense(well)

        p200.delay(ethanol_delay)

        well = mag_plate[i].bottom(1)

        p200.aspirate(ethanol_volume / 2, well)
        p200.aspirate(mag_plate[i].top())
        p200.dispense(trash)

        p200.aspirate(ethanol_volume / 2, well)
        p200.aspirate(mag_plate[i].top())
        p200.drop_tip()

# Disengage magnets, resuspend samples, delay 5 min, engage magents 5 min

# release magnets
mag_deck.disengage()

# add resuspension buffer to all samples and mix
for i in range(num_rows):
    well = mag_plate.rows[i]
    p200.pick_up_tip().aspirate(buffer_volume, buffer_stock).dispense(well).mix(5, buffer_volume, well).drop_tip()
    
robot.home(enqueue=True)
p200.delay(buffer_delay)

mag_deck.engage()
p200.delay(mag_deck_buffer_delay)


# remove 20 uL from mag bead deck and send to 
for i in range(num_rows):
    well = mag_plate.rows[i]
    output = output_plate.rows[i]
    p200.pick_up_tip().aspirate(final_volume, well).dispense(output).drop_tip()
