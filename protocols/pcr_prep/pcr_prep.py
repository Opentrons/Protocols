from opentrons import protocol_api
from math import ceil

metadata = {
    'protocolName': 'PCR Prep',
    'author': 'Opentrons <protocols@opentrons.com>',
    'source': 'Protocol Library',
    'apiLevel': '2.3'
}


def get_values(*names):
    import json
    _all_values = json.loads("""{ "create_mastermix":true,
                                  "use_same_pipettes":true,
                                  "number_of_samples":96,
                                  "left_pipette_part_1":"p20_single_gen2",
                                  "right_pipette_part_1":"p300_single_gen2",
                                  "left_pipette_tiprack_part_1":"opentrons_96_tiprack_20ul",
                                  "right_pipette_tiprack_part_1":"opentrons_96_tiprack_300ul",
                                  "left_pipette_part_2":"p20_single_gen2",
                                  "right_pipette_part_2":"p300_single_gen2",
                                  "left_pipette_tiprack_part_2":"opentrons_96_tiprack_20ul",
                                  "right_pipette_tiprack_part_2":"opentrons_96_tiprack_300ul",
                                  "temp_mod_slot_1":"temperature module gen2",
                                  "temp_mod_slot_4":,"temperature module gen2",
                                  "temp_mod_slot_7":"temperature module gen2",
                                  "pcr_reagent_labware":"opentrons_24_aluminumblock_nest_1.5ml_snapcap",
                                  "aux_pcr_reagent_labware":"opentrons_24_aluminumblock_nest_1.5ml_screwcap",
                                  "target_labware":"opentrons_96_aluminumblock_biorad_wellplate_200ul",
                                  "mastermix_labware":null,
                                  "mod_temperature":4.0,
                                  "master_mix_csv":"Reagent,Slot,Well,Volume\\nBuffer,1,A2,30\\nMgCl2,1,A3,40\\ndNTPs,2,A2,90\\nWater,2,A3,248\\nprimer 1,1,A4,25\\nprimer 2,1,A5,25\\n"}""")
    return [_all_values[n] for n in names]


