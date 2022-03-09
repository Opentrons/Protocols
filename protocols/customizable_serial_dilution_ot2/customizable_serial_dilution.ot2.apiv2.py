def get_values(*names):
    import json
    _all_values = json.loads("""{"pipette_type":"p300_multi_gen2","dilution_factor":3,"num_of_dilutions":3,"total_mixing_volume":150,"tip_use_strategy":"never"}""")
    return [_all_values[n] for n in names]


metadata = {
    'protocolName': 'Customizable Serial Dilution',
    'author': 'Opentrons <protocols@opentrons.com>',
    'source': 'Protocol Library',
    'apiLevel': '2.2'
    }


def run(protocol_context):
    [pipette_type, dilution_factor, num_of_dilutions, total_mixing_volume,
        tip_use_strategy] = get_values(  # noqa: F821
            'pipette_type', 'dilution_factor', 'num_of_dilutions',
            'total_mixing_volume', 'tip_use_strategy'
        )

    # labware
    trough = protocol_context.load_labware(
        'nest_12_reservoir_15ml', '2')
    liquid_trash = trough.wells()[0]
    plate = protocol_context.load_labware(
        'corning_96_wellplate_360ul_flat', '3')
    tiprack = [
        protocol_context.load_labware('opentrons_96_tiprack_300ul', slot)
        for slot in ['1', '4','5']
    ]

    pip_name = pipette_type.split('_')[1]

    pipette = protocol_context.load_instrument(
        pipette_type, mount='right', tip_racks=tiprack)

    transfer_volume = total_mixing_volume/dilution_factor
    diluent_volume = total_mixing_volume - transfer_volume
if pip_name == 'multi':

        # Distribute diluent across the plate to the the number of samples
        # And add diluent to one column after the number of samples for a blank Test
        if tip_use_strategy == 'never':
            pipette.pick_up_tip()
        for i in range(num_of_dilutions):
            if tip_use_strategy == 'always':
                pipette.pick_up_tip()
            pipette.aspirate(diluent_volume,trough.wells()[0])
            pipette.dispense(diluent_volume,plate.wells()[8+i*8])
            if tip_use_strategy == 'always':
                pipette.drop_tip()

        # Dilution of samples across the 96-well flat bottom plate

        for s, d in zip(
                plate.rows()[0][:num_of_dilutions],
                plate.rows()[0][1:1+num_of_dilutions]
        ):
            if tip_use_strategy == 'always':
                pipette.pick_up_tip()

            #Transfer
            pipette.aspirate(transfer_volume,s)
            pipette.dispense(transfer_volume,d)

            #Mix 3x
            for mix in range(3):
                pipette.aspirate(total_mixing_volume/2,d)
                pipette.dispense(total_mixing_volume/2,d)

            if tip_use_strategy == 'always':
                if d != plate.rows()[0][num_of_dilutions]:
                    pipette.blow_out(d)
                    pipette.drop_tip()

                else:
                    # Remove transfer volume from the last column of the dilution
                    pipette.aspirate(transfer_volume,plate.rows()[0][num_of_dilutions])
                    pipette.dispense(transfer_volume,liquid_trash)
                    pipette.drop_tip()

        if tip_use_strategy == 'never':
            pipette.aspirate(transfer_volume,plate.rows()[0][num_of_dilutions])
            pipette.dispense(transfer_volume,liquid_trash)
            pipette.drop_tip()
else:
        # Distribute diluent across the plate to the the number of samples
        # And add diluent to one column after the number of samples for a blank
        x = 1
        if tip_use_strategy == 'never':
            pipette.pick_up_tip()
        for col in plate.columns()[1:1+num_of_dilutions]:
            c = len(col)
            for well in range(c):
                if tip_use_strategy == 'always':
                    pipette.pick_up_tip()
                pipette.aspirate(diluent_volume, trough.wells()[0])
                pipette.dispense(diluent_volume, plate.columns()[x][well])
                if tip_use_strategy == 'always':
                    pipette.drop_tip()
            x = x+1

        for row in plate.rows():
            for s, d in zip(row[:num_of_dilutions], row[1:1+num_of_dilutions]):

                if tip_use_strategy == 'always':
                    pipette.pick_up_tip()

                #Transfer
                pipette.aspirate(transfer_volume,s)
                pipette.dispense(transfer_volume,d)

                #Mix 3x
                for mix in range(3):
                    pipette.aspirate((total_mixing_volume*0.5),d)
                    pipette.dispense((total_mixing_volume*0.5),d)

                if tip_use_strategy == 'always':
                    if d != row[num_of_dilutions]:
                        pipette.blow_out(d)
                        pipette.drop_tip()
                    else:
                        pipette.aspirate(transfer_volume,row[num_of_dilutions])
                        pipette.dispense(transfer_volume,liquid_trash)
                        pipette.blow_out(liquid_trash)
                        pipette.drop_tip()

        if tip_use_strategy == 'never':
            pipette.drop_tip()
