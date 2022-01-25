from opentrons import protocol_api
import math

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
        json.loads("""{ "mag_engage_time":5,
                        "n_samples":36,
                        "small_pipette_lname":"p20_single_gen2",
                        "large_pipette_lname":"p300_multi_gen2",
                        "small_pipette_tipracks_lname":"opentrons_96_tiprack_20ul",
                        "large_pipette_tipracks_lname":"opentrons_96_tiprack_300ul",
                        "reservoir_lname": "nest_12_reservoir_15ml",
                        "destination_plate_lname":"biorad_96_wellplate_200ul_pcr",
                        "sample_plate_lname":"usascientific_96_wellplate_2.4ml_deep",
                        "mag_mod_lname":"magnetic module gen2",
                        "tube_rack_lname":"opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap",
                        "dest_temp_mod_lname":"temperature module gen2",
                        "resv_temp_mod_lname":"temperature module gen2",
                        "do_vortex_pause":"true",
                        "do_SDS_step":"false",
                        "do_DNAse_step":"true",
                        "use_NaCl":"true",
                        "bead_volume":30.0,
                        "starting_volume":1000.0,
                        "wash_buf_vol":150.0,
                        "elution_buf_vol":100.0,
                        "n_washes":3,
                        "n_wash_mixes":5,
                        "n_elution_mixes":5,
                        "incubation_time":2,
                        "n_bead_mixes":5,
                        "sds_buffer_vol":30}
                        """)
    param_list = [_all_values[n] for n in names]
    return param_list


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
        do_vortex_pause,
        do_SDS_step,
        do_DNAse_step,
        use_NaCl,
        bead_volume,
        starting_volume,
        wash_buf_vol,
        elution_buf_vol,
        n_washes,
        n_wash_mixes,
        n_elution_mixes,
        incubation_time,
        n_bead_mixes,
        sds_buffer_vol
    ] = get_values(  # noqa: F821 (<--- DO NOT REMOVE!)
        "mag_engage_time",
        "n_samples",
        "small_pipette_lname",
        "large_pipette_lname",
        "small_pipette_tipracks_lname",
        "large_pipette_tipracks_lname",
        "reservoir_lname",
        "destination_plate_lname",
        "sample_plate_lname",
        "mag_mod_lname",
        "tube_rack_lname",
        "dest_temp_mod_lname",
        "resv_temp_mod_lname",
        "do_vortex_pause",
        "do_SDS_step",
        "do_DNAse_step",
        "use_NaCl",
        "bead_volume",
        "starting_volume",
        "wash_buf_vol",
        "elution_buf_vol",
        "n_washes",
        "n_wash_mixes",
        "n_elution_mixes",
        "incubation_time",
        "n_bead_mixes",
        "sds_buffer_vol"
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

    total_vol_after_bead_adddn = round(total_lysis_vol + bead_volume, 1)
    if use_NaCl:
        total_vol_after_bead_adddn = round(total_vol_after_bead_adddn +
                                           nacl_first_step_vol, 1)

    n_columns = math.ceil(n_samples/8)

    def str_to_bool(str):
        return True if str.lower().strip() == "true" else False

    # Convert string booleans to Python booleans
    do_vortex_pause = str_to_bool(do_vortex_pause)
    do_SDS_step = str_to_bool(do_SDS_step)
    do_DNAse_step = str_to_bool(do_DNAse_step)
    use_NaCl = str_to_bool(use_NaCl)

    # Error checking

    # If DNAse I is being added from a tube we need to make sure that
    # a) we have a single pipette loaded and b) that dnaseI_vol > pipette min.
    # volume
    if (("single" not in small_pipette_lname and
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

    # TODO: Check that sample well is large enough for lysis reaction
    # (including NaCl addition if used)
    sample_well = sample_plate.wells()[0]
    if total_vol_after_bead_adddn > sample_well.max_volume:
        raise Exception("The sample wells are too small to handle the " +
                        "volumes of reagents")

    dest_plate = None
    if dest_temp_mod_lname != "None":
        dest_plate = dest_temp_mod.load_labware(destination_plate_lname)
    else:
        dest_plate = ctx.load_labware(destination_plate_lname, '4')

    reservoir = None
    if resv_temp_mod_lname != "None":
        reservoir = resv_temp_mod.load_labware(reservoir_lname)
    else:
        reservoir = ctx.load_labware(reservoir_lname, '7')

    dnaseI_tuberack = None
    if do_DNAse_step:
        dnaseI_tuberack = ctx.load_labware(tube_rack_lname, '10')

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
                      for slot in ['5', '8', '11']]
    tipracks_small = [ctx.load_labware(small_pipette_tipracks_lname, slot)
                      for slot in ['6', '9']]

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
                        small_pipette_lname,
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
    def choose_pipette(vol, multi_action=True):
        """
        Choose pipette selects an appropriate pipette based on
        the volume involved, and whether the pipette action involves all
        8 columns or a single well.

        :param vol: The volume to use this pipette with
        :param multi_action: True if the pipette action will be done with
        an 8-channel pipette, i.e. involving an 8-channel source and/or target

        """
        nonlocal s_pip, l_pip
        s_pip_is_multi = True if s_pip.channels == 8 else False
        l_pip_is_multi = True if l_pip.channels == 8 else False

        if s_pip.min_volume > vol:
            raise Exception(("The volume ({} uL)is too small to handle for " +
                             "either pipette, please re-examine your" +
                             "parameters").format(vol))

        # The preference is for the multi-channel pipette with the largest
        # volume capability while the least preferred is the smallest volume
        # single channel pipette.
        if multi_action:
            # Prefer the multi-channel pipettes if available
            if l_pip_is_multi and l_pip.min_volume < vol:
                return l_pip, True
            elif s_pip_is_multi:
                return s_pip, True
            # If they are not, let a single channel pipette do the job of a
            # multi-channel pipette
            elif not l_pip_is_multi and l_pip.min_volume < vol:
                return l_pip, False
            else:
                return s_pip, False
        else:
            if not l_pip_is_multi and l_pip.min_volume < vol:
                return l_pip, False
            elif not s_pip_is_multi:
                return s_pip, False
            else:
                raise Exception(("No approriate single channel pipette is " +
                                "loaded for the volume of {} uL".format(vol)))

    def transfer(pip, volume, source, dest, **kwargs):
        """
        A wrapper function for InstrumentContext.transfer that handles
        labware.OutOfTipsError by asking the user to refill empty tipracks.

        :param pip: The pipette to user for the transfer

        Other parameters: See class
        opentrons.protocol_api.contexts.InstrumentContext
        """
        try:
            pip.transfer(volume, source, dest, kwargs)
        except protocol_api.labware.OutOfTipsError:
            ctx.pause("\n\nReplace empty tip racks for {}\n".format(pip.name))
            pip.reset_tipracks()
            pip.transfer(volume, source, dest, kwargs)

    def reag_to_wells_or_col_transfer(vol, reag_source_well, dest_plate,
                                      multi_transfer=True, **transfer_kwargs):
        """
        function description

        :param vol:

        :param index:
        """
        nonlocal n_columns, n_samples
        pip, pip_is_multi = choose_pipette(vol, multi_transfer)

        if pip_is_multi:
            dest_columns = dest_plate.columns()[0:n_columns]
            for col in dest_columns:
                transfer(pip, vol, reag_source_well, col[0],
                         **transfer_kwargs)
        else:  # Transfer to each well
            transfer(pip, vol, reag_source_well,
                     dest_plate.wells()[0:n_samples],
                     **transfer_kwargs)

    def remove_supernatant(vol, source_plate, multi_transfer=True,
                           **transfer_kwargs):
        """
        Removes a volume from each sample well of the source plate
        (well 0 to well n_samples) and transfers it to the liquid trash
        well of the reservoir.

        :param vol (float): The volume to transfer to the trash.

        :param source_plate (labware plate): The plate to aspirate from.

        :param multi_transfer (Boolean): Use 8-channel pipette and transfer
        a whole column at a time if true, otherwise use a single channel
        pipette and transfer well by well.

        :param **transfer_kwargs: Any keyword arguments that you may want
        to pass into the transfer method calls
        """
        nonlocal n_columns, n_samples
        pip, pip_is_multi = choose_pipette(vol, multi_transfer)

        if pip_is_multi:
            source_columns = source_plate.columns()[0:n_columns]
            for col in source_columns:
                transfer(pip, vol, col[0], waste_well, **transfer_kwargs)
        else:  # Transfer from each well
            transfer(pip, vol, source_plate.wells()[0:n_samples],
                     waste_well, **transfer_kwargs)

    def transfer_plate_to_plate(vol, source_plate, destination_plate):
        pip, is_multi = choose_pipette(vol, True)
        if is_multi:
            for s_col, d_col in zip(source_plate.columns(),
                                    destination_plate.columns()):
                transfer(pip, vol, s_col[0], d_col[0])
        else:
            transfer(pip, vol, sample_wells, dest_wells)

    # reagents

    '''
    Define where all reagents are on the deck using the labware defined above.

    e.g.

    water = reservoir12.wells()[-1]
    waste = reservoir.wells()[0]
    samples = plate.rows()[0][0]
    dnase = tuberack.wells_by_name()['A4']

    '''

    lysis_buffer_well = reservoir.wells_by_name()['A1']
    wash_buffer_well = reservoir.wells_by_name()['A2']
    elution_buffer_well = reservoir.wells_by_name()['A3']
    nacl_well = reservoir.wells_by_name()['A4']
    bead_well = reservoir.wells_by_name()['A5']
    waste_well = reservoir.wells()[-1]  # Use the last well for waste
    dnaseI_tube = None
    if dnaseI_tuberack:
        dnaseI_tube = dnaseI_tuberack.wells_by_name()['A1']
    sds_page_buf_well = None
    if do_SDS_step:
        sds_page_buf_well = reservoir.wells_by_name()['A6']

    # plate, tube rack maps

    '''
    Define any plate or tube maps here.

    e.g.

    plate_wells_by_row = [well for row in plate.rows() for well in row]

    '''
    # unused
    # sample_columns = sample_plate.columns()[0:n_columns]

    sample_wells = sample_plate.wells()[0:n_samples]

    dest_columns = dest_plate.columns()[0:n_columns]
    dest_wells = dest_plate.wells()[0:n_samples]

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
    pip, pip_is_multi = choose_pipette(lysis_buffer_vol)

    reag_to_wells_or_col_transfer(lysis_buffer_vol, lysis_buffer_well,
                                  sample_plate, True)

    if do_DNAse_step:
        ctx.comment('\n\nAdding DNAse I to sample wells\n')
        # Must be single channel, protocol will raise exception otherwise
        reag_to_wells_or_col_transfer(dnaseI_vol, dnaseI_tube, sample_plate,
                                      False)

    ctx.pause("\n\nPlace sample plate on a shaker and shake for 10-20" +
              " minutes at room temperature for the lysis reaction" +
              " to complete\n")

    # Optional addition of NaCl for improved binding to beads
    if use_NaCl:
        ctx.comment("Adding NaCl to samples for a final conc. of 500 mM")
        reag_to_wells_or_col_transfer(nacl_first_step_vol, nacl_well,
                                      sample_plate, True)

    if do_vortex_pause:
        ctx.pause("Pause to vortex/resuspend your magnetic beads")

    # Mixing the beads in the bead well
    pick_up(l_pip)
    l_pip.mix(n_bead_mixes, l_pip.max_volume, bead_well)

    ctx.comment("\n\nTransferring bead solution to sample wells and mixing")
    pip, pip_is_multi = choose_pipette(bead_volume, True)
    if pip_is_multi:
        for col in dest_columns:
            if not pip.has_tip:
                pick_up(pip)
            pip.aspirate(bead_volume, bead_well)
            pip.dispense(bead_volume, col[0])
            mix_vol = (pip.max_volume if total_vol_after_bead_adddn/2 >
                       pip.max_volume else total_vol_after_bead_adddn/2)
            pip.mix(5, mix_vol, col[0])
            pip.drop_tip()
    else:
        for well in sample_wells:
            if not pip.has_tip:
                pick_up(pip)
            pip.aspirate(bead_volume, bead_well)
            pip.dispense(bead_volume, well)
            mix_vol = (pip.max_volume if total_vol_after_bead_adddn/2 >
                       pip.max_volume else total_vol_after_bead_adddn/2)
            pip.mix(5, mix_vol, well)
            pip.drop_tip()

    ctx.comment("\n\nIncubating beads\n")
    ctx.delay(0, incubation_time)
    ctx.comment("\n\nEngaging magnets\n")
    mag_mod.engage()
    ctx.delay(0, mag_engage_time)
    ctx.comment("\n\nRemoving supernatant\n")
    remove_supernatant(total_vol_after_bead_adddn, sample_plate)

    # Wash the beads n_washes times, the standard is 3 washes
    repetitions = 1 if do_SDS_step else n_washes
    for i in range(0, repetitions):
        ctx.comment("\n\nBead wash #{}".format(i + 1))
        mag_mod.disengage()
        # Transfer wash buffer to the sample wells
        supernatant_volume = (wash_buf_vol + nacl_wash_buf_vol if use_NaCl
                              else wash_buf_vol)
        half_supernatant_vol = supernatant_volume/2
        mix_vol = (half_supernatant_vol if half_supernatant_vol
                   < l_pip.max_volume else l_pip.max_volume)
        if use_NaCl:
            reag_to_wells_or_col_transfer(wash_buf_vol, wash_buffer_well,
                                          sample_plate, True)
            reag_to_wells_or_col_transfer(nacl_wash_buf_vol, nacl_well,
                                          sample_plate, True,
                                          mix_after=(n_wash_mixes, mix_vol))
        else:
            reag_to_wells_or_col_transfer(wash_buf_vol, wash_buffer_well,
                                          sample_plate, True,
                                          mix_after=(n_wash_mixes, mix_vol))
        mag_mod.engage()
        ctx.delay(0, mag_engage_time)
        # Remove supernatant
        remove_supernatant(supernatant_volume, sample_plate)

    mag_mod.disengage()

    if do_SDS_step:
        ctx.comment("\n\nAdding 1x SDS-PAGE buffer\n")
        reag_to_wells_or_col_transfer(sds_buffer_vol, sds_page_buf_well,
                                      sample_plate, True)
        mag_mod.engage()
        ctx.delay(0, mag_engage_time)
        # Transfer to target plate
        ctx.comment("\n\nTransferring protein in SDS-buffer to target plate\n")
        transfer_plate_to_plate(sds_buffer_vol, sample_plate, dest_plate)
    # Elute
    else:
        ctx.comment("\n\nAdding elution buffer and mixing\n")
        reag_to_wells_or_col_transfer(elution_buf_vol, elution_buffer_well,
                                      sample_plate, True,
                                      mix_after=(n_elution_mixes, mix_vol))
        ctx.comment("\n\nIncubating samples with elution buffer\n")
        ctx.delay(0, incubation_time)
        ctx.comment("\n\nAttracting beads to magnets\n")
        mag_mod.engage()
        ctx.delay(0, mag_engage_time)
        ctx.comment("\n\nTransferring protein elution supernatant to" +
                    "target plate\n")
        transfer_plate_to_plate(elution_buf_vol, sample_plate, dest_plate)
        ctx.comment("\n\n~~~~~ End of protocol ~~~~~\n")
        import pdb; pdb.set_trace()
