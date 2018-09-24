from opentrons import labware, instruments, robot

trough = labware.load('trough-12row', '5', 'trough')
plate = labware.load('96-PCR-flat', '3', 'plate')

m300rack = labware.load('tiprack-200ul', '1', 'm300-rack')
trash = robot.fixed_trash

m300 = instruments.P300_Multi(
    mount="left",
    tip_racks=[m300rack]
)


def run_custom_protocol(final_volume: float=200):
    transfer_volume = final_volume/10.0
    buffer_volume = final_volume - transfer_volume

    m300.distribute(buffer_volume, trough['A1'], plate.columns('2', to='7'))

    m300.pick_up_tip()

    m300.transfer(
        transfer_volume,
        plate.columns('1', to='6'),
        plate.columns('2', to='7'),
        mix_after=(3, final_volume/2),
        new_tip='never'
    )

    m300.transfer(
        transfer_volume,
        plate.columns('7'),
        trash[0],
        new_tip='never')

    m300.drop_tip()
