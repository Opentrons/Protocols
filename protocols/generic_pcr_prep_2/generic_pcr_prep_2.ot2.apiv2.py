import math
from opentrons import protocol_api

metadata = {
    'protocolName': 'PCR Prep part 2',
    'author': 'Opentrons <protocols@opentrons.com>',
    'source': 'Protocol Library',
    'apiLevel': '2.2'
    }


def get_values(*names):
    import json
    _all_values = json.loads("""{ "number_of_samples":"80",
                                  "left_pipette_lname":"p300_multi_gen2",
                                  "right_pipette_lname":"p20_multi_gen2",
                                  "use_filter_tips_left": false,
                                  "use_filter_tips_right": false,
                                  "mastermix_volume":"18",
                                  "DNA_volume":"2",
                                  "twelve_well_reservoir_lname",
                                  "DNA_well_plate_lname":"biorad_96_wellplate_200ul_pcr",
                                  "destination_well_plate_lname":"biorad_96_wellplate_200ul_pcr",
                                  "DNA_well_plate_tmod",
                                  "dest_well_plate_tmod"}
                                  """)
    return [_all_values[n] for n in names]


def run(ctx: protocol_api.ProtocolContext):
    [number_of_samples, left_pipette_lname, right_pipette_lname,
     mastermix_volume, use_filter_tips_left, use_filter_tips_right,
     DNA_volume, twelve_well_reservoir_lname, DNA_well_plate,
     destination_well_plate] \
      = get_values(  # noqa: F821
        "number_of_samples", "left_pipette_lname", 'right_pipette_lname',
        "use_filter_tips_left", "use_filter_tips_right",
        "mastermix_volume", "DNA_volume", "twelve_well_reservoir_lname",
        "DNA_well_plate", "destination_well_plate_lname"
     )

    # Error checking
    if not left_pipette and not right_pipette:
        raise Exception('You have to select at least 1 pipette.')

    dna_plate_slot = '9'
    reservoir_slot = '3'
    dest_plate_slot = '6'
    tiprack_l_slots = ['4', '7']
    tiprack_r_slots = ['5', '8']

    # load modules
    '''

    Add your modules here with:

    module_name = ctx.load_module('{module_loadname}', '{slot number}')

    Note: if you are loading a thermocycler, you do not need to specify
    a slot number - thermocyclers will always occupy slots 7, 8, 10, and 11.

    For all other modules, you can load them on slots 1, 3, 4, 6, 7, 9, 10.

    '''
    tmod_list = []
    for tmod_lname, slot in zip([DNA_well_plate_tmod, dest_well_plate_tmod],
                                [DNA_plate_slot, dest_plate_slot]):
        if tmod_lname:
            tmod = ctx.load_module(tmod_lname, slot)
            tmod_list.append(tmod)
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
            [labware_1_slot, labware_2_slot],
            ["Tube rack 1", "Tube rack 2"]):
        if labware_lname:
            if tmod:
                plate_list.append(tmod.load_labware(labware_lname, name))
            else:
                plate_list.append(ctx.load_labware(labware_lname, slot,
                                                   name))
        else:
            plate_list.append(None)
    labware1, labware2 = plate_list
    dna_plate = ctx.load_labware(
        DNA_well_plate, '1', 'DNA plate')
    dest_plate = ctx.load_labware(
        destination_well_plate, '2', 'Destination plate')
    res12 = ctx.load_labware(
        'usascientific_12_reservoir_22ml', '3', 'reservoir')
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

    tiprack_lnames = {
        "p20s_filtered": "opentrons_96_filtertiprack_20ul",
        "p20s_nonfiltered": "opentrons_96_tiprack_20ul",
        "p300s_filtered": "opentrons_96_filtertiprack_200ul",
        "p300s_nonfiltered": "opentrons_96_tiprack_300ul",
        "p1000s_filtered": "opentrons_96_filtertiprack_1000ul",
        "p1000s_nonfiltered": "opentrons_96_tiprack_1000ul"
    }

    tipracks = []
    for pip_lname, is_filtered, slot in zip([left_pipette_lname,
                                            right_pipette_lname],
                                            [use_filter_tips_left,
                                             use_filter_tips_right],
                                            [tiprack_l_slots,
                                             tiprack_r_slots]):
        if "20_" in pip_lname:
            if is_filtered:
                tipracks.append(
                    ctx.load_labware(tiprack_lnames["p20s_filtered"], slot))
            else:
                tipracks.append(
                    ctx.load_labware(tiprack_lnames["p20s_nonfiltered"], slot))
        elif "300_" in pip_lname:
            if is_filtered:
                tipracks.append(
                    ctx.load_labware(tiprack_lnames["p300s_filtered"], slot))
            else:
                tipracks.append(
                    ctx.load_labware(tiprack_lnames["p300s_nonfiltered"],
                                     slot))
        elif "1000_" in pip_lname:
            if is_filtered:
                tipracks.append(
                    ctx.load_labware(tiprack_lnames["p100s_filtered"], slot))
            else:
                tipracks.append(
                    ctx.load_labware(tiprack_lnames["p1000s_nonfiltered"],
                                     slot))
        else:
            tipracks.append(None)
    tiprack_l, tiprack_r = tipracks

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
    pipette_l = None
    pipette_r = None

    for pip, mount, tiprack in zip(
            [left_pipette_lname, right_pipette_lname],
            ['left', 'right'],
            [tiprack_l, tiprack_r]):

        if pip:
            if mount == 'left':
                pipette_l = ctx.load_instrument(
                    pip, mount, tip_racks=[tiprack])
            else:
                pipette_r = ctx.load_instrument(
                    pip, mount, tip_racks=[tiprack])

    # determine which pipette has the smaller volume range
    pip_s, pip_l = rank_pipettes(pipette_l, pipette_r)
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
    def is_multi_channel(pip):
        return True if pip.channels == 8 else False

    def resv_to_plate_transfer(pipette, vol, source_well, dest):
        is_mc = is_multi_channel(pipette)
        if is_mc:
            n_columns = math.ceil(number_of_samples/8)
            target_columns = dest.columns()[0:n_columns-1]
            for col in target_columns:
                pipette.pick_up_tip()
                pipette.transfer(vol, source_well, col[0], new_tip='never')
                pipette.drop_tip()
        else:
            for well in dest:
                pipette.pick_up_tip()
                pipette.aspirate(vol, source_well)
                pipette.dispense(vol, well)
                pipette.drop_tip()

    def plate_to_plate_transfer(pipette, vol, source_plate, dest_plate):
        pass

    def pick_up_tip(pipette):
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
    # reagent setup
    mastermix = res12.wells()[0]

    # Make sure we have a pipette that can handle the volume of mastermix
    # Ideally the smaller one
    pipette = pipette_selector(pip_s, pip_l, mastermix_volume)

    col_num = math.ceil(number_of_samples/8)

    ctx.comment("Transferring master mix")
    pipette.pick_up_tip()
    for dest in dest_plate.rows()[0][:col_num]:
        pipette.transfer(
            mastermix_volume,
            mastermix,
            dest,
            new_tip='never'
        )
        pipette.blow_out(mastermix.top())
    pipette.drop_tip()

    # Transfer DNA to the destination plate
    pipette = pipette_selector(pip_s, pip_l, DNA_volume)

    ctx.comment("Transferring DNA")
    for source, dest in zip(dna_plate.rows()[0][:col_num],
                            dest_plate.rows()[0][:col_num]):
        pipette.transfer(DNA_volume, source, dest)


def rank_pipettes(pipette_l, pipette_r):
    """
    Given two pipettes this function will return them in the order of smallest
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
    This function will return the smallest volume pipette capable
    of handling the given volume parameter.
    """
    if small_pipette and large_pipette:
        if (volume <= small_pipette.max_volume
           and volume >= small_pipette.min_volume):
            return small_pipette
        elif (volume <= large_pipette.max_volume
              and volume >= large_pipette.min_volume):
            return large_pipette
        else:
            raise Exception(("There is no suitable pipette loaded for "
                             "pipetting a volume of {} uL").format(volume))
