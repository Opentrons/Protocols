from opentrons import containers, instruments

trough = containers.load('trough-12row', 'D1', 'trough')
plate = containers.load('96-deep-well', 'C1', 'plate')
tubes = containers.load('tube-rack-2ml', 'C2', 'tubes')

p300rack = containers.load('tiprack-200ul', 'E1', 'p300rack')
p200rack = containers.load('tiprack-200ul', 'A1', 'p200rack')
trash = containers.load('point', 'B2', 'trash')

p300_multi = instruments.Pipette(
    name="p300_multi",
    trash_container=trash,
    tip_racks=[p300rack],
    min_volume=50,
    max_volume=300,
    axis="a",
    channels=8
)

p200 = instruments.Pipette(
    name="p200",
    trash_container=trash,
    tip_racks=[p200rack],
    min_volume=20,
    max_volume=200,
    axis="b"
)


def run_protocol(sample_volume: float=20, buffer_volume: float=20):
    # Transfer buffer to all wells, except row 1 on plate.
    p300_multi.distribute(
        buffer_volume, trough['A1'], plate.rows('2', to='12'))

    # Transfer 8 tube samples to row 1 on plate, and mix.
    p200.transfer(
        sample_volume*2,
        tubes.wells('A1', to='D2'),
        plate.rows('1'),
        new_tip='always',
        mix_after=(3, sample_volume)  # How much volume to mix
    )

    # Dilution transfers with mixing of rows after each transfer.
    p300_multi.transfer(
        sample_volume,
        plate.rows('1', to='11'),
        plate.rows('2', to='12'),
        mix_after=(3, sample_volume)  # How much volume to mix
    )