def run(ctx: protocol_api.ProtocolContext):

    [
        _create_mastermix,
        _use_same_pipettes,
        _number_of_samples,
        _left_pipette_part_1,
        _right_pipette_part_1,
        _right_pipette_tiprack_part_1,
        _left_pipette_tiprack_part_1,
        _left_pipette_part_2,
        _right_pipette_part_2,
        _right_pipette_tiprack_part_2,
        _left_pipette_tiprack_part_2,
        _temp_mod_slot_1,
        _temp_mod_slot_4,
        _temp_mod_slot_7,
        _pcr_reagent_labware,
        _aux_pcr_reagent_labware,
        _target_labware,
        _mastermix_labware,
        _multi_pipette_distribution,
        _temperature,
        _master_mix_csv,
        _mastermix_volume,
        _DNA_volume
    ] = get_values(  # noqa: F821
                   "left_pipette_part_1",
                   "right_pipette_part_1",
                   "right_pipette_tiprack_part_1",
                   "left_pipette_tiprack_part_1",
                   "left_pipette_part_2",
                   "right_pipette_part_2",
                   "right_pipette_tiprack_part_2",
                   "left_pipette_tiprack_part_2",
                   "temp_mod_slot_1",
                   "temp_mod_slot_4",
                   "temp_mod_slot_7",
                   "reagent_labware",
                   "reagent_labware_aux",
                   "target_labware",
                   "multi_pipette_distribution",
                   "temperature",
                   "master_mix_csv")

    # Do input error checking here
    if (not _left_pipette_part_1 and not _right_pipette_part_1 and
            _create_mastermix):
        raise Exception('You have to select at least 1 pipette for part 1')

    if (not _left_pipette_part_2 and not _right_pipette_part_2
            and not _use_same_pipettes):
        raise Exception('You have to select at least 1 pipette for part 2')

    # Error check the CSV file
    # 1. Check that the total volume of mastermix that we create is enough
    # to pipette into each target well
    # Fields: Reagent | slot | well | volume

    mastermix_matrix = [
        [cell.strip() for cell in line.split(',')]
        for line in _master_mix_csv.splitlines()[1:] if line
    ]

    mastermix_volume_sum = 0
    for row in mastermix_matrix:
        mastermix_volume_sum = row[3]

    if mastermix_volume_sum < _DNA_volume * _number_of_samples:
        raise Exception("The mastermix that you are creating" +
                        "does not have sufficient volume for your DNA sampes")

    # Error check that there's auxiliary labware if the CSV is requesting it
    if _aux_pcr_reagent_labware is None:
        for row in mastermix_matrix:
            if row[1] == 2:
                raise Exception("The CSV mastermix file makes use of aux. " +
                                "labware, but none has been selected")
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
    # temp_mod_list = [None, None, None]
    """
    Slot 1: In part 1 this will hold the mastermix target container, or the
    DNA/mastermix plate (MDNAP)
    Slot 4: Part 1: PCR components, Part 2: DNA samples
    Slot 7: Part 1: Auxiliary PCR components, Part 2: Mastermix container
    """
    """temp_mod_slots = ['1', '4', '7']
    temp_mod_type_list = [_temp_mod_slot_1, _temp_mod_slot_4,
                          _temp_mod_slot_7]
    for i, slot, type in zip([0, 1, 2],
                             temp_mod_slots,
                             temp_mod_type_list):
        if type is not None:
            temp_mod_list[i] = ctx.load_module(type, slot)"""
    temp_mod_slot_1, temp_mod_slot_4, temp_mod_slot_7 = None, None, None

    if _temp_mod_slot_1 is not None:
        temp_mod_slot_1 = ctx.load_module(_temp_mod_slot_1)
    if _temp_mod_slot_4 is not None:
        temp_mod_slot_4 = ctx.load_module(_temp_mod_slot_4)
    if _temp_mod_slot_7 is not None:
        temp_mod_slot_7 = ctx.load_module(_temp_mod_slot_7)

    '''

    Add your labware here with:

    labware_name = ctx.load_labware('{loadname}', '{slot number}')

    If loading labware on a module, you can load with:

    labware_name = module_name.load_labware('{loadname}')
    where module_name is defined above.

    '''

    # Load labware for part 1

    pcr_reagent_labware, aux_pcr_reagent_labware, mastermix_labware = \
        None, None, None

    # Slot 1: This is either the mastermix container or the MDNAP
    mastermix_target_label = "Mastermix target"
    if _mastermix_labware is not None:
        if temp_mod_slot_1 is not None:
            mastermix_labware = \
                temp_mod_slot_1.load_labware(_mastermix_labware,
                                             mastermix_target_label)
        else:
            mastermix_labware = \
                ctx.load_labware(_mastermix_labware,
                                 '1',
                                 mastermix_target_label)
    else:
        target_labware_label = "target plate"
        if temp_mod_slot_1 is not None:
            target_labware = \
                temp_mod_slot_1.load_labware(_target_labware,
                                             target_labware_label)
        else:
            mastermix_labware = \
                ctx.load_labware(_mastermix_labware,
                                 '1',
                                 target_labware_label)


    # Slot 4: Primary PCR reagent component labware
    pcr_reagent_labware_label = "PCR reagents"
    if temp_mod_slot_4 is not None:
        pcr_reagent_labware = \
            temp_mod_slot_4.load_labware(_pcr_reagent_labware,
                                         pcr_reagent_labware_label)
    else:
        pcr_reagent_labware = \
            ctx.load_labware(_pcr_reagent_labware,
                             '4',
                             pcr_reagent_labware_label)

    # Slot 7: This labware is for auxiliary PCR reagents and is optional
    aux_pcr_reagent_labware_label = "Auxiliary PCR reagents"
    if _aux_pcr_reagent_labware is not None:
        if temp_mod_slot_7 is not None:
            aux_pcr_reagent_labware = \
                temp_mod_slot_7.load_labware(_aux_pcr_reagent_labware,
                                             aux_pcr_reagent_labware_label)
        else:
            aux_pcr_reagent_labware = \
                ctx.load_labware(_aux_pcr_reagent_labware,
                                 '7',
                                 aux_pcr_reagent_labware_label)

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

    left_tipracks = [ctx.load_labware(_left_pipette_tiprack_part_1, slot)
                     for slot in ['5', '6']]

    right_tipracks = [ctx.load_labware(_right_pipette_tiprack_part_1, slot)
                      for slot in ['2', '3']]

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
    left_pipette = ctx.load_instrument(_left_pipette_part_1, "left",
                                       left_tipracks)
    right_pipette = ctx.load_instrument(_right_pipette_part_1, "right",
                                        right_tipracks)

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

    '''
    Select the best pipette for pipetting step according to economic criteria
    '''
    def select_pipette(volume, source):
        # Trivial case: Both pipettes are the same
        if left_pipette.name == right_pipette.name:
            return left_pipette

        # First criteria: is there more than one pipette?
        if left_pipette is None:
            return right_pipette
        elif right_pipette is None:
            return left_pipette

        # Second criteria: If only one of the pipettes has a
        # min_volume < volume return that one
        if (left_pipette.min_volume <= volume
                and right_pipette.min_volume > volume):
            return left_pipette
        elif (right_pipette.min_volume <= volume
                and left_pipette.min_volume > volume):
            return right_pipette

        # Third criteria: If the source is a single well prefer a SCP if it
        # can do the transfer in 3 steps or less
        right_steps = 0
        left_steps = 0
        left_volume_multiplier = ceil(volume / left_pipette.max_volume)
        right_volume_multiplier = ceil(volume / right_pipette.max_volume)
        is_left_multi = "multi" in left_pipette.name
        is_right_multi = "multi" in right_pipette.name

        if len(source.wells()) == 1:
            if left_volume_multiplier <= 3 or right_volume_multiplier <= 3:
                if (not is_left_multi and
                        left_volume_multiplier <= right_volume_multiplier):
                    return left_pipette
                elif not is_right_multi:
                    return right_pipette

        # 4th criteria: Pick the pipette that makes the fewest trips
        for s_col in source.columns():
            s_len = len(s_col)
            col_left_steps = 1 if is_left_multi else s_len
            col_right_steps = 1 if is_right_multi else s_len
            left_steps = col_left_steps * left_volume_multiplier
            right_steps = col_right_steps * right_volume_multiplier

        if left_steps < right_steps:
            return left_pipette
        elif right_steps < left_steps:
            return right_pipette

        # 5th criteria: Return the pipette that uses the smallest tips
        # This stage would only be reached if the number of steps are the same
        if left_pipette.max_volume < right_pipette.max_volume:
            return left_pipette
        else:
            return right_pipette

    # reagents

    '''
    Define where all reagents are on the deck using the labware defined above.

    e.g.

    water = reservoir12.wells()[-1]
    waste = reservoir.wells()[0]
    samples = plate.rows()[0][0]
    dnase = tuberack.wells_by_name()['A4']

    '''

    mastermix_destination = None
    if mastermix_labware is not None:
        mastermix_destination = mastermix_labware.wells_by_name['A1']
    else:
        mastermix_destination = target_labware.columns[0]

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
    if create_mastermix:
        ctx.comment("Running part 1 of the procotol - creating mastermix")
        if temp_mod_slot_1 is not None:
            temp_mod_slot_1.set_temperature(_temperature)
        if temp_mod_slot_4 is not None:
            temp_mod_slot_4.set_temperature(_temperature)
        if temp_mod_slot_7 is not None:
            temp_mod_slot_7.set_temperature(_temperature)

        for line in info_list:
            ctx.comment('Transferring ' + line[0] + ' to destination')
            # labware is 0 indexed, so we need to subtract 1 to get the right one
            source = labware_part_1[int(line[1])-1].wells(line[2].upper())
            if (_multi_pipette_distribution == "True" and not
                    labware_part_1[lw_dict["target"]]):
                vol = float(line[3])/8
            else:
                vol = float(line[3])
            if left_pipette and right_pipette:
                if vol <= pip_s.max_volume:
                    pipette = pip_s
                else:
                    pipette = pip_l
            pipette.transfer(vol, source, master_mix_destination)
