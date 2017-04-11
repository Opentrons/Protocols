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

m200 = instruments.Pipette(
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
        m200.pick_up_tip()

        m200.transfer(
            200,
            trough['A2'],
            mag_plate.rows(i),
            air_gap=100,
            new_tip='never')

        m200.delay(seconds=30)

        m200.transfer(
            200,
            mag_plate.rows(i).bottom(1),
            trash,
            air_gap=100,
            new_tip='never')

        m200.drop_tip()

# Step 5: remove magnets
mag_deck.disengage()

# Step 6: add buffer to samples
m200.distribute(
    20,
    trough['A3'],
    mag_plate.rows('1', length=num_rows),
    mix_after=(5, 20)
)

# Step 7: turn on magnets and wait
mag_deck.delay(minutes=5).engage().delay(minutes=5)

# Step 8: transfer final samples to separate plate
m200.transfer(
    20,
    mag_plate.rows('1', length=num_rows),
    output_plate.rows('1', length=num_rows)
)

# Step 9: remove magnets
mag_deck.disengage()
