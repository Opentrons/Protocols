from opentrons import containers, instruments
from api_helpers.api_helpers import transfer


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

p200_multi = instruments.Pipette(
    axis="a",
    max_volume=200,
    trash_container=trash,
    tip_racks=[p200rack],
    channels=8
)

mag_deck = instruments.Magbead()


def super_n_vol(vol):
    return (vol * 8) / 10


def transfer_with_air(source, target, volumes, pipette):
    if not isinstance(volumes, list):
        volumes = [volumes]
    for vol in volumes:
        p200_multi.aspirate(vol, source)
        p200_multi.aspirate(source.top(5))
        p200_multi.dispense(target)


# List of DNA volumes
samples = [9, 10, 9, 10]
num_samples = len(samples)

# transfer supernatent stock to the mag_plate
transfer(
    trough['A1'],
    mag_plate[:num_samples],
    [super_n_vol(s) for s in samples],
    p10
)

mag_deck.delay(900).engage().delay(120)

# transfer supernatent from mag_plate to the trash
transfer(
    mag_plate[:num_samples],
    trash,
    [super_n_vol(s) + s for s in samples],
    p10,
    rate=0.5
)

# wash with ethanol twice
num_washes = 2
divider = 2
volumes = [p200_multi.max_volume / divider] * divider

for n in range(num_washes):
    for i in range(num_samples):
        p200_multi.pick_up_tip()
        transfer_with_air(
            trough['A2'],
            mag_plate.rows[i],
            volumes,
            p200_multi
        )
        p200_multi.delay(30)
        transfer_with_air(
            mag_plate.rows[i],
            trash,
            volumes,
            p200_multi
        )
        p200_multi.drop_tip()

mag_deck.disengage()

# transfer buffer stock to each sample row
transfer(
    trough['A3'],
    mag_plate.rows[:num_samples],
    20,
    p200_multi,
    mix=(5, 20)
)

mag_deck.delay(300).engage().delay(300)

# transfer each sample row to the final plate
transfer(
    mag_plate.rows[:num_samples],
    output_plate.rows[:num_samples],
    20,
    p200_multi
)

mag_deck.disengage()
