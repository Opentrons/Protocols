from opentrons import protocol_api

metadata = {
    'protocolName': 'Generic PCR Prep: part 1 - mastermix creation',
    'author': 'Opentrons <protocols@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.11'   # CHECK IF YOUR API LEVEL HERE IS UP TO DATE
                         # IN SECTION 5.2 OF THE APIV2 "VERSIONING"
}


def get_values(*names):
    import json
    _all_values = json.loads("""{ "left_pipette_lname":"p1000_single_gen2",
                                  "right_pipette_lname":"p300_single_gen2",
                                  "use_filter_tips_left":false,
                                  "use_filter_tips_right":false,
                                  "tuberack_1_lname":"opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap",
                                  "tuberack_2_lname":"opentrons_24_tuberack_generic_2ml_screwcap",
                                  "twelve_well_resv_lname":"nest_12_reservoir_15ml",
                                  "tmod_1_lname",
                                  "tmod_2_lname",
                                  "master_mix_csv":"Reagent,Slot,Well,Volume\\nBuffer,1,A2,3\\nMgCl,1,A3,40\\ndNTPs,2,A2,90\\nWater,2,A3,248\\nprimer 1,1,A4,25\\nprimer 2,1,A5,25\\n"}""")
    return [_all_values[n] for n in names]


def run(ctx: protocol_api.ProtocolContext):

    [
      left_pipette_lname,
      right_pipette_lname,
      use_filter_tips_left,
      use_filter_tips_right,
      tuberack_1_lname,
      tuberack_2_lname,
      twelve_well_resv_lname,
      tmod_1_lname,
      tmod_2_lname,
      master_mix_csv
    ] = get_values(  # noqa: F821 (<--- DO NOT REMOVE!)
      "left_pipette_lname",
      "right_pipette_lname",
      "use_filter_tips_left",
      "use_filter_tips_right",
      "tuberack_1_lname",
      "tuberack_2_lname",
      "twelve_well_resv_lname",
      "tmod_1_lname",
      "tmod_2_lname",
      "master_mix_csv")

    if not left_pipette_lname and not right_pipette_lname:
        raise Exception('You have to select at least 1 pipette.')

    tuberack_1_slot = '1'
    tuberack_2_slot = '2'
    reservoir_slot = '3'

    # load modules
    '''

    Add your modules here with:

    module_name = ctx.load_module('{module_loadname}', '{slot number}')

    Note: if you are loading a thermocycler, you do not need to specify
    a slot number - thermocyclers will always occupy slots 7, 8, 10, and 11.

    For all other modules, you can load them on slots 1, 3, 4, 6, 7, 9, 10.

    '''
    tmod_list = []
    for tmod_lname, slot in zip([tmod_1_lname, tmod_2_lname],
                                [tuberack_1_slot, tuberack_2_slot]):
        if tmod_lname:
            tmod = ctx.load_module(tmod_lname, slot)
            tmod_list.append(tmod)
        else:
            tmod_list.append(None)
    tmod1, tmod2 = tmod_list

    '''

    Add your labware here with:

    labware_name = ctx.load_labware('{loadname}', '{slot number}')

    If loading labware on a module, you can load with:

    labware_name = module_name.load_labware('{loadname}')
    where module_name is defined above.

    '''
    # load labware
    # Load tuberacks
    tuberack_list = []
    for tuberack_lname, tmod, slot in zip([tuberack_1_lname, tuberack_2_lname],
                                          [tmod1, tmod2],
                                          [tuberack_1_slot, tuberack_2_slot]):
        if tuberack_lname:
            if tmod:
                tuberack_list.append(tmod.load_labware(tuberack_lname))
            else:
                tuberack_list.append(ctx.load_labware(tuberack_lname, slot))
        else:
            tuberack_list.append(None)
    tuberack1, tuberack2 = tuberack_list

    res12 = ctx.load_labware(
        twelve_well_resv_lname, reservoir_slot, '12-channel reservoir')

    reagents = {
        '1': tuberack1,
        '2': tuberack2,
        '3': res12
    }

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

    for pip, mount, slot in zip(
            [left_pipette_lname, right_pipette_lname],
            ['left', 'right'], ['5', '6']):

        if pip:
            range = pip.split('_')[0][1:]
            rack = 'opentrons_96_tiprack_' + range + 'ul'
            tiprack = protocol_context.load_labware(rack, slot)
            if mount == 'left':
                pipette_l = protocol_context.load_instrument(
                    pip, mount, tip_racks=[tiprack])
            else:
                pipette_r = protocol_context.load_instrument(
                    pip, mount, tip_racks=[tiprack])

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


metadata = {
    'protocolName': 'Generic PCR Prep',
    'author': 'Opentrons <protocols@opentrons.com>',
    'source': 'Protocol Library',
    'apiLevel': '2.11'
}


def run(protocol_context):
    [left_pipette, right_pipette, master_mix_csv] = get_values(  # noqa: F821
        "left_pipette", "right_pipette", "master_mix_csv")

    if not left_pipette and not right_pipette:
        raise Exception('You have to select at least 1 pipette.')

    pipette_l = None
    pipette_r = None

    for pip, mount, slot in zip(
            [left_pipette, right_pipette], ['left', 'right'], ['5', '6']):

        if pip:
            range = pip.split('_')[0][1:]
            rack = 'opentrons_96_tiprack_' + range + 'ul'
            tiprack = protocol_context.load_labware(rack, slot)
            if mount == 'left':
                pipette_l = protocol_context.load_instrument(
                    pip, mount, tip_racks=[tiprack])
            else:
                pipette_r = protocol_context.load_instrument(
                    pip, mount, tip_racks=[tiprack])

    # labware setup
    snaprack = protocol_context.load_labware(
        'opentrons_24_tuberack_eppendorf_2ml_safelock_snapcap',
        '1',
        'snapcap 2ml tuberack'
    )
    screwrack = protocol_context.load_labware(
        'opentrons_24_tuberack_generic_2ml_screwcap',
        '2',
        'screwcap 2ml tuberack'
    )
    res12 = protocol_context.load_labware(
        'usascientific_12_reservoir_22ml', '3', '12-channel reservoir')
    reagents = {
        '1': snaprack,
        '2': screwrack,
        '3': res12
    }

    # determine which pipette has the smaller volume range
    if pipette_l and pipette_r:
        if left_pipette == right_pipette:
            pip_s = pipette_l
            pip_l = pipette_r
        else:
            if pipette_l.max_volume < pipette_r.max_volume:
                pip_s, pip_l = pipette_l, pipette_r
            else:
                pip_s, pip_l = pipette_r, pipette_l
    else:
        pipette = pipette_l if pipette_l else pipette_r

    # destination
    mastermix_dest = res12.wells()[0]

    info_list = [
        [cell.strip() for cell in line.split(',')]
        for line in master_mix_csv.splitlines()[1:] if line
    ]

    for line in info_list:
        protocol_context.comment('Transferring ' + line[0] + ' to destination')
        source = reagents[line[1]].wells(line[2].upper())
        vol = float(line[3])
        if pipette_l and pipette_r:
            if vol <= pip_s.max_volume:
                pipette = pip_s
            else:
                pipette = pip_l
        pipette.transfer(vol, source, mastermix_dest)
