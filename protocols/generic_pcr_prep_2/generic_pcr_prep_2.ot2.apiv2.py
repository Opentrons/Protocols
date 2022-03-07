import math
from opentrons import protocol_api

metadata = {
    'protocolName': 'Generic PCR Prep Part 2 - Mastermix and DNA Distribution',
    'author': 'Opentrons <protocols@opentrons.com>',
    'source': 'Protocol Library',
    'apiLevel': '2.11'
    }


def get_values(*names):
    import json
    _all_values = json.loads("""{
                                  "n_samples":96,
                                  "n_mixes":3,
                                  "n_sample_plate":1,
                                  "left_pipette_lname":"p20_multi_gen2",
                                  "right_pipette_lname":"p300_multi_gen2",
                                  "use_filter_tips_left":true,
                                  "use_filter_tips_right":true,
                                  "mastermix_volume":18,
                                  "DNA_volume":2,
                                  "mastermix_reservoir_lname":"nest_12_reservoir_15ml",
                                  "DNA_well_plate_lname":"nest_96_wellplate_100ul_pcr_full_skirt",
                                  "destination_well_plate_lname":"nest_96_wellplate_100ul_pcr_full_skirt",
                                  "DNA_well_plate_tmod":false,
                                  "dest_well_plate_tmod":false
                                  }
                                  """)
    return [_all_values[n] for n in names]


