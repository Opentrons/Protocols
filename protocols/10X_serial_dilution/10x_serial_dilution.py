from opentrons import containers, instruments


trough = containers.load('trough-12row', 'D2', 'trough')
plate = containers.load('96-PCR-flat', 'C1', 'plate')

m200rack = containers.load('tiprack-200ul', 'A1', 'm200-rack')
trash = containers.load('trash-box', 'B2')

m200 = instruments.Pipette(
    name="m200",
    trash_container=trash,
    tip_racks=[m200rack],
    min_volume=20,
    max_volume=200,
    axis="a",
    channels=8
)


def run_custom_protocol(final_volume: float=200):
    transfer_volume = final_volume/10.0
    buffer_volume = final_volume - transfer_volume

    m200.distribute(buffer_volume, trough['A1'], plate.rows('2', to='7'))

    m200.pick_up_tip()

    m200.transfer(
        transfer_volume,
        plate.rows('1', to='6'),
        plate.rows('2', to='7'),
        mix_after=(3, final_volume/2),
        new_tip='never'
    )

    m200.transfer(transfer_volume, plate.rows('7'), trash[0], new_tip='never')

    m200.drop_tip()
