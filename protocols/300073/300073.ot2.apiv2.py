from opentrons import protocol_api

metadata = {
    'protocolName': 'Protocol Title',
    'author': 'AUTHOR NAME <authoremail@company.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.11'   # CHECK IF YOUR API LEVEL HERE IS UP TO DATE
                         # IN SECTION 5.2 OF THE APIV2 "VERSIONING"
}


def get_values(*names):
    import json
    _all_values = json.loads("""{ "n_samples_set1":48,
                                  "has_second_tube_set":true,
                                  "n_samples_set2":45,
                                  "aspiration_velocity":100,
                                  "dispension_velocity":100,
                                  "sample_aspiration_vol_ul":50,
                                  "aspiration_height_mm":3,
                                  "temp_mod_lname":null,
                                  "temperature":4
                                 }
                                  """)
    return [_all_values[n] for n in names]


def run(ctx: protocol_api.ProtocolContext):

    [
     n_samples_set1,
     has_second_tube_set,
     n_samples_set2,
     aspiration_velocity,
     dispension_velocity,
     sample_aspiration_vol_ul,
     aspiration_height_mm,
     temp_mod_lname,
     temperature
    ] = get_values(  # noqa: F821 (<--- DO NOT REMOVE!)
        "n_samples_set1",
        "has_second_tube_set",
        "n_samples_set2",
        "aspiration_velocity",
        "dispension_velocity",
        "sample_aspiration_vol_ul",
        "aspiration_height_mm",
        "temp_mod_lname",
        "temperature"
        )

    if not 1 <= n_samples_set1 <= 48:
        raise Exception(
            "Enter a number of samples for tube set 1 between 1-48")

    if (not 1 <= n_samples_set2 <= 45) and has_second_tube_set:
        raise Exception(
            "Enter a number of samples for tube set 2 between 1-45")

    if not 4 <= temperature <= 95:
        raise Exception(
            "Temperature module must be set to a temperature between " +
            "4 and 95 degrees Celsius")

    p20_lname = 'p20_single_gen2'
    p300_lname = 'p300_single_gen2'
    left_pipette_lname = (p20_lname if sample_aspiration_vol_ul < 20
                          else p300_lname)

    filtered_20_lname = "opentrons_96_filtertiprack_20ul"
    filtered_200_lname = "opentrons_96_filtertiprack_200ul"
    tiprack_lname = (filtered_20_lname if left_pipette_lname == p20_lname
                     else filtered_200_lname)

    tuberack_lname = "opentrons_6_tuberack_falcon_50ml_conical"
    well_plate_on_alum_lname = \
        "opentrons_96_aluminumblock_nest_wellplate_100ul"
    well_plate_lname = "nest_96_wellplate_100ul_pcr_full_skirt"
    # load modules

    '''

    Add your modules here with:

    module_name = ctx.load_module('{module_loadname}', '{slot number}')

    Note: if you are loading a thermocycler, you do not need to specify
    a slot number - thermocyclers will always occupy slots 7, 8, 10, and 11.

    For all other modules, you can load them on slots 1, 3, 4, 6, 7, 9, 10.

    '''
    temp_mod = None
    if temp_mod_lname:
        temp_mod = ctx.load_module("temperature module gen2", '3')

    # load labware

    '''

    Add your labware here with:

    labware_name = ctx.load_labware('{loadname}', '{slot number}')

    If loading labware on a module, you can load with:

    labware_name = module_name.load_labware('{loadname}')
    where module_name is defined above.

    '''
    tuberacks = [ctx.load_labware(tuberack_lname, slot)
                 for slot in ['1', '2',
                              '4', '5',
                              '7', '8',
                              '10', '11']]

    plate = None
    if temp_mod:
        plate = temp_mod.load_labware(well_plate_on_alum_lname,
                                      label="target plate")
    else:
        plate = ctx.load_labware(well_plate_lname, '3', label="target plate")

    # load tipracks

    '''

    Add your tipracks here as a list:

    For a single tip rack:

    tiprack_name = [ctx.load_labware('{loadname}', '{slot number}')]

    For multiple tip racks of the same type:

    tiprack_name = [ctx.load_labware('{loadname}', 'slot')
                     for slot in ['1', '2', '3']]

    If two different tipracks are on the deck, use convention:
    tiprack[number of microliters]
    e.g. tiprack10, tiprack20, tiprack200, tiprack300, tiprack1000

    '''
    tiprack = ctx.load_labware(tiprack_lname, '9')

    # load instrument

    '''
    Nomenclature for pipette:

    use 'p'  for single-channel, 'm' for multi-channel,
    followed by number of microliters.

    p20, p300, p1000 (single channel pipettes)
    m20, m300 (multi-channel pipettes)

    If loading pipette, load with:

    ctx.load_instrument(
                        '{pipette api load name}',
                        pipette_mount ("left", or "right"),
                        tip_racks=tiprack
                        )
    '''
    pipette = ctx.load_instrument(
                        left_pipette_lname,
                        "left",
                        tip_racks=[tiprack]
                        )

    # pipette functions   # INCLUDE ANY BINDING TO CLASS

    '''

    Define all pipette functions, and class extensions here.
    These may include but are not limited to:

    - Custom pickup functions
    - Custom drop tip functions
    - Custom Tip tracking functions
    - Custom Trash tracking functions
    - Slow tip withdrawal

    For any functions in your protocol, describe the function as well as
    describe the parameters which are to be passed in as a docstring below
    the function (see below).

    def pick_up(pipette):
        """`pick_up()` will pause the protocol when all tip boxes are out of
        tips, prompting the user to replace all tip racks. Once tipracks are
        reset, the protocol will start picking up tips from the first tip
        box as defined in the slot order when assigning the labware definition
        for that tip box. `pick_up()` will track tips for both pipettes if
        applicable.

        :param pipette: The pipette desired to pick up tip
        as definited earlier in the protocol (e.g. p300, m20).
        """
        try:
            pipette.pick_up_tip()
        except protocol_api.labware.OutOfTipsError:
            ctx.pause("Replace empty tip racks")
            pipette.reset_tipracks()
            pipette.pick_up_tip()

    '''

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

    # Map the target quadrants of the destination plate
    targ_cols = plate.columns()
    # Top left quadrant minus first 3 wells:
    # The rectangle of A1-D1 to A6-D6 minus well A1 to A3
    target_quadrant_1 = []
    target_quadrant_1.append(targ_cols[0][3:4])
    for col in targ_cols[1:6]:
        target_quadrant_1.append(col[0:4])

    # Top right quadrant: A7-D7 to A12-D12 rectangle
    target_quadrant_2 = []
    for col in targ_cols[6:12]:
        target_quadrant_2.append(col[0:4])

    # Bottom left quadrant: E1-H1 to E6-H6 rectangle
    target_quadrant_3 = []
    for col in targ_cols[0:6]:
        target_quadrant_3.append(col[4:8])

    # Bottom right quadrant: E7-H7 to E12-H12 rectangle
    target_quadrant_4 = []
    for col in targ_cols[6:12]:
        target_quadrant_4.append(col[4:8])

    target_well_map = []
    for quadrant in [target_quadrant_1, target_quadrant_2, target_quadrant_3,
                     target_quadrant_4]:
        for well in quadrant:
            target_well_map.append(well)

    general_tube_map = []
    for tuberack in tuberacks:
        general_tube_map.append(tuberack.wells())

    tube_map_set1 = general_tube_map[0:n_samples_set1]
    tube_maps_set2 = general_tube_map[0:n_samples_set2]
    # protocol

    '''

    Include header sections as follows for each "section" of your protocol.

    Section can be defined as a step in a bench protocol.

    e.g.

    ctx.comment('\n\nMOVING MASTERMIX TO SAMPLES IN COLUMNS 1-6\n')

    for .... in ...:
        ...
        ...

    ctx.comment('\n\nRUNNING THERMOCYCLER PROFILE\n')

    ...
    ...
    ...


    '''
    if temp_mod:
        ctx.comment("\n\nSetting temperature module to {} degrees C".
                    format(temperature))
        temp_mod.set_temperature(temperature)

    ctx.comment("\n\nTransferring samples from set 1 to destination plate")
    import pdb; pdb.set_trace()
    pipette.transfer(sample_aspiration_vol_ul, tube_map_set1,
                     target_well_map[0:n_samples_set1])
