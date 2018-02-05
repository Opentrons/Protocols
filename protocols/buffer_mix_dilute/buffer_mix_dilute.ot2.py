from opentrons import containers, instruments

trough = containers.load('trough-12row', '3', 'trough')
plate = containers.load('96-deep-well', '2', 'plate')
tubes = containers.load('tube-rack-2ml', '8', 'tubes')

p300rack = containers.load('tiprack-200ul', '1', 'p300rack')
p200rack = containers.load('tiprack-200ul', '4', 'p200rack')
trash = containers.load('fixed-trash', '12', 'trash')

p300_multi = instruments.Pipette(
    name="p300_multi",
    trash_container=trash,
    tip_racks=[p300rack],
    min_volume=50,
    max_volume=300,
    mount="left",
    channels=8
)

p200 = instruments.Pipette(
    name="p200",
    trash_container=trash,
    tip_racks=[p200rack],
    min_volume=20,
    max_volume=200,
    mount="right"
)


def run_custom_protocol(sample_volume: float=20, buffer_volume: float=20):
    # Transfer buffer to all wells, except row 1 on plate.
    p300_multi.distribute(
        buffer_volume, trough['A1'], plate.columns('2', to='12'))

    # Transfer 8 tube samples to row 1 on plate, and mix.
    p200.transfer(
        sample_volume*2,
        tubes.wells('A1', to='D2'),
        plate.columns('1'),
        new_tip='always',
        mix_after=(3, sample_volume)  # How much volume to mix
    )

    # Dilution transfers with mixing of rows after each transfer.
    p300_multi.transfer(
        sample_volume,
        plate.columns('1', to='11'),
        plate.columns('2', to='12'),
        mix_after=(3, sample_volume)  # How much volume to mix
    )


run_custom_protocol(**{'sample_volume': 20.0, 'buffer_volume': 20.0})
