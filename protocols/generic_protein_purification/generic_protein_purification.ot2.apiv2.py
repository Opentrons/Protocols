from opentrons import protocol_api

metadata = {
    'protocolName': 'Generic protein purification protocol',
    'author': 'Opentrons <authoremail@company.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.11'   # CHECK IF YOUR API LEVEL HERE IS UP TO DATE
                         # IN SECTION 5.2 OF THE APIV2 "VERSIONING"
}


def get_values(*names):
    import json
    _all_values = \
        json.loads("""{ "mag_engage_time":"",
                        "n_samples":36,
                        "small_pipette_lname":"p20_multi_gen2",
                        "large_pipette_lname":"p300_multi_gen2",
                        "small_pipette_tipracks_lname":"opentrons_96_tiprack_20ul",
                        "large_pipette_tipracks_lname":"opentrons_96_tiprack_300ul",
                        "reservoir_lname": "nest_12_reservoir_15ml",
                        "destination_plate_lname":"",
                        "sample_plate_lname":"",
                        "mag_mod_lname":"",
                        "tube_rack_loadname":"",
                        "dest_temp_mod_lname":"temperature module gen2",
                        "resv_temp_mod_lname":"temperature module gen2",
                        "has_vortex_pause":True,
                        "do_SDS_step":False,
                        "do_DNAse_step":False,
                        "bead_volume":30.0,
                        "starting_volume":1000.0,
                        "wash_buf_vol":150.0,
                        "elution_buf_vol":100.0}
                        "use_NaCl":True}
                        """)
    return [_all_values[n] for n in names]


def run(ctx: protocol_api.ProtocolContext):

    [
     mag_engage_time,
     n_samples,
     small_pipette_lname,
     large_pipette_lname,
     small_pipette_tipracks_lname,
     large_pipette_tipracks_lname,
     reservoir_lname,
     destination_plate_lname,
     sample_plate_lname,
     mag_mod_lname,
     tube_rack_lname,
     dest_temp_mod_lname,
     resv_temp_mod_lname,
     has_vortex_pause,
     do_SDS_step,
     do_DNAse_step,
     bead_volume,
     starting_volume,
     wash_buf_vol
    ] = get_values(  # noqa: F821 (<--- DO NOT REMOVE!)
        "mag_engage_time",
        "n_samples",
        "small_pipette",
        "large_pipette",
        "small_pipette_tipracks",
        "large_pipette_tipracks",
        "reservoir_lname",
        "destination_plate_lname",
        "sample_plate_lname",
        "mag_mod_lname",
        "tube_rack_lname",
        "dest_temp_mod_lname",
        "resv_temp_mod_lname",
        "has_vortex_pause",
        "do_SDS_step",
        "do_DNAse_step",
        "bead_volume",
        "starting_volume",
        "wash_buf_vol",
        )

    # define all custom variables above here with descriptions:

    # Calculate reagent volumes
    # See docs for calculations
    # 10:1, v_lysis = v_s/9, e.g. for v_s = 1000 uL, v_lysis = 1000/9=111 uL
    lysis_buffer_vol = starting_volume/9
    dnaseI_vol = starting_volume/1000  # 1 uL per mL
    total_lysis_vol = starting_volume + lysis_buffer_vol + dnaseI_vol

    nacl_first_step_vol = total_lysis_vol/7
    nacl_wash_buf_vol = wash_buf_vol/7

    # Error checking

    # If DNAse I is being added from a tube we need to make sure that
    # a) we have a single pipette loaded and b) that dnaseI_vol > pipette min.
    # volume
    if (("single" not in small_pipette_lname or
         "single" not in large_pipette_lname) and do_DNAse_step):
        raise Exception("No single channel pipette for DNAse I distribution " +
                        "selected")
    # More error checking on this in the pipette loading section

    # load modules

    '''

    Add your modules here with:

    module_name = ctx.load_module('{module_loadname}', '{slot number}')

    Note: if you are loading a thermocycler, you do not need to specify
    a slot number - thermocyclers will always occupy slots 7, 8, 10, and 11.

    For all other modules, you can load them on slots 1, 3, 4, 6, 7, 9, 10.

    '''

    # import pdb; pdb.set_trace()
    # load labware

    # Load temperature modules (if any)
    t_mods = []
    for mod_lname, slot in zip([dest_temp_mod_lname, resv_temp_mod_lname],
                               ['4', '7']):
        if mod_lname != "None":
            t_mods.append(ctx.load_module(mod_lname, slot))
    dest_temp_mod, resv_temp_mod = t_mods[0], t_mods[1]

    # Load the magnetic module
    mag_mod = ctx.load_module(mag_mod_lname, '1')

    '''

    Add your labware here with:

    labware_name = ctx.load_labware('{loadname}', '{slot number}')

    If loading labware on a module, you can load with:

    labware_name = module_name.load_labware('{loadname}')
    where module_name is defined above.

    '''
    sample_plate = mag_mod.load_labware(sample_plate_lname)

    # Check that sample well is large enough for lysis reaction after NaCl addn
    sample_well = sample_plate.wells()[0]

    dest_plate = None
    if destination_temp_mod:
        dest_plate = dest_temp_mod.load_labware(destination_plate_lname)
    else:
        dest_plate = ctx.load_labware(destination_plate_lname, '4')

    reservoir = None
    if resv_temp_mod:
        reservoir = resv_temp_mod.load_labware(reservoir_lname)
    else:
        reservoir = ctx.load_labware(reservoir_lname, '7')

    dnaseI_tuberack = None
    if do_DNAse_step:
        DNAse_tuberack = ctx.load_labware(tube_rack_lname, '10')

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
    tipracks_large = [ctx.load_labware(large_pipette_tipracks_lname, slot)
                      for slot in ['8', '11']]
    tipracks_small = [ctx.load_labware(small_pipette_tipracks_lname, slot)
                      for slot in ['5', '6']]

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
    l_pip = ctx.load_instrument(
                        large_pipette_lname,
                        "left",
                        tip_racks=tipracks_large
                        )

    s_pip = ctx.load_instrument(
                        large_pipette_lname,
                        "right",
                        tip_racks=tipracks_small
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

    lysis_buffer = reservoir.wells_by_name()['A1']
    wash_buffer = reservoir.wells_by_name()['A2']
    elution_buffer = reservoir.wells_by_name()['A3']
    dnaseI = None
    if dnaseI_tuberack:
        dnaseI = dnaseI_tuberack.wells_by_name()['A1']
    sds_page_buf = None
    if do_SDS_step:
        sds_page_buf = reservoir.wells_by_name()['A4']

    # plate, tube rack maps

    '''
    Define any plate or tube maps here.

    e.g.

    plate_wells_by_row = [well for row in plate.rows() for well in row]

    '''

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
    ctx.comment('\n\nAdding lysis buffer to samples\n')