def run(ctx: protocol_api.ProtocolContext):

    [n_samples,
     n_mixes,
     n_sample_plate,
     left_pipette_lname,
     right_pipette_lname,
     use_filter_tips_left,
     use_filter_tips_right,
     mastermix_volume,
     DNA_volume,
     mastermix_reservoir_lname,
     DNA_well_plate_lname,
     destination_well_plate_lname,
     DNA_well_plate_tmod,
     dest_well_plate_tmod] = get_values(  # noqa: F821
     "n_samples",
     "n_mixes",
     "n_sample_plate",
     "left_pipette_lname",
     "right_pipette_lname",
     "use_filter_tips_left",
     "use_filter_tips_right",
     "mastermix_volume",
     "DNA_volume",
     "mastermix_reservoir_lname",
     "DNA_well_plate_lname",
     "destination_well_plate_lname",
     "DNA_well_plate_tmod",
     "dest_well_plate_tmod")

    # Error checking
    if not left_pipette_lname and not right_pipette_lname:
        raise Exception('You have to select at least 1 pipette.')

    if not (DNA_volume > 0 or mastermix_volume > 0):
        raise Exception('DNA or mastermix volume is 0 or less µL')

    DNA_plate_slot = '9'
    reservoir_slot = '3'
    dest_plate_slot = '6'
    tiprack_l_slots = ['4', '7']
    tiprack_r_slots = ['5', '8']

    # load modules
    '''

    Add your modules here with:

    module_name = ctx.load_module('{module_loadname}', '{slot number}')

    Note : if you are loading a thermocycler, you do not need to specify
    a slot number - thermocyclers will always occupy slots 7, 8, 10, and 11.

    For all other modules, you can load them on slots 1, 3, 4, 6, 7, 9, 10.

    '''

    tmod_list = []
    for tmod_lname, slot in zip([DNA_well_plate_tmod, dest_well_plate_tmod],
                                [DNA_plate_slot, dest_plate_slot]):
        if tmod_lname:
            tmod = ctx.load_module(tmod_lname, slot)
            tmod_list. append(tmod)
        else:
            tmod_list.append(None)
    tmod_dna_plate, tmod_dest_plate = tmod_list
    '''


    Add your labware here with:
    labware_name = ctx.load_labware('{loadname}', '{slot number}')

    If loading labware on a module, you can load with:

    labware_name = module_name.load_labware('{loadname}')
    where module_name is defined above.

    '''

    # labware setup
    plate_list = []
    for labware_lname, tmod, slot, name in \
        zip([DNA_well_plate_lname, destination_well_plate_lname],
            [tmod_dna_plate, tmod_dest_plate],
            [DNA_plate_slot, dest_plate_slot],
            ["DNA plate", "destination plate"]):
        if tmod:
            plate_list.append(tmod.load_labware(labware_lname, name))
        else:
            plate_list.append(ctx.load_labware(labware_lname, slot, name))

    DNA_well_plate, destination_well_plate = plate_list

    mastermix_reservoir = ctx.load_labware(mastermix_reservoir_lname,
                                           reservoir_slot,
                                           'mastermix reservoir')
    # load tipracks
    '''


    Add your tipracks here as a list:

    For
    a single tip rack:
    tiprack_name = [ctx.load_labware('{loadname}', '{slot number}')]

    For multiple tip racks of the same type:

    tiprack_name = [ctx.load_labware('{loadname}', 'slot')
                     for slot in ['1', '2', '3']]

    If two different tipracks are on the deck, use convention:
    tiprack[ number of microliters]
    e. g. tiprack10, tiprack20, tiprack200, tiprack300, tiprack1000
    '''

    tiprack_lnames = {
        "p20s_filtered": "opentrons_96_filtertiprack_20ul",
        "p20s_nonfiltered": "opentrons_96_tiprack_20ul",
        "p300s_filtered": "opentrons_96_filtertiprack_200ul",
        "p300s_nonfiltered": "opentrons_96_tiprack_300ul",
        "p1000s_filtered": "opentrons_96_filtertiprack_1000ul",
        "p1000s_nonfiltered": "opentrons_96_tiprack_1000ul"
    }

    # Helper function for loading tipracks
    def load_tipracks(tiprack_list, filtered_tips, non_filtered_tips,
                      is_filtered, slot):
        tip_type = filtered_tips if is_filtered else non_filtered_tips
        tiprack_list.append([ctx.load_labware(tip_type, s) for s in slot])

    tiprack_list = []

    for pip_lname, is_filtered, slot \
        in zip([left_pipette_lname, right_pipette_lname],
               [use_filter_tips_left, use_filter_tips_right],
               [tiprack_l_slots, tiprack_r_slots]):

        if "20_" in pip_lname:
            load_tipracks(tiprack_list, tiprack_lnames["p20s_filtered"],
                          tiprack_lnames["p20s_nonfiltered"], is_filtered,
                          slot)
        elif "300_" in pip_lname:
            load_tipracks(tiprack_list, tiprack_lnames["p300s_filtered"],
                          tiprack_lnames["p300s_nonfiltered"], is_filtered,
                          slot)
        elif "1000_" in pip_lname:
            load_tipracks(tiprack_list, tiprack_lnames["p1000s_filtered"],
                          tiprack_lnames["p1000s_nonfiltered"], is_filtered,
                          slot)
        else:
            tiprack_list.append(None)
    tiprack_l, tiprack_r = tiprack_list

    # load instrument
    '''
    Nomenclature for pipette:

    use 'p' for single-channel, 'm' for multi-channel,
    followed by number of microliters.

    p20, p300, p1000 (single channel pipettes)
    m20, m300 (multi-channel pipettes)

    If loading pipette, load with:
    ctx.load_instrument('{pipette api load name}',
                        pipette_mount("left", or "right"),
                        tip_racks= tiprack )
    '''

    pipette_l = None
    pipette_r = None
    pipettes = []
    for pip, mount, tiprack in zip([left_pipette_lname, right_pipette_lname],
                                   ["left", "right"],
                                   [tiprack_l, tiprack_r]):
        if pip:
            pipettes.append(ctx.load_instrument(pip, mount, tip_racks=tiprack))
        else:
            pipettes.append(None)

    pipette_l, pipette_r = pipettes
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
    the function.
    '''
    def is_multi_channel(pip): return True if pip.channels == 8 else False

    def pick_up_tip(pipette):
        """
        Safe function for picking up tips in that it checks for tip
        availability and asks user to replace tips if the tipracks
        have run empty.

        :param pipette: Pipette to pick up tip with
        """
        try:
            pipette.pick_up_tip()
        except protocol_api.labware.OutOfTipsError:
            ctx.pause("Replace empty tip racks")
            pipette.reset_tipracks()
            pipette.pick_up_tip()

    def rank_pipettes(pipette_l, pipette_r):
        """
        Given two pipettes this fn will return them in the order of smallest
        to largest. This function assumes that error checking for cases where
        no pipettes were loaded was already done.
        """
        if not pipette_l:
            return [pipette_r, pipette_r]
        elif not pipette_r:
            return [pipette_l, pipette_l]
        else:
            if pipette_l.max_volume <= pipette_r.max_volume:
                return [pipette_l, pipette_r]
            else:
                return [pipette_r, pipette_l]

    def pipette_selector(small_pipette, large_pipette, volume):
        """
        This function will try to return a multi-channel pipette that
        can handle the given volume, and failing that a single channel pip.
        """
        if small_pipette.min_volume >= volume \
                and is_multi_channel(small_pipette):
            return small_pipette
        elif large_pipette.min_volume >= volume \
                and is_multi_channel(large_pipette):
            return large_pipette
        elif small_pipette.min_volume >= volume:
            return small_pipette
        elif large_pipette.min_volume >= volume:
            return large_pipette
        else:
            raise Exception("No suitable pipette for a volume of {} loaded".
                            format(volume))

    # helper functions
    ''' Define any custom helper functions outside of the pipette scope here,
    using the convention seen above.
    e.g.
    def
        remove_supernatant(vol, index):
        """
        function description
        : param vol:
        : param index:
        """

    '''
    def resv_to_plate_transfer(pipette, vol, source_well, dest_plate,
                               drop_tips=False):
        """
        Transfer from a reservoir to a plate. If the pipette is multi channel
        the transfers will be column to column.

        :param pipette: Pipette for the pipetting actions
        :param vol: The volume per tip to transfer
        :param source_well: The reservoir well to transfer from
        :param dest_plate: The plate to transfer to
        :param drop_tips: Whether to drop tips after each transfer or use the
        same tips throughout. Defaults to false
        """
        # If the pip is multi-channel transfer to the a row well of each col
        if is_multi_channel(pipette):
            n_columns = math.ceil(n_samples/8)
            target_columns = dest_plate.columns()[0:n_columns-1]
            if not drop_tips:
                pick_up_tip(pipette)
            for col in target_columns:
                if drop_tips:
                    pick_up_tip(pipette)
                pipette.aspirate(vol, source_well)
                pipette.dispense(vol, col[0])
                if drop_tips:
                    pipette.drop_tip()
            if not drop_tips:
                pipette.drop_tip()
        # Single channel pip: well to well
        else:
            if not drop_tips:
                pick_up_tip(pipette)
            for well in dest_plate:
                # pipette.pick_up_tip()
                if drop_tips:
                    pick_up_tip(pipette)
                pipette.aspirate(vol, source_well)
                pipette.dispense(vol, well)
                if drop_tips:
                    pipette.drop_tip()
            if not drop_tips:
                pipette.drop_tip()

    def plate96_to_plate96_transfer(pipette, vol, source_plate, dest_plate,
                                    n_mixes, mix_vol, n_samples):
        """
        Transfer from a 96 well plate to a 96 well plate.
        If the pipette is multi channel the transfers will be column to column.

        :param pipette: Pipette for the pipetting actions
        :param vol: The volume per tip to transfer
        :param source_plate: The well plate to transfer from
        :param dest_plate: The well plate to transfer to
        :param n_mixes: How many times to mix after dispensing
        :param mix_vol: Mixing volume
        """
        # Multi-channel pip: column by column transfer
        if is_multi_channel(pipette):
            n_columns = math.ceil(n_samples/8)
            source_columns = source_plate.columns()[0:n_columns-1]
            target_columns = dest_plate.columns()[0:n_columns-1]
            for s_col, d_col in zip(source_columns, target_columns):
                pick_up_tip(pipette)
                pipette.aspirate(vol, s_col[0])
                pipette.dispense(vol, d_col[0])
                pipette.mix(n_mixes, mix_vol, d_col[0])
                pipette.drop_tip()
        # SCP: well by well transfer
        else:
            for s_well, d_well in zip(source_plate.wells()[:n_samples],
                                      dest_plate.wells()[:n_samples]):
                pick_up_tip(pipette)
                pipette.aspirate(vol, s_well)
                pipette.dispense(vol, d_well)
                pipette.mix(n_mixes, mix_vol, d_well)
                pipette.drop_tip()

    def plate96_to_plate384_transfer(pipette, vol, source_plate, dest_plate,
                                     n_mixes, mix_vol, n_samples, offset):
        """
        Transfer from a well plate to a well plate.
        If the pipette is multi channel the transfers will be column to column.

        :param pipette: Pipette for the pipetting actions
        :param vol: The volume per tip to transfer
        :param source_plate: The 96 well plate to transfer from
        :param dest_plate: The 384 well plate to transfer to
        :param n_mixes: How many times to mix after dispensing
        :param mix_vol: Mixing volume
        """
        # Error check
        s_len = len(source_plate.wells())
        d_len = len(dest_plate.wells())
        if not s_len == 96 and d_len == 384:
            raise Exception(("Source plate should have 96 wells, and the "
                             "destination plate should have 384, but they "
                             "have {} and {} wells").format(s_len, d_len))
        # Multi-channel pip: column by column transfer
        if is_multi_channel(pipette):
            n_columns = math.ceil(n_samples/8)
            n_offset_columns = math.ceil(offset/8)
            source_wells = [column[0] for column
                            in source_plate.columns()[:n_columns]]
            target_wells = []
            for i in range(n_offset_columns, n_columns + n_offset_columns):
                if i % 2 == 0:
                    target_wells.append(dest_plate.columns[i][0])
                else:
                    target_wells.append(dest_plate.columns[i][1])
            for s_well, d_well in zip(source_wells, target_wells):
                pick_up_tip(pipette)
                pipette.aspirate(vol, s_well)
                pipette.dispense(vol, d_well)
                pipette.mix(n_mixes, mix_vol, d_well)
                pipette.drop_tip()
        # SCP: well by well transfer
        else:
            for s_well, d_well in zip(source_plate.wells()[:n_samples],
                                      dest_plate.wells()
                                      [n_offset_columns:n_samples]):
                pick_up_tip(pipette)
                pipette.aspirate(vol, s_well)
                pipette.dispense(vol, d_well)
                pipette.drop_tip()

    def plate384_to_plate384_transfer(pipette, vol, source_plate, dest_plate,
                                      n_mixes, mix_vol, n_samples, offset):
        """
        Transfer from a well plate to a well plate.
        If the pipette is multi channel the transfers will be column to column.

        :param pipette: Pipette for the pipetting actions
        :param vol: The volume per tip to transfer
        :param source_plate: The 96 well plate to transfer from
        :param dest_plate: The 384 well plate to transfer to
        :param n_mixes: How many times to mix after dispensing
        :param mix_vol: Mixing volume
        """
        # Error check
        s_len = len(source_plate.wells())
        d_len = len(dest_plate.wells())
        if not s_len == 384 and d_len == 384:
            raise Exception(("The source and destination plate should have "
                             "384 wells, but they have {} and {} wells").
                            format(s_len, d_len))
        # Multi-channel pip: column by column transfer
        if is_multi_channel(pipette):
            n_columns = math.ceil(n_samples/8)
            n_offset_columns = math.ceil(offset/8)
            source_wells = []
            target_wells = []
            for i in range(n_offset_columns, n_columns + n_offset_columns):
                if i % 2 == 0:
                    source_wells.append(source_plate.columns[i][0])
                    target_wells.append(dest_plate.columns[i][0])
                else:
                    source_wells.append(source_plate.columns[i][1])
                    target_wells.append(dest_plate.columns[i][1])
            for s_well, d_well in zip(source_wells, target_wells):
                pick_up_tip(pipette)
                pipette.aspirate(vol, s_well)
                pipette.dispense(vol, d_well)
                pipette.mix(n_mixes, mix_vol, d_well)
                pipette.drop_tip()
        # SCP: well by well transfer
        else:
            for s_well, d_well in zip(source_plate.wells()[:n_samples],
                                      dest_plate.wells()
                                      [n_offset_columns:n_samples]):
                pick_up_tip(pipette)
                pipette.aspirate(vol, s_well)
                pipette.dispense(vol, d_well)
                pipette.drop_tip()
    # reagents
    '''
    Define where all reagents are on the deck using the labware defined above.

    e.g.

    water = reservoir12.wells()[-1]
    waste = reservoir.wells()[0]
    samples = plate.rows()[0][0]
    dnase = tuberack.wells_by_name()['A4']

    '''
    mastermix = mastermix_reservoir.wells()[0]

    '''

    Include header sections as follows for each "section" of your protocol.

    Section can be defined as a step in a bench protocol.

    e.g.

    ctx.comment('\n\nMOVING MASTERMIX TO SAMPLES IN COLUMNS 1-6\n')

    for .... in ...:
        ...
        ...

    ctx.comment('\n\nRUNNING THERMOCYCLER PROFILE\n')
    '''

    n_wells_source = len(DNA_well_plate.wells())
    n_wells_dest = len(destination_well_plate.wells())
    if n_wells_dest < n_samples:
        raise Exception("The destination plate does not have enough wells ({})"
                        "for all the samples ({})".
                        format(n_wells_dest, n_samples))

    # determine which pipette has the smaller volume range
    pip_s, pip_l = rank_pipettes(pipette_l, pipette_r)
    # Make sure we have a pipette that can handle the volume of mastermix
    # Ideally the smaller one
    pipette = pipette_selector(pip_s, pip_l, mastermix_volume)
    ctx.comment("\n\nTransferring master mix to target plate\n")
    resv_to_plate_transfer(pipette, mastermix_volume, mastermix,
                           destination_well_plate)

    # Transfer DNA to the destination plate
    pipette = pipette_selector(pip_s, pip_l, DNA_volume)
    ctx.comment("\n\nTransferring DNA to target plate\n")
    if n_wells_source == 96:
        mixing_volume = DNA_volume + mastermix_volume - 1
        if n_wells_dest == 96:
            plate96_to_plate96_transfer(pipette, DNA_volume, DNA_well_plate,
                                        n_mixes, mixing_volume,
                                        destination_well_plate, n_samples)
        elif n_wells_dest == 384:
            remaining_samples = n_samples
            while remaining_samples > 0:
                plate96_to_plate384_transfer()
                remaining_samples -= 96
        else:
            raise Exception(
                "The destination plate has an unexpected number of wells: {}".
                format(n_wells_dest))
    elif n_wells_source == 384 and n_wells_dest == 384:
        plate384_to_plate384_transfer()
    else:
        raise Exception(
            "The protocol cannot transfer from a {} to a {} well plate".
            format(n_wells_source, n_wells_dest))
    ctx.comment("\n\n~~~~ Protocol complete ~~~~\n")
