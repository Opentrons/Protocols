from opentrons import labware, instruments
from otcustomizers import StringSelection

trough = labware.load('trough-12row', 2, 'trough')

liquid_trash = trough.wells('A12')

plate = labware.load('96-flat', 3, 'plate')

tiprack = labware.load('tiprack-200ul', 1)


def run_custom_protocol(
    pipette_type: StringSelection(
        'p300-Single', 'p300-Multi', 'p50-Single', 'p50-Multi')='p300-Multi',
    # dilution_factor: float=1.5,
    # num_of_dilutions: int=10,
    # final_volume: float=200.0,
    tip_reuse_strategy: StringSelection(
        'reuse one tip', 'new tip each time')='reuse one tip'):

    dilution_factor = 1.5
    num_of_dilutions = 10
    final_volume = 200.0

    pip_name = pipette_type.split('-')
    print(pip_name[1])

    if pipette_type == 'p300-Single':
        pipette = instruments.P300_Single(
            mount='left',
            tip_racks=[tiprack])
    elif pipette_type == 'p50-Single':
        pipette = instruments.P50_Single(
            mount='left',
            tip_racks=[tiprack])
    elif pipette_type == 'p300-Multi':
        pipette = instruments.P300_Multi(
            mount='left',
            tip_racks=[tiprack])
    elif pipette_type == 'p50-Multi':
        pipette = instruments.P50_Multi(
            mount='left',
            tip_racks=[tiprack])

    new_tip = 'never' if tip_reuse_strategy == 'reuse one tip' else 'always'

    pipette.set_pick_up_current(0.6)  # what is this?

    transfer_volume = final_volume/dilution_factor
    buffer_volume = final_volume - transfer_volume

    # Distribute diluent across the plate to the the number of samples
    # And add diluent to one column after the number of samples for a blank
    pipette.distribute(buffer_volume, trough['A1'], plate.columns(
        '2', to=(num_of_dilutions+1)))

    # Dilution of samples across the 96-well flat bottom plate
    pipette.pick_up_tip(presses=3, increment=1)

    pipette.transfer(
        transfer_volume,
        plate.columns('1', to=(num_of_dilutions-1)),
        plate.columns('2', to=num_of_dilutions),
        mix_after=(3, final_volume/2),
        new_tip=new_tip
    )

    # Remove transfer volume from the last column of the dilution
    pipette.transfer(
        transfer_volume,
        plate.columns(num_of_dilutions),
        liquid_trash,
        new_tip=new_tip)

    pipette.drop_tip()
