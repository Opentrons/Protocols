from opentrons import protocol_api
import math

metadata = {
    'protocolName': '357404: Slide antibody assay',
    'author': 'Eskil Andersen <protocols@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.11'   # CHECK IF YOUR API LEVEL HERE IS UP TO DATE
                         # IN SECTION 5.2 OF THE APIV2 "VERSIONING"
}


def get_values(*names):
    import json
    _all_values = json.loads("""{
                                  "n_slots":6,
                                  "vol_reagent":1500,
                                  "n_ab_containers":3,
                                  "do_step_x":true,
                                  "tuberack_lname":"opentrons_24_aluminumblock_nest_2ml_screwcap"
                                  }
                                  """)
    return [_all_values[n] for n in names]


def run(ctx: protocol_api.ProtocolContext):

    [n_slots,
     vol_reagent,
     n_ab_containers,
     do_step_x,
     tuberack_lname] = get_values(  # noqa: F821
     "n_slots",
     "vol_reagent",
     "n_ab_containers",
     "do_step_x",
     "tuberack_lname")

    slide_holder_lname = 'customslideholder_8_wellplate_15000ul'
    slide_slots = [1, 4, 5, 7, 8, 10, 11]

    # load modules
    temp_mod = ctx.load_module('temperature module gen2', '3')

    '''

    Add your modules here with:

    module_name = ctx.load_module('{module_loadname}', '{slot number}')

    Note: if you are loading a thermocycler, you do not need to specify
    a slot number - thermocyclers will always occupy slots 7, 8, 10, and 11.

    For all other modules, you can load them on slots 1, 3, 4, 6, 7, 9, 10.

    '''

    # load labware
    # Labware: 290 mL reservoir, Tuberack for reagents, slide holders
    reservoir = ctx.load_labware('agilent_1_reservoir_290ml', '2')
    tuberack = temp_mod.load_labware(tuberack_lname)
    slide_holders = []
    for slot in slide_slots[:n_slots]:
        slide_holder = ctx.load_labware(slide_holder_lname, slot)
        slide_holders.append(slide_holder)

    '''

    Add your labware here with:

    labware_name = ctx.load_labware('{loadname}', '{slot number}')

    If loading labware on a module, you can load with:

    labware_name = module_name.load_labware('{loadname}')
    where module_name is defined above.

    '''
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
    # Load 1000 uL tips on 9, 300 uL on 6
    tiprack_300 = [ctx.load_labware('opentrons_96_tiprack_300ul', '6')]
    tiprack_1000 = [ctx.load_labware('opentrons_96_tiprack_1000ul', '9')]

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
    # Load p300, p1000 gen2
    p300 = ctx.load_instrument(
                              'p300_single_gen2',
                              'left',
                              tip_racks=tiprack_300
                              )
    p1000 = ctx.load_instrument(
                              'p1000_single_gen2',
                              'left',
                              tip_racks=tiprack_1000
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
    def dispense_while_moving(pip, well, vol, steps):
        """
        This function dispenses a partial volume = vol/steps and then moves
        a distance/steps and repeats
        """
        pass

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
    class VolTracker:
        def __init__(self, labware, well_vol,
                     start=1, end=8,
                     mode='reagent',
                     pip_type='single',
                     msg='Reset labware volumes'):
            """
            Voltracker tracks the volume(s) used in a piece of labware

            :param labware: The labware to track
            :param well_vol: The volume of the liquid in the wells, if using a
            multi-pipette with a well plate, treat the plate like a reservoir,
            i.e. start=1, end=1, well_vol = 8 * vol of each individual well.
            :param pip_type: The pipette type used 'single' or 'multi'
            :param mode: 'reagent' or 'waste'
            :param start: The starting well
            :param end: The ending well
            :param msg: Message to send to the user when all wells are empty
            (or full when in waste mode)

            """
            self.labware_wells = dict.fromkeys(
                labware.wells()[start-1:end], 0)
            self.labware_wells_backup = self.labware_wells.copy()
            self.well_vol = well_vol
            self.pip_type = pip_type
            self.mode = mode
            self.start = start
            self.end = end
            self.msg = msg

            # Parameter error checking
            if not (pip_type == 'single' or pip_type == 'multi'):
                raise Exception('Pipette type must be single or multi')

            if not (mode == 'reagent' or mode == 'waste'):
                raise Exception('mode must be reagent or waste')

    # reagents

    '''
    Define where all reagents are on the deck using the labware defined above.

    e.g.

    water = reservoir12.wells()[-1]
    waste = reservoir.wells()[0]
    samples = plate.rows()[0][0]
    dnase = tuberack.wells_by_name()['A4']

    '''
    # Each slide holder has 8 "wells", each well uses up 100 uL of each
    # reagent: Block, antibody1, antibody2, nuclear counterstain
    total_reagent_vol = 100 * n_slots * 8
    n_tubes = math.ceil(total_reagent_vol / vol_reagent)
    block = VolTracker(tuberack, 1500, start=1, end=n_tubes)
    antibody1 = VolTracker(tuberack, 1500, start=n_tubes+1, end=n_tubes*2+1)
    antibody2 = VolTracker(tuberack, 1500, start=n_tubes*2+1, end=n_tubes*3+1)
    # Nuclear counterstain
    nuc_cstn = VolTracker(tuberack, 1500, start=n_tubes*3+1, end=n_tubes*4+1)
    pbs = VolTracker(
        reservoir, 290*10**3, start=1, end=2, mode='reagent',
        pip_type='single', msg="Refill PBS reservoir")

    # plate, tube rack maps
    target_wells = []
    for slide_holder in slide_holders:
        for well in slide_holder.wells():
            target_wells.append(well)

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
    # Set the temperature to 4 degrees on the temperature module.
    temp_mod.set_temperature(4)
    # Transfer 100 µL of block from the tuberack to each destination well
    # (slide) (could be done as a multi-dispense with the P1000)
    # Pause/Incubate for 1 hour
    # Transfer 100 µL of primary antibody to dest. wells (slide)
    # Pause 1 hour
    # Transfer 4 mL of PBS to each slide target well (i.e. 4 round trips)
    # with the P1000
    # Transfer 100 µL of the second antibody
    # Pause 1 hour
    # Transfer 4 mL of PBS to slide target wells
    # Transfer 100 µL nuclear counterstain to each well
    # Incubate 5 minutes
    # Transfer 4 mL PBS
    # Pause until resume (stop the protocol)
