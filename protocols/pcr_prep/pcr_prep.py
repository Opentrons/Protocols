from opentrons import protocol_api

metadata = {
    'protocolName': 'PCR Prep',
    'author': 'Opentrons <protocols@opentrons.com>',
    'source': 'Protocol Library',
    'apiLevel': '2.3'
}


def get_values(*names):
    import json
    _all_values = json.loads("""{ "left_pipette_step_1":"p20_single_gen2",
                                  "right_pipette_step_1":"p300_single_gen2",
                                  "left_pipette_tiprack_step_1":"opentrons_96_tiprack_20ul",
                                  "right_pipette_tiprack_step_1":"opentrons_96_tiprack_300ul",
                                  "left_pipette_step_2":"p20_single_gen2",
                                  "right_pipette_step_2":"p300_single_gen2",
                                  "left_pipette_tiprack_step_2":"opentrons_96_tiprack_20ul",
                                  "right_pipette_tiprack_step_2":"opentrons_96_tiprack_300ul",
                                  "temp_mod_reagents":"temperature module gen2",
                                  "temp_mod_reagents_aux":null,
                                  "temp_mod_target":"temperature module gen2",
                                  "reagent_labware":"opentrons_24_aluminumblock_nest_1.5ml_snapcap",
                                  "reagent_labware_aux":"opentrons_24_aluminumblock_nest_1.5ml_screwcap",
                                  "target_labware":"opentrons_96_aluminumblock_biorad_wellplate_200ul",
                                  "multi_pipette_distribution":"True",
                                  "temperature":4.0,
                                  "master_mix_csv":"Reagent,Slot,Well,Volume\\nBuffer,1,A2,30\\nMgCl2,1,A3,40\\ndNTPs,2,A2,90\\nWater,2,A3,248\\nprimer 1,1,A4,25\\nprimer 2,1,A5,25\\n"}""")
    return [_all_values[n] for n in names]


