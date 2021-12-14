from opentrons import protocol_api
from math import ceil
from opentrons.protocol_api.labware import Well

metadata = {
    'protocolName': 'PCR Prep',
    'author': 'Opentrons <protocols@opentrons.com>',
    'source': 'Protocol Library',
    'apiLevel': '2.7'
}


def get_values(*names):
    import json
    _all_values = json.loads("""{ "create_mastermix":true,
                                  "use_same_pipettes":true,
                                  "number_of_samples":96,
                                  "left_pipette_part_1":"p300_single_gen2",
                                  "right_pipette_part_1":"p20_single_gen2",
                                  "left_pipette_tiprack_part_1":"opentrons_96_tiprack_300ul",
                                  "right_pipette_tiprack_part_1":"opentrons_96_tiprack_20ul",
                                  "left_pipette_part_2":"p20_single_gen2",
                                  "right_pipette_part_2":"p300_single_gen2",
                                  "left_pipette_tiprack_part_2":"opentrons_96_tiprack_20ul",
                                  "right_pipette_tiprack_part_2":"opentrons_96_tiprack_300ul",
                                  "temp_mod_slot_1":"temperature module gen2",
                                  "temp_mod_slot_4":"temperature module gen2",
                                  "temp_mod_slot_7":"temperature module gen2",
                                  "pcr_reagent_labware":"opentrons_24_aluminumblock_nest_1.5ml_snapcap",
                                  "aux_pcr_reagent_labware":"opentrons_24_aluminumblock_nest_1.5ml_screwcap",
                                  "target_labware":"opentrons_96_aluminumblock_biorad_wellplate_200ul",
                                  "mastermix_labware":"nest_12_reservoir_15ml",
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
        _temp_mod_slot_1,
        _temp_mod_slot_4,
        _temp_mod_slot_7,
        _pcr_reagent_labware,
        _aux_pcr_reagent_labware,
        _target_labware,
        _mastermix_labware,
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
                   "temp_mod_slot_1",
                   "temp_mod_slot_4",
                   "temp_mod_slot_7",
                   "pcr_reagent_labware",
                   "aux_pcr_reagent_labware",
                   "target_labware",
                   "mastermix_labware",
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
    temp_mod_slot_1, temp_mod_slot_4, temp_mod_slot_7 = None, None, None
    if _temp_mod_slot_1 is not None:
        temp_mod_slot_1 = ctx.load_module(_temp_mod_slot_1, '4')
    if _temp_mod_slot_4 is not None:
        temp_mod_slot_4 = ctx.load_module(_temp_mod_slot_4, '7')
    if _temp_mod_slot_7 is not None:
        temp_mod_slot_7 = ctx.load_module(_temp_mod_slot_7, '10')

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
                                 '4',
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
                                 '4',
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
                             '7',
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
        mastermix_destination = [mastermix_labware.wells_by_name()['A1']]
    elif _number_of_samples < 8:
        mastermix_destination = target_labware.columns()[0:_number_of_samples]
    else:
        mastermix_destination = target_labware.columns()[0]

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
        if temp_mod_slot_1 is not None:
            temp_mod_slot_1.set_temperature(_temperature)
        if temp_mod_slot_4 is not None:
            temp_mod_slot_4.set_temperature(_temperature)
        if temp_mod_slot_7 is not None:
            temp_mod_slot_7.set_temperature(_temperature)

        for line in mastermix_matrix:
            ctx.comment("Transferring {}".format(line[0]))
            source = None
            pipette = None
            volume = float(line[3]) / len(mastermix_destination)
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
            if "single" in pipette.name:
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
        if "single" in pipette.name:
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
                pipette.drop_tips()
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
