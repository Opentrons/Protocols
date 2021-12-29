metadata = {
    'protocolName': 'Customizable Serial Dilution',
    'author': 'Opentrons <protocols@opentrons.com>',
    'source': 'Protocol Library',
    'apiLevel': '2.5'
    }


def run(protocol_context):
    [pipette_type, tip_type, trough_type, plate_type,
     dilution_factor, num_of_dilutions, total_mixing_volume,
        tip_use_strategy] = get_values(  # noqa: F821
            'pipette_type', 'tip_type', 'trough_type', 'plate_type',
            'dilution_factor', 'num_of_dilutions',
            'total_mixing_volume', 'tip_use_strategy'
        )

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
        for slot in ['1', '4']
    ]

    pipette = protocol_context.load_instrument(
        pipette_type, mount='left', tip_racks=tiprack)

    transfer_volume = total_mixing_volume/dilution_factor
    diluent_volume = total_mixing_volume - transfer_volume

    if 'multi' in pipette_type:

        # Distribute diluent across the plate to the the number of samples
        # And add diluent to one column after the number of samples for a blank
        pipette.transfer(
            diluent_volume,
            trough.wells()[0],
            plate.rows()[0][1:1+num_of_dilutions]
        )

        # Dilution of samples across the 96-well flat bottom plate
        if tip_use_strategy == 'never':
            pipette.pick_up_tip()

        for s, d in zip(
                plate.rows()[0][:num_of_dilutions],
                plate.rows()[0][1:1+num_of_dilutions]
        ):
            pipette.transfer(
                transfer_volume,
                s,
                d,
                mix_after=(3, total_mixing_volume/2),
                new_tip=tip_use_strategy
            )

        # Remove transfer volume from the last column of the dilution
        pipette.transfer(
            transfer_volume,
            plate.rows()[0][num_of_dilutions],
            liquid_trash,
            new_tip=tip_use_strategy,
            blow_out=True
        )

        if tip_use_strategy == 'never':
            pipette.drop_tip()

    else:
        # Distribute diluent across the plate to the the number of samples
        # And add diluent to one column after the number of samples for a blank
        for col in plate.columns()[1:1+num_of_dilutions]:
            pipette.distribute(
                diluent_volume, trough.wells()[0], [well for well in col])

        for row in plate.rows():
            if tip_use_strategy == 'never':
                pipette.pick_up_tip()

            for s, d in zip(row[:num_of_dilutions], row[1:1+num_of_dilutions]):

                pipette.transfer(
                    transfer_volume,
                    s,
                    d,
                    mix_after=(3, total_mixing_volume/2),
                    new_tip=tip_use_strategy
                )

                pipette.transfer(
                    transfer_volume,
                    row[num_of_dilutions],
                    liquid_trash,
                    new_tip=tip_use_strategy,
                    blow_out=True
                )

            if tip_use_strategy == 'never':
                pipette.drop_tip()