def run(ctx: protocol_api.ProtocolContext):

    [
        _left_pipette,
        _right_pipette,
        _right_pipette_tiprack,
        _left_pipette_tiprack,
        _temp_mod_reagents,
        _temp_mod_reagents_aux,
        _temp_mod_target,
        _reagent_labware,
        _reagent_labware_aux,
        _target_labware,
        _multi_pipette_distribution,
        _temperature,
        _master_mix_csv
    ] = get_values(  # noqa: F821
                   "left_pipette",
                   "right_pipette",
                   "right_pipette_tiprack",
                   "left_pipette_tiprack",
                   "temp_mod_reagents",
                   "temp_mod_reagents_aux",
                   "temp_mod_target",
                   "reagent_labware",
                   "reagent_labware_aux",
                   "target_labware",
                   "multi_pipette_distribution",
                   "temperature",
                   "master_mix_csv")

    # Do input error checking here
    if not _left_pipette and not _right_pipette:
        raise Exception('You have to select at least 1 pipette.')

    # define all custom variables above here with descriptions:

    # load modules

    '''

    Add your modules here with:

    module_name = ctx.load_module('{module_loadname}', '{slot number}')

    Note: if you are loading a thermocycler, you do not need to specify
    a slot number - thermocyclers will always occupy slots 7, 8, 10, and 11.

    For all other modules, you can load them on slots 1, 3, 4, 6, 7, 9, 10.

    '''

    # Loading temperature modules here
    temp_mod_list = [None, None, None]  # Reagent, reag. aux, and target T mod
    temp_mod_slots = ['7', '8', '9']
    temp_mod_type_list = [_temp_mod_reagents, _temp_mod_reagents_aux,
                          _temp_mod_target]
    for i, slot, type in zip([0, 1, 2],
                             temp_mod_slots,
                             temp_mod_type_list):
        if type is not None:
            temp_mod_list[i] = ctx.load_module(type, slot)
    '''

    Add your labware here with:

    labware_name = ctx.load_labware('{loadname}', '{slot number}')

    If loading labware on a module, you can load with:

    labware_name = module_name.load_labware('{loadname}')
    where module_name is defined above.

    '''
    # load labware
    labware_loadnames = [_reagent_labware, _reagent_labware_aux,
                         _target_labware]
    labware = [None, None, None]  # Reagent, Aux. reagent and target
    labware_labels = ["reagent labware", "auxilliary reagent labware",
                      "target labware"]
    lw_dict = {
        "reagents": 0,
        "aux_reagents": 1,
        "target": 2
    }

    # Load the reagent labware
    for i, label in zip(range(0, len(labware)), labware_labels):
        if temp_mod_list[i] is not None:
            labware[i] = \
                temp_mod_list[i].load_labware(labware_loadnames[i],
                                              labware_labels[i])
        else:
            labware[i] = ctx.load_labware(labware_loadnames[i],
                                          temp_mod_slots[i],
                                          labware_labels[i])

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

    left_tipracks = [ctx.load_labware(_left_pipette_tiprack, slot)
                     for slot in ['1']]

    right_tipracks = [ctx.load_labware(_right_pipette_tiprack, slot)
                      for slot in ['2']]

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

    left_pipette = None
    right_pipette = None

    for loadname, mount, tipracks in zip(
                                    [_left_pipette, _right_pipette],
                                    ["left", "right"],
                                    [left_tipracks, right_tipracks]):
        if mount == "left":
            left_pipette = ctx.load_instrument(loadname, mount,
                                               tip_racks=tipracks)
        else:
            right_pipette = ctx.load_instrument(loadname, mount,
                                                tip_racks=tipracks)

    pip_s = None
    pip_l = None

    # determine which pipette has the smaller volume range
    if left_pipette and right_pipette:
        # Case when pipettes are the same
        if left_pipette.name == right_pipette.name:
            pip_s = left_pipette
            pip_l = right_pipette
        else:
            if left_pipette.max_volume < right_pipette.max_volume:
                pip_s, pip_l = left_pipette, right_pipette
            else:
                pip_s, pip_l = right_pipette, left_pipette
    else:
        pipette = left_pipette if left_pipette else right_pipette

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

    master_mix_destination = None
    if _multi_pipette_distribution is True:
        ctx.comment("Distributing master mix")
        # Make sure that the target labware is appropriate for distribution
        # of mastermix, appropriate targets either have 8 or more wells
        # or they are reservoirs
        if len((labware[lw_dict["target"]].columns()[0]) <= 8
                and not labware[lw_dict["target"]].name in "reservoir"):
            raise Exception("Target labware does not have 8 wells per column")
        master_mix_destination = labware[lw_dict["target"]].columns()[0]
    else:
        # Mix in well A1 of the target
        master_mix_destination = labware[lw_dict["target"]].wells()[0]

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
    if temp_mod_list[0] is not None or temp_mod_list[1] is not None \
            or temp_mod_list[2] is not None:
        ctx.comment(
            "Setting temperature module temperatures and waiting for cooling")
        for mod in temp_mod_list:
            if mod is not None:
                mod.set_temperature(_temperature)
        ctx.comment("\nTemp modules have reached {} degrees C\n"
                    .format(_temperature))
        ctx.comment("\nWaiting for user to load reagents on labware\n")
        ctx.pause("Resume after the samples have been loaded")
        ctx.comment(
            "\nStarting PCR prep part 1 protocol - Mastermix assembly\n")

    info_list = [
        [cell.strip() for cell in line.split(',')]
        for line in _master_mix_csv.splitlines()[1:] if line
    ]

    for line in info_list:
        ctx.comment('Transferring ' + line[0] + ' to destination')
        # labware is 0 indexed, so we need to subtract 1 to get the right one
        source = labware[int(line[1])-1].wells(line[2].upper())
        if (_multi_pipette_distribution == "True" and not
                labware[lw_dict["target"]]):
            vol = float(line[3])/8
        else:
            vol = float(line[3])
        if left_pipette and right_pipette:
            if vol <= pip_s.max_volume:
                pipette = pip_s
            else:
                pipette = pip_l
        pipette.transfer(vol, source, master_mix_destination)
