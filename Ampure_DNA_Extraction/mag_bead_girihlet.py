from opentrons import robot, containers, instruments


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

samples = [9, 10, 9, 10]
samples_mod = [(s * 8) / 10 for s in samples]
num_samples = len(samples)

# Step 1: transfer buffer to magbead plate
p10.distribute(
    samples_mod,
    trough.wells('A1'),
    mag_plate.wells('A1', length=num_samples)
)

# Step 2: engage magnets and wait
mag_deck.delay(900).engage().delay(120)

# Step 3: (slowly) remove supernatent from plate
volumes = [samples[i] + samples_mod[i] for i in range(num_samples)]
p10.consolidate(
    volumes,
    mag_plate.wells('A1', length=num_samples),
    trash,
    rate=0.5
)

# Step 4: wash each sample (twice) with ethanol
num_washes = 2
for n in range(num_washes):
    for i in range(num_samples):
        p200_multi.pick_up_tip()
        p200_multi.transfer(
            200, trough['A2'], mag_plate.rows[i], air_gap=100, new_tip='never')
        p200_multi.delay(30)
        p200_multi.transfer(
            200, mag_plate.rows[i], trash, air_gap=100, new_tip='never')
        p200_multi.drop_tip()

# Step 5: remove magnets
mag_deck.disengage()

# Step 6: add buffer to samples
p200_multi.distribute(
    20,
    trough['A3'],
    mag_plate.rows.get(length=num_samples),
    mix_before=(5, 20)
)

# Step 7: turn on magnets and wait
mag_deck.delay(300).engage().delay(300)

# Step 8: transfer final samples to separate plate
p200_multi.transfer(
    20,
    mag_plate.rows.get(length=num_samples),
    output_plate.rows.get(length=num_samples)
)

# Step 9: remove magnets
mag_deck.disengage()

for c in robot.commands():
    print(c)
