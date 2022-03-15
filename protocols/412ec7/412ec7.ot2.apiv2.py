metadata = {
    'protocolName': 'Protocol Title',
    'author': 'John C. Lynch',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.11'   # CHECK IF YOUR API LEVEL HERE IS UP TO DATE
    }


def run(ctx):

    [plate_type,
     temp_mod_on,
     dilution_factor,
     num_of_dilutions,
     total_mixing_volume,
     blank_on,
     tip_use_strategy
<<<<<<< HEAD
    ] = get_values(  # noqa: F821 (<--- DO NOT REMOVE!)
        "plate_type",
        "temp_mod_on",
        "dilution_factor",
        "num_of_dilutions",
        "total_mixing_volume",
        "blank_on",
        "tip_use_strategy")
=======
     ] = get_values(  # noqa: F821 (<--- DO NOT REMOVE!)
        'plate_type',
        'temp_mod_on',
        'dilution_factor',
        'num_of_dilutions',
        'total_mixing_volume',
        'blank_on',
        'tip_use_strategy')
>>>>>>> 748827f82161a55cd3a73515dccb89c79631d9b4

    # Check for bad setup here
    if not 1 <= num_of_dilutions <= 11:
        raise Exception('Enter a number of dilutions between 1 and 11')
    if temp_mod_on == 1 and 'aluminum' not in plate_type:
<<<<<<< HEAD
        raise Exception(
                        "Please select compatible plate/\
                        temperature module setting")
    if temp_mod_on == 0 and 'aluminum' in plate_type:
        raise Exception(
                        "Please select compatible plate/\
                        temperature module setting")
=======
        raise Exception('Please select compatible plate and\
    temperature module settiing')
    if temp_mod_on == 0 and 'aluminum' in plate_type:
        raise Exception(
                        'Please select compatible plate and\
    temperature module settiing')
>>>>>>> 748827f82161a55cd3a73515dccb89c79631d9b4
    if num_of_dilutions == 11 and blank_on == 1:
        raise Exception(
                        'No room for blank with 11 dilutions'
        )

    # define all custom variables above here with descriptions:
    transfer_volume = total_mixing_volume/dilution_factor
    diluent_volume = total_mixing_volume - transfer_volume

    # load modules
    if temp_mod_on == 1:
        temp_mod = ctx.load_module('tempdeck', '4')

    # load labware
    trough = ctx.load_labware('nest_12_reservoir_15ml', '1')
    if temp_mod_on == 1:
        dilute_plate = temp_mod.load_labware(plate_type)
    elif temp_mod_on == 0:
        dilute_plate = ctx.load_labware(plate_type, '4')

    # load tipracks
    tiprack = [
        ctx.load_labware('opentrons_96_tiprack_300ul', slot)
        for slot in ['2', '3', '5']
        ]
    # load instrument
    pipette = ctx.load_instrument(
        'p300_multi_gen2', mount='left', tip_racks=tiprack)
    # pipette functions   # INCLUDE ANY BINDING TO CLASS

    # helper functions

    # reagents
    liquid_trash = trough.wells()[-1]

    # protocol
    # step 2
    # Distribute diluent across the plate to the the number of samples
    pipette.transfer(
        diluent_volume,
        trough.wells()[0],
        dilute_plate.rows()[0][1:num_of_dilutions],
        air_gap=10,
        new_tip=tip_use_strategy
    )

    # step 3, 4
    # Dilution of samples across the 96-well flat bottom plate
    if tip_use_strategy == 'never':
        pipette.pick_up_tip()
    for s, d in zip(
            dilute_plate.rows()[0][:num_of_dilutions-1],
            dilute_plate.rows()[0][1:num_of_dilutions]
    ):
        pipette.transfer(
            transfer_volume,
            s,
            d,
            air_gap=10,
            mix_after=(5, total_mixing_volume-5),
            new_tip=tip_use_strategy
        )
    if tip_use_strategy == 'never':
        pipette.drop_tip()

    if blank_on == 1:
        pipette.transfer(
            diluent_volume,
            trough.wells()[0],
            dilute_plate.rows()[-1],
            air_gap=10,
            new_tip=tip_use_strategy
        )
