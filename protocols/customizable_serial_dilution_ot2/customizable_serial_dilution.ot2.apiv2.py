metadata = {
    'protocolName': 'Customizable Serial Dilution',
    'author': 'Opentrons <protocols@opentrons.com>',
    'source': 'Protocol Library',
    'apiLevel': '2.11'
    }


def run(protocol_context):
    [pipette_type, mount_side, tip_type, trough_type, plate_type,
        dilution_factor, num_of_dilutions, total_mixing_volume,
        blank_on, tip_use_strategy, air_gap_volume] = get_values(  # noqa: F821
            'pipette_type', 'mount_side', 'tip_type', 'trough_type',
            'plate_type', 'dilution_factor', 'num_of_dilutions',
            'total_mixing_volume', 'blank_on',
            'tip_use_strategy', 'air_gap_volume'
        )
    # check for bad setup here
    if not 1 <= num_of_dilutions <= 11:
        raise Exception('Enter a number of dilutions between 1 and 11')

    if num_of_dilutions == 11 and blank_on == 1:
        raise Exception(
                        'No room for blank with 11 dilutions')

    # labware
    trough = protocol_context.load_labware(
        trough_type, '2')
    liquid_trash = trough.wells()[-1]
    plate = protocol_context.load_labware(
        plate_type, '3')
    if 'p20' in pipette_type:
        tip_name = 'opentrons_96_filtertiprack_20ul' if tip_type \
            else 'opentrons_96_tiprack_20ul'
    else:
        tip_name = 'opentrons_96_filtertiprack_200ul' if tip_type \
            else 'opentrons_96_tiprack_300ul'
    tiprack = [
        protocol_context.load_labware(tip_name, slot)
        for slot in ['1', '4', '5']
    ]

    pip_name = pipette_type.split('_')[1]

    pipette = protocol_context.load_instrument(
        pipette_type, mount=mount_side, tip_racks=tiprack)

    transfer_volume = total_mixing_volume/dilution_factor
    diluent_volume = total_mixing_volume - transfer_volume

    if pip_name == 'multi':

        # Distribute diluent across the plate to the the number of samples
        # And add diluent to one column after the number of samples for a blank
        pipette.transfer(
                diluent_volume,
                trough.wells()[0],
                plate.rows()[0][1:num_of_dilutions],
                air_gap=air_gap_volume,
                new_tip=tip_use_strategy
                )

        # Di lution of samples across the 96-well flat bottom plate

        if tip_use_strategy == 'never':
            pipette.pick_up_tip()
        for s, d in zip(
                    plate.rows()[0][:num_of_dilutions-1],
                    plate.rows()[0][1:num_of_dilutions]
        ):
            pipette.transfer(
                    transfer_volume,
                    s,
                    d,
                    air_gap=air_gap_volume,
                    mix_after=(5, total_mixing_volume/2),
                    new_tip=tip_use_strategy
                    )
        if tip_use_strategy == 'never':
            pipette.drop_tip()

        if blank_on == 1:
            pipette.transfer(
                    diluent_volume,
                    trough.wells()[0],
                    plate.rows()[0][num_of_dilutions+1],
                    air_gap=air_gap_volume,
                    new_tip=tip_use_strategy
                )
        # Single Pipette
    else:
        # Distribute diluent across the plate to the the number of samples
        # And add diluent to one column after the number of samples for a blank
        if tip_use_strategy == 'never':
            pipette.pick_up_tip()

        pipette.transfer(
                    diluent_volume,
                    trough.wells()[0],
                    plate.rows()[0:7][1:num_of_dilutions],
                    air_gap=air_gap_volume,
                    new_tip=tip_use_strategy
                    )

        # Transfer
        total_transfer_wells = (num_of_dilutions*8)
        for x in range(total_transfer_wells):
            pipette.transfer(
                        transfer_volume,
                        plate.wells()[x],
                        plate.wells()[x+8],
                        air_gap=air_gap_volume,
                        new_tip=tip_use_strategy,
                        mix_after=(3, total_mixing_volume/2)
                        )

        if blank_on == 1:
            for x in range(total_transfer_wells+8, total_transfer_wells+16):
                pipette.transfer(
                        diluent_volume,
                        trough.wells()[0],
                        plate.wells()[x],
                        air_gap=air_gap_volume,
                        new_tip=tip_use_strategy
                    )
