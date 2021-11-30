metadata = {
    'protocolName': 'Customizable Serial Dilution',
    'author': 'Opentrons <protocols@opentrons.com>',
    'source': 'Protocol Library',
    'apiLevel': '2.2'
    }


def get_values(*names):
    import json
    _all_values = json.loads("""{ "pipette_type":"p300_single",
                                  "dilution_factor":"1.5",
                                  "num_of_dilutions":"11",
                                  "total_mixing_volume":"200",
                                  "tip_use_strategy":"never",
                                  "plate_type":"corning_96_wellplate_360ul_flat",
                                  "trough_type":"usascientific_12_reservoir_22ml",
                                  "tiprack_type":"opentrons_96_tiprack_300ul"}
                                  """)
    return [_all_values[n] for n in names]


def run(protocol_context):
    [pipette_type, dilution_factor, num_of_dilutions, total_mixing_volume,
        tip_use_strategy, plate_type, trough_type,
        tiprack_type] = get_values(  # noqa: F821
            'pipette_type', 'dilution_factor', 'num_of_dilutions',
            'total_mixing_volume', 'tip_use_strategy', 'plate_type',
            'trough_type', 'tiprack_type'
        )

    total_mixing_volume = float(total_mixing_volume)
    dilution_factor = float(dilution_factor)
    num_of_dilutions = int(num_of_dilutions)

    transfer_volume = total_mixing_volume/dilution_factor
    diluent_volume = total_mixing_volume - transfer_volume

    # labware
    trough = protocol_context.load_labware(
        trough_type, '2')
    # Todo: I thought this well was were we got diluent? Figure out meaning
    liquid_trash = trough.wells()[0]
    plate = protocol_context.load_labware(
        plate_type, '3')
    tiprack = [
        protocol_context.load_labware('opentrons_96_tiprack_300ul', slot)
        for slot in ['1', '4']
    ]
    # import pdb
    # pdb.set_trace()

    pipette = protocol_context.load_instrument(
        pipette_type, mount='left', tip_racks=tiprack)

    # Error checking
    pipette_vol_error_check(pipette, transfer_volume, "transfer")
    pipette_vol_error_check(pipette, diluent_volume, "diluent")

    if "multi" in pip_name:

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


def pipette_vol_error_check(pipette, volume, message):
    """
    This function checks if the volumes to be pipetted are compatible with
    the  volumes of the choosen pipette
    """
    if volume < pipette.min_volume:
        raise Exception(("The mounted pipette cannot pipette "
                         "a {} volume of {} uL because the volume "
                         "is too small for it.").format(message, volume)
                        )
    if volume > pipette.max_volume:
        raise Exception(("The mounted pipette cannot pipette "
                         "a {} volume of {} uL because the volume "
                         "is too large for it.").format(message, volume)
                        )
