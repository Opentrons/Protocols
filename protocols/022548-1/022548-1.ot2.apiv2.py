from opentrons import protocol_api
from opentrons.protocol_api.labware import Labware, Well
import re
from typing import Tuple, Optional, Sequence
from math import ceil, pi

metadata = {
    'protocolName': '022548-2 - DNA extraction: Mastermix creation',
    'author': 'Eskil Andersen <protocols@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.11'   # CHECK IF YOUR API LEVEL HERE IS UP TO DATE
                         # IN SECTION 5.2 OF THE APIV2 "VERSIONING"
}


def parse_range_string(range: str) -> Tuple[int, int]:
    """ Parses a range or a single number from the input string.
    the format for a number is n-m, where n and m are any positive integers.
    :param range: range string to decode
    :return value: A tuple of the start and end index of the range
    """
    single_num_pattern = re.compile('[0-9]+')
    range_pattern = re.compile('[0-9]+-[0-9]+')
    # Case when there's only one index (e.g. the string decodes to a single
    # well
    if single_num_pattern.fullmatch(range) is not None:
        index = int(range)
        return index, index
    if range_pattern.fullmatch(range):
        # Return both substrings that match numbers (i.e. the start and
        # end indices
        start, end = range.split('-')
        return int(start), int(end)
    # If neither regular expression matched then we assume that the string
    # is incorrectly formatted
    raise Exception(("Invalid range string: it was \"{}\" but should be a "
                     "natural number or a range in the format of n-m where n "
                     "and m are natural numbers, "
                     "e.g: 1-4").format(range))


def get_values(*names):
    import json
    _all_values = json.loads("""{
                                  "n_samples":96,
                                  "bindbuf_source_wells":"1-4",
                                  "bead_mix_source_wells":"5",
                                  "vol_source_bb_per_well":15.0,
                                  "vol_source_bead_mix_per_well":2.5,
                                  "p300_mount":"left",
                                  "m300_mount":"right",
                                  "mastermix_tuberack_lname":"opentrons_15_tuberack_falcon_15ml_conical",
                                  "mastermix_mix_rate_multiplier":0.5,
                                  "bb_asp_rate_mult":0.3,
                                  "bb_disp_rate_multipler":0.3,
                                  "bead_asp_rate_mult":1.0,
                                  "bead_disp_rate_multipler":1.0,
                                  "n_mm_mixes":10
                                  }
                                  """)
    return [_all_values[n] for n in names]


