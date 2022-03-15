metadata = {
    'protocolName': 'Customizable Serial Dilution',
    'author': 'Opentrons <protocols@opentrons.com>',
    'source': 'Protocol Library',
    'apiLevel': '2.11'
    }


def run(protocol_context):
    [pipette_type, tip_type, trough_type, plate_type,
     dilution_factor, num_of_dilutions, total_mixing_volume,
        tip_use_strategy, blank_on] = get_values(  # noqa: F821
            'pipette_type', 'tip_type', 'trough_type', 'plate_type',
            'dilution_factor', 'num_of_dilutions',
            'total_mixing_volume', 'tip_use_strategy', 'blank_on'
        )
    # Check for blank viability
    if num_of_dilutions == 11 and blank_on == 1:
        raise Exception(
                        'No room for blank with 11 dilutions'
        )

    # labware
    trough = protocol_context.load_labware(
        trough_type, '2')
    liquid_trash = trough.wells()[-1]
    plate = protocol_context.load_labware(
        plate_type, '3')
    if 'p20' in pipette_type:
        tip_name = 'opentrons_96_filtertiprack_20ul' if tip_type == 1\
            else 'opentrons_96_tiprack_20ul'
    else:
        tip_name = 'opentrons_96_filtertiprack_200ul' if tip_type == 1\
            else 'opentrons_96_tiprack_300ul'
    tiprack = [
        protocol_context.load_labware(tip_name, slot)
        for slot in ['1', '4', '5']
    ]
    pip_name = pipette_type.split('_')[1]

    pipette = protocol_context.load_instrument(
        pipette_type, mount='right', tip_racks=tiprack)

    transfer_volume = total_mixing_volume/dilution_factor
    diluent_volume = total_mixing_volume - transfer_volume

    # Protocol Body

    # multi-channel loop
    # Distribute diluent across the plate to the the number of samples
    # And add diluent to one column after the number of
    # samples for a blank Test
    if pip_name == 'multi':
        pipette.transfer(
                diluent_volume,
                trough.wells()[0],
                plate.rows()[0][1:num_of_dilutions],
                air_gap=10,
                new_tip=tip_use_strategy
            )

        # step 3, 4
        # Dilution of samples across the 96-well flat bottom plate
        if tip_use_strategy == 'never':
            pipette.pick_up_tip()
        for s, d in zip(
                plate.rows()[0][:num_of_dilutions/2],
                plate.rows()[0][1:num_of_dilutions]
        ):
            pipette.transfer(
                transfer_volume,
                s,
                d,
                air_gap=10,
                mix_after=(5, total_mixing_volume/2),
                new_tip=tip_use_strategy
            )
        if tip_use_strategy == 'never':
            pipette.drop_tip()

        if blank_on == 1:
            pipette.transfer(
                diluent_volume,
                trough.wells()[0],
                plate.rows()[0][-1],
                air_gap=10,
                new_tip=tip_use_strategy
                )
    # single-channel loop
    # Distribute diluent across the plate to the the number of samples
    # And add diluent to one column after the number of samples for a blank
    if pip_name == 'single':
        x = 1
        if tip_use_strategy == 'never':
            pipette.pick_up_tip()
        for col in plate.columns()[1:num_of_dilutions]:
            c = len(col)
            for well in range(c):
                pipette.transfer(
                    diluent_volume,
                    trough.wells()[0],
                    plate.columns()[x][well],
                    new_tip=tip_use_strategy
                )
            if tip_use_strategy == 'never':
                pipette.drop_tip()
            x = x+1
        for row in plate.rows():
            for s, d in zip(row[:num_of_dilutions], row[1:1+num_of_dilutions]):
                # Transfer
                pipette.aspirate(transfer_volume, s)
                pipette.dispense(transfer_volume, d)
                if tip_use_strategy == 'always':
                    pipette.drop_tip()

            # Mix 3x
            for mix in range(3):
                if tip_use_strategy == 'always':
                    pipette.pick_up_tip()
                    pipette.mix(1, total_mixing_volume/2, d)
                    pipette.drop_tip()
                else:
                    pipette.pick_up_tip()
                    pipette.mix(1, total_mixing_volume/2, d)

            if tip_use_strategy == 'always':
                if d != row[num_of_dilutions]:
                    pipette.blow_out(d)
                    pipette.drop_tip()
                else:
                    pipette.aspirate(transfer_volume,
                                     row[num_of_dilutions])
                    pipette.dispense(transfer_volume, liquid_trash)
                    pipette.blow_out(liquid_trash)
                    pipette.drop_tip()

            if tip_use_strategy == 'never':
                pipette.drop_tip()
