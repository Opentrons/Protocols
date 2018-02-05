from opentrons import containers, instruments


trough = containers.load('trough-12row', 'B1', 'trough')
plate = containers.load('96-PCR-flat', 'C1', 'plate')

m200rack = containers.load('tiprack-200ul', 'A1', 'm200-rack')
trash = containers.load('fixed-trash', 'C4')

m200 = instruments.Pipette(
    name="m200",
    trash_container=trash,
    tip_racks=[m200rack],
    min_volume=20,
    max_volume=200,
    mount="left",
    channels=8
)


def run_custom_protocol(final_volume: float=200):
    transfer_volume = final_volume/10.0
    buffer_volume = final_volume - transfer_volume

    m200.distribute(buffer_volume, trough['A1'], plate.columns('2', to='7'))

    m200.pick_up_tip()

    m200.transfer(
        transfer_volume,
        plate.columns('1', to='6'),
        plate.columns('2', to='7'),
        mix_after=(3, final_volume/2),
        new_tip='never'
    )

    m200.transfer(transfer_volume, plate.columns('7'), trash[0], new_tip='never')

    m200.drop_tip()


run_custom_protocol(**{'final_volume': 200.0})
