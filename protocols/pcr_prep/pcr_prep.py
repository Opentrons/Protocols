from opentrons import protocol_api
from math import ceil
from math import floor

metadata = {
    'protocolName': 'PCR Prep',
    'author': 'Opentrons <protocols@opentrons.com>',
    'source': 'Protocol Library',
    'apiLevel': '2.7'
}


def get_values(*names):
    import json
    _all_values = json.loads("""{ "create_mastermix":true,
                                  "use_same_pipettes":false,
                                  "number_of_samples":77,
                                  "left_pipette_part_1":"p300_single_gen2",
                                  "right_pipette_part_1":"p20_multi_gen2",
                                  "left_pipette_tiprack_part_1":"opentrons_96_tiprack_300ul",
                                  "right_pipette_tiprack_part_1":"opentrons_96_tiprack_20ul",
                                  "left_pipette_part_2":"p20_single_gen2",
                                  "right_pipette_part_2":"p300_single_gen2",
                                  "left_pipette_tiprack_part_2":"opentrons_96_tiprack_20ul",
                                  "right_pipette_tiprack_part_2":"opentrons_96_tiprack_300ul",
                                  "temp_mod_slot_4":"temperature module gen2",
                                  "temp_mod_slot_7":"temperature module gen2",
                                  "temp_mod_slot_10":"temperature module gen2",
                                  "pcr_reagent_labware":"opentrons_24_aluminumblock_nest_1.5ml_snapcap",
                                  "aux_pcr_reagent_labware":"opentrons_24_aluminumblock_nest_1.5ml_screwcap",
                                  "target_labware":"opentrons_96_aluminumblock_biorad_wellplate_200ul",
                                  "mastermix_labware":"nest_12_reservoir_15ml",
                                  "DNA_sample_plate":"opentrons_96_aluminumblock_biorad_wellplate_200ul",
                                  "mod_temperature":4.0,
                                  "DNA_volume":18.0,
                                  "mastermix_volume":2.0,
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
        _temp_mod_slot_4,
        _temp_mod_slot_7,
        _temp_mod_slot_10,
        _pcr_reagent_labware,
        _aux_pcr_reagent_labware,
        _target_labware,
        _mastermix_labware,
        _DNA_sample_plate,
        _temperature,
        _master_mix_csv,
        _mastermix_volume,
        _DNA_volume
    ] = get_values(  # noqa: F821
                   "create_mastermix",
                   "use_same_pipettes",
                   "number_of_samples",
                   "left_pipette_part_1",
                   "right_pipette_part_1",
                   "right_pipette_tiprack_part_1",
                   "left_pipette_tiprack_part_1",
                   "left_pipette_part_2",
                   "right_pipette_part_2",
                   "right_pipette_tiprack_part_2",
                   "left_pipette_tiprack_part_2",
                   "temp_mod_slot_4",
                   "temp_mod_slot_7",
                   "temp_mod_slot_10",
                   "pcr_reagent_labware",
                   "aux_pcr_reagent_labware",
                   "target_labware",
                   "mastermix_labware",
                   "DNA_sample_plate",
                   "mod_temperature",
                   "master_mix_csv",
                   "mastermix_volume",
                   "DNA_volume"
                   )

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
        mastermix_volume_sum += int(row[3])

    if mastermix_volume_sum < _mastermix_volume * _number_of_samples:
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
    temp_mod_slot_4, temp_mod_slot_7, temp_mod_slot_10 = None, None, None

    def load_temp_mods():
        nonlocal temp_mod_slot_4, temp_mod_slot_7, temp_mod_slot_10
        if _temp_mod_slot_4 is not None:
            temp_mod_slot_4 = ctx.load_module(_temp_mod_slot_4, '4')
        if _temp_mod_slot_7 is not None:
            temp_mod_slot_7 = ctx.load_module(_temp_mod_slot_7, '7')
        if _temp_mod_slot_10 is not None:
            temp_mod_slot_10 = ctx.load_module(_temp_mod_slot_10, '10')
    load_temp_mods()

    # Dictionary defines what labware goes on what module
    temp_mod_dict = \
        {"mastermix": temp_mod_slot_4,
         "pcr_reagent_labware_step_1": temp_mod_slot_7,
         "aux_pcr_reagent_labware_step_1": temp_mod_slot_10,
         "DNA_sample_plate_step_2": temp_mod_slot_7,
         "target_plate_step_2": temp_mod_slot_10
         }
    # Dictionary that matches labware with deck slots, must match with
    # temp_mod_dict's entries
    lw_slot_dict = \
        {"mastermix": 4,
         "pcr_reagent_labware_step_1": 7,
         "aux_pcr_reagent_labware_step_1": 10,
         "DNA_sample_plate_step_2": 7,
         "target_plate_step_2": 10
         }

    '''

    Add your labware here with:

    labware_name = ctx.load_labware('{loadname}', '{slot number}')

    If loading labware on a module, you can load with:

    labware_name = module_name.load_labware('{loadname}')
    where module_name is defined above.

    '''

    # Load labware for part 1
    if _create_mastermix:
        pcr_reagent_labware, aux_pcr_reagent_labware, mastermix_labware = \
            None, None, None

        # Slot 4: This is either the mastermix container or the MDNAP
        mastermix_target_label = "Mastermix target"
        if temp_mod_slot_4 is not None:
            mastermix_labware = \
                temp_mod_slot_4.load_labware(_mastermix_labware,
                                             mastermix_target_label)
        else:
            mastermix_labware = \
                ctx.load_labware(_mastermix_labware,
                                 '4',
                                 mastermix_target_label)

        # Slot 7: Primary PCR reagent component labware
        pcr_reagent_labware_label = "PCR reagents"
        if temp_mod_slot_7 is not None:
            pcr_reagent_labware = \
                temp_mod_slot_7.load_labware(_pcr_reagent_labware,
                                             pcr_reagent_labware_label)
        else:
            pcr_reagent_labware = \
                ctx.load_labware(_pcr_reagent_labware,
                                 '7',
                                 pcr_reagent_labware_label)

        # Slot 10: This labware is for auxiliary PCR reagents and is optional
        aux_pcr_reagent_labware_label = "Auxiliary PCR reagents"
        if _aux_pcr_reagent_labware is not None:
            if temp_mod_slot_10 is not None:
                aux_pcr_reagent_labware = \
                    temp_mod_slot_10.load_labware(_aux_pcr_reagent_labware,
                                                  aux_pcr_reagent_labware_label
                                                  )
            else:
                aux_pcr_reagent_labware = \
                    ctx.load_labware(_aux_pcr_reagent_labware,
                                     '10',
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
                     for slot in ['8', '9']]

    right_tipracks = [ctx.load_labware(_right_pipette_tiprack_part_1, slot)
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
    def get_tiprack_well_with_n_tips(pipette, n):
        for rack in pipette.tip_racks:
            # Iterate from bottom of the column and try to find n tips to
            # pick up with the 8CP
            for col in rack.columns():
                sum_tips = 0
                for well in reversed(col):
                    if well.has_tip:
                        sum_tips += 1
                        if sum_tips == n:
                            return rack, well
        # If there are no column with n tips raise error
        raise protocol_api.labware.OutOfTipsError(
                "Can't find a tiprack with {} tips for {}"
                .format(n, pipette.name))

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
    def is_single(pipette):
        return "single" in pipette.name

    def drop_all_tips(pipettes: list):
        for pip in pipettes:
            if pip.has_tip:
                pip.drop_tip()

    '''
    Select the best pipette for pipetting step according to economic criteria
    The source is either a column of wells or a singular well
    volume: The volume in uL
    source: A list of wells (1 or more) to aspirate from
    source_labware: The labware that the source belongs to
    '''
    def select_pipette(volume, source: list, source_labware):
        if not isinstance(source, list):
            raise TypeError("source should be a list")

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

        right_steps = 0
        left_steps = 0
        left_volume_multiplier = ceil(volume / left_pipette.max_volume)
        right_volume_multiplier = ceil(volume / right_pipette.max_volume)
        is_left_multi = "multi" in left_pipette.name
        is_right_multi = "multi" in right_pipette.name

        # Third criteria: If the source is a single well prefer a SCP if it
        # can do the transfer in 3 steps or less (reservoirs appear as single)
        # wells, but are 8-channel reservoirs. If both pipettes are SCP
        # pick the one that will make the fewest trips
        # If the source is a reservoir a single well represents 8 pseudo-wells
        # import pdb; pdb.set_trace()
        if (len(source) == 1
                and "reservoir" not in source_labware.load_name):
            # Check if both pipettes are SCP. If they are we just pick
            # the pipette that can do the operation in the fewest steps
            if not is_left_multi and not is_right_multi:
                if left_volume_multiplier <= right_volume_multiplier:
                    return left_pipette
                else:
                    return right_pipette

        # 4th criteria: Pick the pipette that makes the fewest trips
        s_len = 0
        s_len = len(source)
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

    """
    Classifies labware that contains mastermix as single well
    or 8-well
    """
    def classify_mastermix_labware(mastermix_labware):
        name = mastermix_labware.name
        if "reservoir" in name:
            return "multi_well_unified"
        if "wellplate" in name:
            return "multi_well_distributed"
        return "single_well"

    # reagents

    '''
    Define where all reagents are on the deck using the labware defined above.

    e.g.

    water = reservoir12.wells()[-1]
    waste = reservoir.wells()[0]
    samples = plate.rows()[0][0]
    dnase = tuberack.wells_by_name()['A4']

    '''

    mastermix_destination = [mastermix_labware.wells_by_name()['A1']]
    '''if mastermix_labware is not None:
        mastermix_destination = [mastermix_labware.wells_by_name()['A1']]
    elif _number_of_samples < 8:
        mastermix_destination = target_labware.columns()[0:_number_of_samples]
    else:
        mastermix_destination = target_labware.columns()[0]'''

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
    if _create_mastermix:
        ctx.comment("Running part 1 of the procotol - creating mastermix")
        if temp_mod_slot_4 is not None:
            temp_mod_slot_4.set_temperature(_temperature)
        if temp_mod_slot_7 is not None:
            temp_mod_slot_7.set_temperature(_temperature)
        if temp_mod_slot_10 is not None:
            temp_mod_slot_10.set_temperature(_temperature)

        for line in mastermix_matrix:
            ctx.comment("Transferring {}".format(line[0]))
            source = None
            pipette = None
            volume = float(line[3])
            if int(line[1]) == 1:
                source = pcr_reagent_labware.wells_by_name()[line[2]]
                pipette = select_pipette(volume, [source],
                                         pcr_reagent_labware)
            elif int(line[1]) == 2:
                source = aux_pcr_reagent_labware.wells_by_name()[line[2]]
                pipette = select_pipette(volume, [source],
                                         aux_pcr_reagent_labware)
            # Use a SCP to pipette mastermix component to a single well
            # reservoir
            if is_single(pipette):
                try:
                    pipette.transfer(volume,
                                     source,
                                     mastermix_destination)
                except protocol_api.labware.OutOfTipsError:
                    ctx.pause("Replace empty tip racks for {}"
                              .format(pipette.name))
                    pipette.reset_tipracks()
            # The selected pipette is an 8CP, pick up a single tip and
            # transfer mastermix component
            else:
                try:
                    rack, rack_well = get_tiprack_well_with_n_tips(pipette, 1)
                    pipette.pick_up_tip(rack_well)
                except protocol_api.labware.OutOfTipsError:
                    ctx.pause("Replace empty tip racks for {}".
                              format(pipette.name))
                    pipette.reset_tipracks()
                for well in mastermix_destination:
                    pipette.aspirate(volume, source)
                    pipette.dispense(volume, well)
                pipette.drop_tip()
        # After the mastermix has all components added it's time to mix
        mix_volume = mastermix_volume_sum / (2*len(mastermix_destination))
        pipette = select_pipette(mix_volume, mastermix_destination,
                                 mastermix_labware)
        if is_single(pipette):
            if pipette.has_tip:
                pipette.drop_tips()
            pipette.pick_up_tip()
            for well in mastermix_destination:
                if mix_volume > pipette.max_volume:
                    pipette.mix(5, pipette.max_volume, well)
                    pipette.blow_out(well)
                else:
                    pipette.mix(5, mix_volume, well)
                    pipette.blow_out(well)
        else:
            if pipette.has_tip:
                pipette.drop_tip()
            rack, rack_well = \
                get_tiprack_well_with_n_tips(pipette,
                                             len(mastermix_destination))
            pipette.pick_up_tip(rack_well)
            if mix_volume > pipette.max_volume:
                if isinstance(mastermix_destination, list):
                    pipette.mix(5, pipette.max_volume,
                                mastermix_destination[0])
                    pipette.blow_out(mastermix_destination[0])
                else:
                    pipette.mix(5, pipette.max_volume, mastermix_destination)
                    pipette.blow_out(mastermix_destination)
            else:
                if isinstance(mastermix_destination, list):
                    pipette.mix(5, mix_volume,
                                mastermix_destination[0])
                    pipette.blow_out(mastermix_destination[0])
                else:
                    pipette.mix(5, mix_volume, mastermix_destination)
                    pipette.blow_out(mastermix_destination)
        ctx.comment("\nFinished mixing mastermix\n")

    ctx.comment("Please insert the DNA sample plate in slot {} ({})"
                .format(lw_slot_dict["DNA_sample_plate_step_2"],
                        _target_labware))
    ctx.comment("and the target plate in slot {} ({})"
                .format(lw_slot_dict["target_plate_step_2"],
                        _DNA_sample_plate))
    if not _use_same_pipettes:
        ctx.comment("Change the pipettes for step 2, left: {}, right: {}"
                    .format(_left_pipette_part_2, _right_pipette_part_2))
    ctx.pause()

    if _create_mastermix:
        del ctx.deck[4]
        del ctx.deck[7]
        del ctx.deck[10]
        temp_mod_slot_4, temp_mod_slot_7, temp_mod_slot_10 = None, None, None
        load_temp_mods()

    # We have to repopulate the dictionary since Python assigns by value.
    temp_mod_dict = \
        {"mastermix": temp_mod_slot_4,
         "pcr_reagent_labware_step_1": temp_mod_slot_7,
         "aux_pcr_reagent_labware_step_1": temp_mod_slot_10,
         "DNA_sample_plate_step_2": temp_mod_slot_7,
         "target_plate_step_2": temp_mod_slot_10
         }

    mastermix_label = "Mastermix container"
    dna_label = "DNA sample plate"
    target_label = "DNA/Mastermix target plate"

    dna_sample_plate = None
    mastermix_labware = None
    dna_mastermix_target_plate = None

    # Load mastermix container
    if temp_mod_dict["mastermix"] is not None:
        mastermix_labware = \
            temp_mod_dict["mastermix"].load_labware(_mastermix_labware)
    else:
        mastermix_labware = \
            ctx.load_labware(_mastermix_labware, lw_slot_dict["mastermix"],
                             mastermix_label)
    # Load DNA sample plate
    if temp_mod_dict["DNA_sample_plate_step_2"] is not None:
        dna_sample_plate = \
            (temp_mod_dict["DNA_sample_plate_step_2"].
                load_labware(_DNA_sample_plate, dna_label))
    else:
        dna_sample_plate = \
            ctx.load_labware(_DNA_sample_plate,
                             lw_slot_dict["DNA_sample_plate_step_2"],
                             dna_label)

    # Load the target plate
    if temp_mod_dict["target_plate_step_2"] is not None:
        dna_mastermix_target_plate = \
            temp_mod_dict["target_plate_step_2"].load_labware(_target_labware,
                                                              target_label)
    else:
        dna_mastermix_target_plate = \
            ctx.load_labware(_DNA_sample_plate,
                             lw_slot_dict["target_plate_step_2"],
                             target_label)

    # Distribute mastermix
    ctx.comment("\nDistributing mastermix into column 1 of the target plate\n")
    mastermix_source = mastermix_labware.columns()[0]

    n_target_columns = floor(_number_of_samples / 8)
    remainder = _number_of_samples % 8

    # Pipette mastermix into the first column of the target,
    # then distribute through the rows

    # Drop any tips
    drop_all_tips([left_pipette, right_pipette])

    def SCP_distribute_mastermix(pipette, source_well, dest_plate):
        nonlocal n_target_columns, remainder
        col_1 = dest_plate.columns()[0]
        for i, well in zip(range(1, len(col_1)+1), col_1):
            volume = 0
            pipette = None
            if i <= remainder:
                volume = (n_target_columns+1)*_mastermix_volume
            else:
                volume = n_target_columns*_mastermix_volume

            if volume > 0:
                pipette.transfer(volume,
                                 mastermix_source,
                                 well)

    min_pipetting_volume = n_target_columns*_mastermix_volume
    eight_sample_columns_volume = min_pipetting_volume
    pipette = select_pipette(min_pipetting_volume,
                             mastermix_source,
                             mastermix_labware)
    if classify_mastermix_labware(mastermix_labware) == "single_well":
        if is_single(pipette):
            SCP_distribute_mastermix(pipette,
                                     mastermix_source,
                                     dna_mastermix_target_plate)
        else:
            _, tiprack_well = get_tiprack_well_with_n_tips(pipette, 1)
            pipette.pick_up_tip(tiprack_well)
            pipette.aspirate(volume, mastermix_source)
            pipette.dispense(volume, well)
    # 8-channel to 8-channel well distribution, but no barriers between
    # the source wells (i.e. "reservoirs")
    # so we can aspirate from the same "well".
    elif classify_mastermix_labware(mastermix_labware) == "multi_well_unified":
        if is_single(pipette):
            SCP_distribute_mastermix(pipette,
                                     mastermix_source,
                                     dna_mastermix_target_plate)
        else:
            dest_col_1 = dna_mastermix_target_plate.columns()[0]
            if n_target_columns > 0:
                pipette.transfer(eight_sample_columns_volume,
                                 mastermix_source,
                                 dest_col_1[0])
            if remainder > 0:
                pipette = select_pipette(_mastermix_volume, mastermix_source,
                                         mastermix_labware)
                if is_single(pipette):
                    for well in dest_col_1[:remainder]:
                        pipette.transfer(_mastermix_volume,
                                         mastermix_source,
                                         well)
                else:
                    _, rack_well = get_tiprack_well_with_n_tips(pipette,
                                                                remainder)
                    pipette.pick_up_tip(rack_well)
                    pipette.aspirate(_mastermix_volume, mastermix_source[0])
                    pipette.dispense(_mastermix_volume, dest_col_1[0])
    # Case when mastermix is distributed in the first 8-well column,
    # and the wells have to be aspirated with an 8CP or individually with
    # an SCP. An example is when mastermix is distributed into the first col.
    # of a 96-well plate
    elif (classify_mastermix_labware(mastermix_labware)
            == "multi_well_distributed"):
        dest_col_1 = dna_mastermix_target_plate.columns()[0]
        if is_single(pipette):
            i_range = range(1, len(mastermix_source)+1)
            for i, s_well, d_well in zip(i_range,
                                         mastermix_source, dest_col_1):
                volume = 0
                if i <= remainder:
                    volume = eight_sample_columns_volume + _mastermix_volume
                else:
                    volume = eight_sample_columns_volume

                if volume > 0:
                    pipette.transfer(volume, s_well, d_well)
        # Split the transfer into two steps; step one: transfer
        # eight_sample_columns_volume + _mastermix_volume to rows
        # which have n+1 wells due to the remainder.
        # then transfer eight_sample_columns_volume to the rows where there's
        # no remainder
        else:  # 8CP
            if remainder > 0:
                _, rack_well = get_tiprack_well_with_n_tips(pipette, remainder)
                pipette.pick_up_tip(rack_well)
                volume = eight_sample_columns_volume+_mastermix_volume
                pipette.aspirate(volume,
                                 mastermix_source[0])
                pipette.dispense(volume, dest_col_1[0])
                pipette.drop_tip()

            _, rack_well = \
                get_tiprack_well_with_n_tips(pipette,
                                             len(mastermix_source)-remainder)
            pipette.pick_up_tip(rack_well)
            volume = eight_sample_columns_volume
            pipette.aspirate(volume, mastermix_source[remainder])
            pipette.dispense(volume, dest_col_1[remainder])

    # Distribute the mastermix into the rest of the target wells
    drop_all_tips([left_pipette, right_pipette])
    if n_target_columns > 1:
        ctx.comment("\nDistributing mastermix into all sample wells\n")

        mastermix_column = dna_mastermix_target_plate.columns()[0]
        target_columns = \
            dna_mastermix_target_plate.columns()[1:n_target_columns]
        remainder_column = \
            dna_mastermix_target_plate.columns()[n_target_columns+1]

        pipette = select_pipette(_mastermix_volume,
                                 mastermix_column,
                                 dna_mastermix_target_plate)
        if is_single(pipette):
            for col in target_columns:
                pipette.transfer(_mastermix_volume,
                                 mastermix_column,
                                 col)
            if remainder > 0:
                dest_col = \
                    dna_mastermix_target_plate.columns()[n_target_columns+1]
                pipette.transfer(_mastermix_volume,
                                 mastermix_column[:remainder],
                                 dest_col[:remainder])
        else:
            if n_target_columns > 1:
                _, rack_well = \
                    get_tiprack_well_with_n_tips(pipette, 8)
                pipette.pick_up_tip(rack_well)
                volume = eight_sample_columns_volume
                for d_col in target_columns:
                    pipette.aspirate(volume, mastermix_source[0])
                    pipette.dispense(volume, d_col[0])
            if remainder > 0:
                _, rack_well = \
                    get_tiprack_well_with_n_tips(pipette, remainder)
                pipette.drop_tip()
                pipette.pick_up_tip(rack_well)
                pipette.aspirate(_mastermix_volume, mastermix_column[0])
                pipette.dispense(_mastermix_volume, remainder_column[0])

    # Distribute DNA into all sample wells and mix
    ctx.comment("\nDistributing DNA samples to target plate\n")
    drop_all_tips([left_pipette, right_pipette])

    source_columns = dna_sample_plate.columns()[:n_target_columns-1]
    target_columns = dna_mastermix_target_plate.columns()[:n_target_columns-1]
    source_remainder_column = \
        dna_sample_plate.columns()[n_target_columns]
    target_remainder_column = \
        dna_mastermix_target_plate.columns()[n_target_columns]


    pipette = select_pipette(_DNA_volume,
                             dna_sample_plate.columns()[0],
                             dna_sample_plate)
    if is_single(pipette):
        for s_col, d_col in zip(source_columns, target_columns):
            pipette.transfer(_DNA_volume,
                             s_col,
                             d_col)
        if remainder > 0:
            dest_col = \
                dna_mastermix_target_plate.columns()[n_target_columns+1]
            source_col = \
                dna_sample_plate.columns()[n_target_columns+1]
            pipette.transfer(_DNA_volume,
                             source_col[:remainder],
                             dest_col[:remainder])
    else:
        _, rack_well = \
            get_tiprack_well_with_n_tips(pipette, 8)
        pipette.pick_up_tip(rack_well)
        for s_col, d_col in zip(source_columns, target_columns):
            pipette.aspirate(_DNA_volume, s_col[0])
            pipette.dispense(volume, d_col[0])
        if remainder > 0:
            _, rack_well = \
                get_tiprack_well_with_n_tips(pipette, remainder)
            pipette.drop_tip()
            pipette.pick_up_tip(rack_well)
            pipette.aspirate(_DNA_volume, source_remainder_column[0])
            pipette.dispense(_DNA_volume, target_remainder_column[0])
    ctx.comment("Protocol complete")