def run(ctx: protocol_api.ProtocolContext):

    [n_samples,
     bindbuf_source_wells,
     bead_mix_source_wells,
     vol_source_bb_per_well,
     vol_source_bead_mix_per_well,
     p300_mount,
     m300_mount,
     mastermix_tuberack_lname,
     mastermix_mix_rate_multiplier,
     bb_asp_rate_mult,
     bb_disp_rate_multipler,
     bead_asp_rate_mult,
     bead_disp_rate_multipler,
     n_mm_mixes] = get_values(  # noqa: F821
     "n_samples",
     "bindbuf_source_wells",
     "bead_mix_source_wells",
     "vol_source_bb_per_well",
     "vol_source_bead_mix_per_well",
     "p300_mount",
     "m300_mount",
     "mastermix_tuberack_lname",
     "mastermix_mix_rate_multiplier",
     "bb_asp_rate_mult",
     "bb_disp_rate_multipler",
     "bead_asp_rate_mult",
     "bead_disp_rate_multipler",
     "n_mm_mixes")

    # 1 mL of dead volume is required when using the reservoir,
    # 100 uL for tubes, the dead volume should have the same composition
    # as the rest of the mix
    dead_vol = 100 if mastermix_tuberack_lname is not None else 1000
    bead_dead_vol = 10/265 * dead_vol
    bb_dead_vol = dead_vol - bead_dead_vol

    bind_buf_vol = n_samples*1.5*265
    bead_vol = (10/265) * total_bind_buf_vol
    mm_vol = bind_buf_vol + bead_vol
    # The volume of mastermix in each reservoir well should be 9.65 mL max
    # and also accounting for 1 mL dead volume in the resevoir
    useful_vol_mm_per_well = (9.65-1)*10**3
    n_mm_target_wells = ceil(mm_vol/useful_vol_mm_per_well)
    total_mm_vol = n_mm_target_wells * dead_vol + useful_vol_mm_per_well

    total_bead_vol = total_mm_vol * (10/265)
    total_bb_vol = total_mm_vol - total_bead_vol
    # Add on the dead volume (1 mL of each reagent)

    # If the tuberack isn't set we're going to create the mastermix in the
    # reservoir
    tuberack_slot = '6'
    reservoir_loader = ('nest_12_reservoir_15ml', '10')

    bb_start_index, bb_end_index = parse_range_string(bindbuf_source_wells)
    bead_start_index, bead_end_index = parse_range_string(
        bead_mix_source_wells)

    well_index_post_reagent_well = max(bb_end_index, bead_end_index) + 1

    starting_mm_well_index = \
        (well_index_post_reagent_well if mastermix_tuberack_lname is None
         else 1)

    is_single_pip = True if mastermix_tuberack_lname else False

    # define all custom variables above here with descriptions:

    # load modules

    '''

    Add your modules here with:

    module_name = ctx.load_module('{module_loadname}', '{slot number}')

    Note: if you are loading a thermocycler, you do not need to specify
    a slot number - thermocyclers will always occupy slots 7, 8, 10, and 11.

    For all other modules, you can load them on slots 1, 3, 4, 6, 7, 9, 10.

    '''

    # load labware

    '''

    Add your labware here with:

    labware_name = ctx.load_labware('{loadname}', '{slot number}')

    If loading labware on a module, you can load with:

    labware_name = module_name.load_labware('{loadname}')
    where module_name is defined above.

    '''
    tuberack_mm_target = (
        ctx.load_labware(mastermix_tuberack_lname, tuberack_slot)
        if mastermix_tuberack_lname else None)

    res12 = ctx.load_labware(reservoir_loader[0], reservoir_loader[1])

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
    tiprack_300 = [ctx.load_labware('opentrons_96_tiprack_300ul', '9')]

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
    p300 = ctx.load_instrument(
                              'p300_single_gen2',
                              p300_mount,
                              tip_racks=tiprack_300
                              )

    m300 = ctx.load_instrument(
                              'p300_multi_gen2',
                              m300_mount,
                              tip_racks=tiprack_300
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
        def __init__(self, labware: Labware,
                     well_vol: float = 0,
                     start: int = 1, end: int = 8,
                     mode: str = 'reagent',
                     pip_type: str = 'single',
                     msg: str = 'Refill labware volumes'):
            """
            Voltracker tracks the volume(s) used in a piece of labware

            :param labware: The labware to track
            :param well_vol: The volume of the liquid in the wells, if using a
            multi-pipette with a well plate, treat the plate like a reservoir,
            i.e. start=1, end=1, well_vol = 8 * vol of each individual well.
            :param pip_type: The pipette type used: 'single' or 'multi'
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

        def flash_lights(self):
            """
            Flash the lights of the robot to grab the users attention
            """
            initial_light_state = ctx.rail_lights_on
            opposite_state = not initial_light_state
            for _ in range(5):
                ctx.set_rail_lights(opposite_state)
                ctx.delay(seconds=0.5)
                ctx.set_rail_lights(initial_light_state)
                ctx.delay(seconds=0.5)

        def get_remaining_well_vol(self):
            """
            Return the volume remaining in the current well
            """
            well = next(iter(self.labware_wells))
            return self.labware_wells[well]

        def track(self, vol: float) -> Well:
            """track() will track how much liquid
            was used up per well. If the volume of
            a given well is greater than self.well_vol
            it will remove it from the dictionary and iterate
            to the next well which will act as the reservoir.
            """
            well = next(iter(self.labware_wells))
            # Treat plates like reservoirs and add 8 well volumes together
            vol = vol * 8 if self.pip_type == 'multi' else vol
            if self.labware_wells[well] + vol >= self.well_vol:
                del self.labware_wells[well]
                if len(self.labware_wells) < 1:
                    self.flash_lights()
                    ctx.pause(self.msg)
                    self.labware_wells = self.labware_wells_backup.copy()
                well = next(iter(self.labware_wells))
            self.labware_wells[well] += vol

            if self.mode == 'waste':
                ctx.comment('{}: {} ul of total waste'
                            .format(well, int(self.labware_wells[well])))
            else:
                ctx.comment('{} uL of liquid used from {}'
                            .format(int(self.labware_wells[well]), well))
            return well

    # reagents

    '''
    Define where all reagents are on the deck using the labware defined above.

    e.g.

    water = reservoir12.wells()[-1]
    waste = reservoir.wells()[0]
    samples = plate.rows()[0][0]
    dnase = tuberack.wells_by_name()['A4']

    '''
    # Source wells of binding buffer
    bb_source = VolTracker(res12,
                           vol_source_bb_per_well, bb_start_index,
                           bb_end_index,
                           msg="Refill binding buffer wells",
                           pip_type='single' if is_single_pip else 'multi')

    # Source wells of bead mix
    bead_mix = VolTracker(res12,
                          vol_source_bb_per_well, bb_start_index,
                          bb_end_index,
                          msg="Refill binding buffer wells",
                          pip_type='single' if is_single_pip else 'multi')

    # plate, tube rack maps

    '''
    Define any plate or tube maps here.

    e.g.

    plate_wells_by_row = [well for row in plate.rows() for well in row]

    '''
    mastermix_target = (tuberack_mm_target if tuberack_mm_target
                        is not None else res12)

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
    def pick_up_tip_decorator(tip_pickup_fn, pip, *args, **kwargs):
        try:
            tip_pickup_fn(*args, **kwargs)
        except protocol_api.labware.OutOfTipsError:
            ctx.pause("Replace empty tip racks")
            pip.reset_tipracks()
            pip.pick_up_tip()

    def moving_fractional_dispense(pip,
                                   vol: float,
                                   offsets: Sequence[float],
                                   source: VolTracker,
                                   dest_well: Well):
        pass

    def tube_liq_height(vol, tuberack: Labware):
        """
        Calculates the height of the liquid level in a conical tube
        given its liquid volume.The function tries to account for the conical
        part of the tube
        :param vol: The volume in uL
        :param tuberack: The tuberack with the tubes
        :return value: The height of the liquid level measured from
        the bottom in mm
        """
        tube = tuberack.wells()[0]
        r = tube.diameter/2 - 0.25  # With a fudge factor

        # Cone height approximation
        h_cone_max = 0.171 * tube.depth
        vol_cone_max = (h_cone_max*pi*r**2)/3

        if vol < vol_cone_max:
            h_cone = (3*vol)/(pi*r**2)
            print("h_cone", h_cone)
            return h_cone
        else:
            cylinder_partial_vol = vol - vol_cone_max
            print('cylinder v', cylinder_partial_vol,
                  'cone max vol', vol_cone_max)
            h_partial_tube = cylinder_partial_vol/(pi*r**2)
            print('h cone max', h_cone_max, 'h partial tube', h_partial_tube)
            return h_cone_max + h_partial_tube

    def transfer_reagent(
            source: VolTracker,
            vol: float,
            reagent_name: str,
            target_labware: Labware,
            dest_well_max_vol: float,
            starting_well_index,
            is_pip_single: bool,
            aspiration_rate_multiplier: float,
            dispense_rate_multiplier: float,
            fractional_dispense_offsets: Optional[Sequence[float]] = None):

        ctx.comment("Transferring {} to mastermix wells", format(reagent_name))
        vol_remaining = vol
        # Reverse the list of wells so we can pop off starting at the 1st well
        d_wells = target_labware.wells()[starting_well_index-1:].reverse()
        pip = p300 if is_pip_single else m300
        pip.flow_rate.aspirate *= aspiration_rate_multiplier
        pip.flow_rate.dispense *= dispense_rate_multiplier
        pick_up_tip_decorator(pip.pick_up_tip, pip)
        while vol_remaining > 0:
            d_well = d_wells.pop()
            transfer_vol = (dest_well_max_vol if
                            vol_remaining > dest_well_max_vol
                            else vol_remaining)
            transfer_vol = (transfer_vol/8 if not is_pip_single else
                            transfer_vol)
            if fractional_dispense_offsets is None:
                pip.transfer(transfer_vol, source.track(transfer_vol),
                             d_well, new_tip="never", blow_out=True,
                             blowout_location='destination well')
            else:
                moving_fractional_dispense(pip, transfer_vol,
                                           fractional_dispense_offsets,
                                           source,
                                           d_well)

            vol_remaining -= transfer_vol
        pip.drop_tip()

        # Mastermix creation
        # Step 7-8: Transfer binding buffer
        transfer_reagent(
            bb_source,
            total_bind_buf_vol,
            "Binding Buffer",
            target_labware, dest_well_max_vol,
            starting_well_index, is_pip_single, aspiration_rate_multiplier, dispense_rate_multiplier)
        # Step 9: Mix the bead solution
        # Step 10: Transfer bead solution to target wells
        # Dispense 1/3rd in the center of the well, 1/3rd at the top
        # and 1/3rd at the bottom.
        # and 1/3rd at the bottom.
