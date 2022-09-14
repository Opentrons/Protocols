from opentrons import protocol_api

metadata = {
    'protocolName': 'Day 2',
    'author': 'Opentrons <protocols@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.11'   # CHECK IF YOUR API LEVEL HERE IS UP TO DATE
                         # IN SECTION 5.2 OF THE APIV2 "VERSIONING"
}


def run(ctx: protocol_api.ProtocolContext):

    [
     _custom_variable1,
     p300_mount
    ] = get_values(  # noqa: F821 (<--- DO NOT REMOVE!)
        "_custom_variable1",
        "p300_mount")

    if not 1 <= _custom_variable1 <= 12:
        raise Exception("Enter a value between 1-12")

    # define all custom variables above here with descriptions:
    if p300_mount == 'left':
        p20_mount = 'right'
    else:
        p20_mount = 'left'
    # number of samples
    custom_variable1 = _custom_variable1

    # "True" for park tips, "False" for discard tips
    custom_variable2 = _custom_variable2

    # load modules

    temp_mod = ctx.load_module('temperature module gen2', '3')
    temp_mod.set_temperature(95)

    # load labware
    temp_plate = temp_mod.load_labware('nest_96_wellplate_2ml_deep')
    reagent_resv = ctx.load_labware('nest_12_reservoir_15ml', '1')
    std_plate = ctx.load_labware('opentrons_24_tuberack_generic_2ml_screwcap',
                                 '2')
    sample_plate = ctx.load_labware('opentrons_24_tuberack_generic_'
                                    '2ml_screwcap', '6')

    # load tipracks
    tiprack_300 = [ctx.load_labware('opentrons_96_tiprack_300ul', slot)
                   for slot in ['8', '11']]
    tiprack_20 = [ctx.load_labware('opentrons_96_tiprack_20ul', slot)
                  for slot in ['7', '10']]

    # load instrument
    p300 = load_instrument('p300_single_gen2', p300_mount,
                           tip_racks=tiprack_300)
    p20 = load_instrument('p20_single_gen2', p20_mount,
                          tip_racks=tiprack_20)

    # pipette functions   # INCLUDE ANY BINDING TO CLASS

    # helper functions
    '''
    Define any custom helper functions outside of the pipette scope here, using
    the convention seen above.

    e.g.

    def remove_supernatant(vol, index):
        """
        function description

        :param vol:

        :param index:
        """


    '''

    # reagents
    std_plate_well_list = [item for sublist in std_plate.rows()
                           for item in sublist]
    std_wells = std_plate_well_list[:21]
    reag_a = std_plate.rows()[3][3]
    reag_b = std_plate.rows()[3][4]
    reag_c = std_plate.rows()[3][5]
    sample_list = sample_plate.wells()[:4]+sample_plate.wells()[12:16]
    '''
    Define where all reagents are on the deck using the labware defined above.

    e.g.

    water = reservoir12.wells()[-1]
    waste = reservoir.wells()[0]
    samples = plate.rows()[0][0]
    dnase = tuberack.wells_by_name()['A4']

    '''

    # plate, tube rack maps

    '''
    Define any plate or tube maps here.

    e.g.

    plate_wells_by_row = [well for row in plate.rows() for well in row]

    '''

    # BEGIN PROTOCOL

    # Transfer X uL from starting vials slot 6 to slot 3 in triplicate

    # Transfer 36 uL DI from slot 1 well 1 to all 7 standards in triplicate

    # Wait 1 hour

    # Add 46 uL to samples

    # Reagent A, add 30 uL to all samples and standards

    # Turn off temp module

    # 1 hour wait

    # 49 uL Reagent B added to all samples/standards

    # 75 uL Reagent C added to all samples/standards
