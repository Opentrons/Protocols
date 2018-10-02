from opentrons import labware, instruments

trough = labware.load('trough-12row', '3', 'trough')
plate = labware.load('96-deep-well', '2', 'plate')
tubes = labware.load('tube-rack-2ml', '8', 'tubes')

multirack = labware.load('tiprack-200ul', '1', 'p300rack')
singlerack = labware.load('tiprack-200ul', '4', 'p300rack')


m300 = instruments.P300_Multi(
    mount="left",
    tip_racks=[multirack]
)

p300 = instruments.P300_Single(
    mount="right",
    tip_racks=[singlerack],
)


def run_custom_protocol(sample_volume: float=30, buffer_volume: float=30):
    if sample_volume < 30:
        raise ValueError("Pipette only aspirates 30ul and above")
    if buffer_volume < 30:
        raise ValueError("Pipette only aspirates 30ul and above")
    # Transfer buffer to all wells, except row 1 on plate.
    m300.distribute(
        buffer_volume, trough['A1'], plate.columns('2', to='12'))

    # Transfer 8 tube samples to row 1 on plate, and mix.
    p300.transfer(
        sample_volume*2,
        tubes.wells('A1', to='D2'),
        plate.columns('1'),
        new_tip='always',
        mix_after=(3, sample_volume)  # How much volume to mix
    )

    # Dilution transfers with mixing of rows after each transfer.
    m300.transfer(
        sample_volume,
        plate.columns('1', to='11'),
        plate.columns('2', to='12'),
        mix_after=(3, sample_volume)  # How much volume to mix
    )
