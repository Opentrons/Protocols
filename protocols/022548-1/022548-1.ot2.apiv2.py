from opentrons import protocol_api
from opentrons.protocol_api.labware import Labware, Well
import re
from typing import Tuple, Optional, Sequence
from math import ceil, pi
from opentrons.types import Point, Location
import copy

metadata = {
    'protocolName': '022548-2 - DNA extraction: Mastermix creation',
    'author': 'Eskil Andersen <protocols@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.11'   # CHECK IF YOUR API LEVEL HERE IS UP TO DATE
                         # IN SECTION 5.2 OF THE APIV2 "VERSIONING"
}


def parse_range_string(range_string: str) -> Tuple[int, int]:
    """ Parses a range or a single number from the input string.
    the format for a number is n-m, where n and m are any positive integers.
    :param range_string: range string to decode
    :return value: A tuple of the start and end index of the range
    """
    single_num_pattern = re.compile('[0-9]+')
    range_pattern = re.compile('[0-9]+-[0-9]+')
    # Case when there's only one index (e.g. the string decodes to a single
    # well
    if single_num_pattern.fullmatch(range_string) is not None:
        index = int(range_string)
        return index, index
    if range_pattern.fullmatch(range_string):
        # Return both substrings that match numbers (i.e. the start and
        # end indices
        start, end = range_string.split('-')
        return int(start), int(end)
    # If neither regular expression matched then we assume that the string
    # is incorrectly formatted
    raise Exception(("Invalid range string: it was \"{}\" but should be a "
                     "natural number or a range in the format of n-m where n "
                     "and m are natural numbers, "
                     "e.g: 1-4").format(range_string))


def get_values(*names):
    import json
    _all_values = json.loads("""{
                                  "n_samples":96,
                                  "bindbuf_source_well_indices":"1-4",
                                  "bead_mix_source_well_indices":"5",
                                  "vol_source_bb_per_well":15.0,
                                  "vol_source_bead_mix_per_well":2.5,
                                  "p300_mount":"left",
                                  "m300_mount":"right",
                                  "mastermix_tuberack_lname":false,
                                  "mastermix_mix_rate_multiplier":0.5,
                                  "bb_asp_rate_multiplier":0.3,
                                  "bb_disp_rate_multipler":0.3,
                                  "bead_asp_rate_multiplier":1.0,
                                  "bead_disp_rate_multiplier":1.0,
                                  "n_mm_mixes":10,
                                  "tube_edge_offset":4.3,
                                  "resv_well_edge_offset":10,
                                  "is_verbose":true
                                  }
                                  """)
    return [_all_values[n] for n in names]


def run(ctx: protocol_api.ProtocolContext):

    [n_samples,
     bindbuf_source_well_indices,
     bead_mix_source_well_indices,
     vol_source_bb_per_well,
     vol_source_bead_mix_per_well,
     p300_mount,
     m300_mount,
     mastermix_tuberack_lname,
     mastermix_mix_rate_multiplier,
     bb_asp_rate_multiplier,
     bb_disp_rate_multipler,
     bead_asp_rate_multiplier,
     bead_disp_rate_multiplier,
     n_mm_mixes,
     tube_edge_offset,
     resv_well_edge_offset,
     is_verbose] = get_values(  # noqa: F821
     "n_samples",
     "bindbuf_source_well_indices",
     "bead_mix_source_well_indices",
     "vol_source_bb_per_well",
     "vol_source_bead_mix_per_well",
     "p300_mount",
     "m300_mount",
     "mastermix_tuberack_lname",
     "mastermix_mix_rate_multiplier",
     "bb_asp_rate_multiplier",
     "bb_disp_rate_multipler",
     "bead_asp_rate_multiplier",
     "bead_disp_rate_multiplier",
     "n_mm_mixes",
     "tube_edge_offset",
     "resv_well_edge_offset",
     "is_verbose")

    is_debug_mode = True
    # 1 mL of dead volume is required when using the reservoir,
    # 100 uL for tubes, the dead volume should have the same composition
    # as the rest of the mix
    dead_vol = 100 if mastermix_tuberack_lname is not None else 1000

    # Reagent volume not including added dead volume
    bind_buf_vol = n_samples*1.5*265
    bead_vol = (10/265) * bind_buf_vol
    mm_vol = bind_buf_vol + bead_vol

    # The volume of mastermix in each reservoir well should be 9.65 mL max
    # and also accounting for 1 mL dead volume in the resevoir
    # TODO: The reagent source may also be 15 mL tubes, in which case
    # the dead volume should be 100 uL per tube
    max_vol_mm_per_well = 9.65*10**3
    useful_vol_mm_per_well = max_vol_mm_per_well - 1_000
    n_mm_target_wells = ceil(mm_vol/useful_vol_mm_per_well)
    total_mm_vol = n_mm_target_wells * dead_vol + mm_vol

    total_bead_vol = total_mm_vol * (10/265)
    total_bb_vol = total_mm_vol - total_bead_vol

    max_bead_vol_per_well = max_vol_mm_per_well * 10/265
    max_bb_vol_per_well = max_vol_mm_per_well - max_bead_vol_per_well

    # If the tuberack isn't set we're going to create the mastermix in the
    # reservoir
    tuberack_slot = '6'
    reservoir_loader = ('nest_12_reservoir_15ml', '10')

    bb_start_index, bb_end_index = parse_range_string(
        bindbuf_source_well_indices)
    bead_start_index, bead_end_index = parse_range_string(
        bead_mix_source_well_indices)

    well_index_after_reagent_wells = max(bb_end_index, bead_end_index) + 1

    starting_mm_well_index = \
        (well_index_after_reagent_wells if mastermix_tuberack_lname is None
         else 1)

    is_single_pip = True if mastermix_tuberack_lname else False
    # Synonymous conditions
    is_target_tube = is_single_pip

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
                     start: int = 1,
                     end: int = 8,
                     mode: str = 'reagent',
                     pip_type: str = 'single',
                     msg: str = 'Refill labware volumes',
                     reagent_name: str = 'nameless reagent',
                     is_verbose: bool = True,
                     is_strict_mode: bool = False,
                     threshhold_advancement_vol: float = 1):
            """
            Voltracker tracks the volume(s) used in a piece of labware.
            It's conceptually important to understand that in reagent
            mode the volumes tracked are how much volume has been removed from
            the VolTracker, but waste and target is how much has been added
            to it, and how much was there/have been taken out to begin with.
            This will have implications for how the class is initialized.

            :param labware: The labware to track
            :param well_vol: The volume of the liquid in the wells, if using a
            multi-pipette with a well plate, treat the plate like a reservoir,
            i.e. start=1, end=1, well_vol = 8 * vol of each individual well.
            :param pip_type: The pipette type used: 'single' or 'multi',
            when the type is 'multi' volumes are multiplied by 8 to reflect
            the true volumes used by the pipette.
            :param mode: 'reagent', 'target' or 'waste'
            :param start: The starting well
            :param end: The ending well
            :param msg: Message to send to the user when all wells are empty
            (or full when in waste mode)
            :param reagent_name: Name of the reagent tracked by the object
            :param is_verbose: Whether to have VolTracker send ProtocolContext
            messages about its actions or not.
            :param is_strict_mode: If set to True VolTracker will pause
            execution when its tracked wells are depleted (or filled), ask the
            user to replace the labware and reset the volumes. If it's False
            VolTracker will raise an exception if trying to use more volume
            than the VolTracker is set up for. strict_mode also forces the
            user to check if there's enough volume in the active well and
            to manually advance to the next well by calling advance_well()
            :param threshhold_advancement_vol: If using strict mode VolTr.
            will throw an exception if the user advances the well while there
            is more than the threshhold_advancement_vol of volume left in
            the well.
            """
            # Boolean value: True if the well has been filled
            # or has been depleted
            self.labware_wells = {}
            for well in labware.wells()[start-1:end]:
                self.labware_wells[well] = [0, False]
            self.labware_wells_backup = self.labware_wells.copy()
            self.well_vol = well_vol
            self.pip_type = pip_type
            self.mode = mode
            self.start = start
            self.end = end
            self.msg = msg
            self.is_verbose = is_verbose
            # Total vol changed - how much volume has been withdrawn or added
            # to this Voltracker
            self.total_vol_changed = 0
            # If true, then labware should raise an exception when full
            # rather than reset
            self.is_strict_mode = is_strict_mode
            self.reagent_name = reagent_name

            valid_modes = ['reagent', 'waste', 'target']

            # Parameter error checking
            if not (pip_type == 'single' or pip_type == 'multi'):
                raise Exception('Pipette type must be single or multi')

            if mode not in valid_modes:
                msg = "Invalid mode, valid modes are {}"
                msg = msg.format(valid_modes)
                raise Exception(msg)

        def __str__(self):
            msg = (self.reagent_name + " " + self.mode
                   + " volume change: " + str(self.total_vol_changed))
            msg += "\nChanges in each well:\n"
            for i, well_tracker in enumerate(self.labware_wells.values()):
                msg += "well {}: Volume change: {}\n".format(
                    i+1, well_tracker[0])
            return msg

        @staticmethod
        def flash_lights():
            """
            Flash the lights of the robot to grab the users attention
            """
            nonlocal ctx
            initial_light_state = ctx.rail_lights_on
            opposite_state = not initial_light_state
            for _ in range(5):
                ctx.set_rail_lights(opposite_state)
                ctx.delay(seconds=0.5)
                ctx.set_rail_lights(initial_light_state)
                ctx.delay(seconds=0.5)

        def get_wells(self) -> Sequence:
            return list(self.labware_wells.keys())

        def to_list(self):
            return list(self.labware_wells.items())

        def get_total_initial_vol(self):
            # Return the total initial vol = n_wells * well_vol
            return len(self.labware_wells) * self.well_vol

        def get_total_remaining_vol(self):
            return self.get_total_initial_vol() - self.total_vol_changed

        def get_active_well_vol_change(self):
            """
            Return the volume either used up (reagents) or added
            (target or trash) in the currently active well
            """
            well = self.get_active_well()
            return self.labware_wells[well][0]

        def get_active_well_remaining_vol(self):
            """
            Returns how much volume is remaing to be used (reagents) or the
            space left to fill the well (waste and targets)
            """
            vol_change = self.get_active_well_vol_change()
            return self.well_vol - vol_change

        def get_active_well(self):
            for key in self.labware_wells:
                # Return the first well that is not full
                if self.labware_wells[key][1] is False:
                    return key

        def advance_well(self):
            curr_well = self.get_active_well()
            # Mark the current well as 'used up'
            self.labware_wells[curr_well][1] = True
            pass

        def reset_labware(self):
            VolTracker.flash_lights()
            ctx.pause(self.msg)
            self.labware_wells = self.labware_wells_backup.copy()

        def get_active_well_vol(self):
            well = self.get_active_well()
            return self.labware_wells[well][0]

        def get_current_vol_by_key(self, well_key):
            vol_diff = self.labware_wells[well_key][0]
            if self.mode == 'reagent':
                # Subtractive volumes (reagents) starts aat well_vol and
                # decreases by vol_diff
                return self.well_vol - vol_diff
            else:
                # Additive volumes i.e. targets and waste that start at 0
                return vol_diff

        def track(self, vol: float) -> Well:
            """track() will track how much liquid
            was used up per well. If the volume of
            a given well is greater than self.well_vol
            it will remove it from the dictionary and iterate
            to the next well which will act as the active source well.
            :param vol: How much volume to track (per tip), i.e. if it's one
            tip track vol, but if it's multi-pipette, track 8 * vol.

            This implies that VolTracker will treat a column like a well,
            whether it's a plate or a reservoir.
            """
            well = self.get_active_well()
            # Treat plates like reservoirs and add 8 well volumes together
            # Total vol changed keeps track across labware resets, i.e.
            # when the user replaces filled/emptied wells
            vol = vol * 8 if self.pip_type == 'multi' else vol

            # Track the total change in volume of this volume tracker
            self.total_vol_changed += vol

            if self.labware_wells[well][0] + vol > self.well_vol:
                if self.is_strict_mode:
                    msg = ("Tracking a volume of {} uL would {} the "
                           "current well: {} on the {} {} tracker. "
                           "The max well volume is {}, and "
                           "the current vol is {}")
                    mode_msg = ("over-deplete`" if self.mode == "reagent"
                                else "over-fill")
                    msg = msg.format(
                        vol, mode_msg, well, self.reagent_name, self.mode,
                        self.well_vol, self.get_active_well_vol())
                    raise Exception(msg)
                self.labware_wells[well][1] = True
                is_all_used = True

                # Check if wells are completely full (or depleted)
                for w in self.labware_wells:
                    if self.labware_wells[w][1] is False:
                        is_all_used = False

                if is_all_used is True:
                    if self.is_strict_mode is False:
                        self.reset_labware()
                    else:
                        e_msg = "{}: {} {} wells would be {} by this action"
                        fill_status = \
                            ("over-depleted" if self.mode == "reagent" else
                             "over-filled")
                        e_msg = e_msg.format(str(self),
                                             self.reagent,
                                             self.mode, fill_status)
                        raise Exception(e_msg)

                well = self.get_active_well()
                if self.is_verbose:
                    ctx.comment(
                        "\n{} {} tracker switching to well {}\n".format(
                            self.reagent_name, self.mode, well))
            self.labware_wells[well][0] += vol

            if self.is_verbose:
                if self.mode == 'waste':
                    ctx.comment('{}: {} ul of total waste'
                                .format(well,
                                        int(self.labware_wells[well][0])))
                elif self.mode == 'target':
                    ctx.comment('{}: {} ul of reagent added to target well'
                                .format(well,
                                        int(self.labware_wells[well][0])))
                else:
                    ctx.comment('{} uL of liquid used from {}'
                                .format(int(self.labware_wells[well][0]),
                                        well))
            return well

    def is_15ml_tube(well: Well):
        name = str(well).lower()
        if "tube" not in name or "15" not in name:
            return False
        return True

    def pick_up_tip_decorator(tip_pickup_fn, pip, *args, **kwargs):
        try:
            tip_pickup_fn(*args, **kwargs)
        except protocol_api.labware.OutOfTipsError:
            ctx.pause("Replace empty tip racks")
            pip.reset_tipracks()
            pip.pick_up_tip()

    def moving_fractional_dispense(pip,
                                   vol: float,
                                   liq_height: float,
                                   y_offsets: Sequence[float],
                                   dest_location: Location):
        """
        This function moves to the offsets from the center of the well in the
        y-direction and dispenses a fractional amount based on the length of
        the offset sequence.
        :param pip: Pipette to dispense with
        :param vol: The volume to dispense
        :param offsets: A tuple of offsets from the center of the dest_well
        to do fractional dispenses at
        :param dest_location: The location to dispense at
        """
        nonlocal is_verbose, ctx
        fractional_vol = vol/len(y_offsets)
        for offset in y_offsets:
            offset_point = Point(0, offset, 0)
            disp_loc = dest_location.move(offset_point)
            if is_verbose:
                ctx.comment("Dispensing at {}".format(str(disp_loc)))
            pip.dispense(fractional_vol, disp_loc)

    def tube_15ml_cone_height(tube: Well):
        """
        :return value: Approximate height of the tube cone
        """

        if not is_15ml_tube(tube):
            msg = ("The input well parameter: {}, does not appear to "
                   "be a 15 mL tube")
            msg.format(tube)
            raise Exception(msg)
        return 0.171 * tube.depth

    def tube_liq_height(vol, tube: Well, is_min_cone_height: bool = True):
        """
        Calculates the height of the liquid level in a conical tube
        given its liquid volume.The function tries to account for the conical
        part of the tube
        :param vol: The volume in uL
        :param tuberack: The tuberack with the tubes
        :param is_min_cone_height: Always return the height of the cone at
        minimum
        :return value: The height of the liquid level measured from
        the bottom in mm
        """

        if not is_15ml_tube(tube):
            msg = ("The input well parameter: {}, does not appear to "
                   "be a 15 mL tube")
            msg.format(tube)
            raise Exception(msg)

        r = tube.diameter/2
        # Fudge factor - height seems too low given a volume, so bump it up
        # a little bit by "decreasing" the radius
        r *= 0.94

        # Cone height approximation
        h_cone_max = tube_15ml_cone_height(tube)
        vol_cone_max = (h_cone_max*pi*r**2)/3

        if vol < vol_cone_max:
            h_cone = (3*vol)/(pi*r**2)
            # print("h_cone", h_cone)
            if is_min_cone_height:
                return h_cone_max
            return h_cone
        else:
            cylinder_partial_vol = vol - vol_cone_max
            # print('cylinder v', cylinder_partial_vol,
            # 'cone max vol', vol_cone_max)
            h_partial_tube = cylinder_partial_vol/(pi*r**2)
            # print('h cone max', h_cone_max, 'h partial tube', h_partial_tube)
            return h_cone_max + h_partial_tube

    def transfer_reagent(
            source: VolTracker,
            vol: float,
            reagent_name: str,
            target: VolTracker,
            starting_well_index: int,
            is_pip_single: bool,
            aspiration_rate_multiplier: float,
            dispense_rate_multiplier: float,
            fractional_dispense_y_offsets: Optional[Sequence[float]] = None,
            new_tip: bool = True,
            is_verbose: bool = True,
            ):

        nonlocal ctx
        msg = "Transferring {} to mastermix {}"
        target_string = "15 mL tubes" if is_pip_single else "reservoir wells"
        msg = msg.format(reagent_name, target_string)
        ctx.comment(msg)

        vol_remaining = vol
        pip = p300 if is_pip_single else m300

        # flow rates are floats, so they will copy by value
        fr_copy = (pip.flow_rate.aspirate, pip.flow_rate.dispense)
        pip.flow_rate.aspirate *= aspiration_rate_multiplier
        pip.flow_rate.dispense *= dispense_rate_multiplier
        if new_tip:
            if pip.has_tip:
                pip.drop_tip()
            pick_up_tip_decorator(pip.pick_up_tip, pip)
        # Loop over each target well filling it up to its maximal volume
        # or less
        while vol_remaining > 0:
            # Either fill up a target well completely and move on to the next
            # target well
            # or fill it up to some volume less than it's maximal volume
            # and end the transfer (i.e. that well would be the final target
            # by virtue of being able to contain the entire remaining volume)
            # Subtract the transfer_vol at the end of the while loop
            # from vol_remaining

            # Calculate aspiration and dispensing offsets for/if tubes.
            # = 0.1 for reservoirs, and not recalculated.
            source_liq_height = 0.1
            target_liq_height = \
                (10 if fractional_dispense_y_offsets is not None else 0.1)
            # and dispense a fractional volume
            # Fractionate the volume transfer into discrete pipette
            # aspirate/dispense steps
            aspiration_vol = 0
            source_volume = source.get_active_well_vol_change()
            target_volume = target.get_active_well_vol_change()

            # Advance to the next well on source and tracker if they
            # are full/depleted.
            for tracker in [source, target]:
                if tracker.get_active_well_remaining_vol() <= 1:
                    tracker.advance_well()
            if is_pip_single:
                aspiration_vol = min(
                    vol_remaining, pip.max_volume,
                    source.get_active_well_remaining_vol()-1,
                    target.get_active_well_remaining_vol()-1)
                # If we're doing dispenses with offsets we should be
                # above the cone height so we don't bump the tube with
                # the tip
                is_cone_min_offset = (True if fractional_dispense_y_offsets
                                      is not None else False)
                target_liq_height = tube_liq_height(
                    target_volume, target.get_active_well(),
                    is_cone_min_offset)
                # Make sure we don't bang into the bottom of the tube
                target_liq_height = max(target_liq_height, 0.1)
                source_liq_height = tube_liq_height(
                    source_volume, source.get_active_well(),
                    False)
                # Make sure we're dipping below the surface for aspirations
                # without hitting the bottom
                source_liq_height = max(source_liq_height-10, 0.1)
                if is_verbose:
                    msg = ("Aspirating from the source tube with a {} "
                           "mm offset from the bottom")
                    msg = msg.format(source_liq_height)
                    ctx.comment(msg)

                    msg = ("Dispensing into the target tube with a {} "
                           "mm offset from the bottom")
                    msg = msg.format(target_liq_height)
                    ctx.comment(msg)
            else:
                # If we are using a reservoir/multi-channel:
                # Aspiration volume should be either
                # the max volume of the pipette, or any other
                # volume (remaining volume, source well volume,
                # remaining target well volume) divided by 8
                # Aspiration/dispensing z-offsets kept constant at 0.1 mm
                aspiration_vol = min(
                    vol_remaining/8, pip.max_volume,
                    (source.get_active_well_remaining_vol()-1)/8,
                    (target.get_active_well_remaining_vol()-1)/8)

            d_loc = target.track(
                aspiration_vol).bottom(target_liq_height)
            s_loc = source.track(
                aspiration_vol).bottom(source_liq_height)

            pip.aspirate(aspiration_vol,
                         s_loc)

            if fractional_dispense_y_offsets is not None:
                moving_fractional_dispense(
                    pip, aspiration_vol, target_liq_height,
                    fractional_dispense_y_offsets,
                    d_loc)
            else:
                pip.dispense(aspiration_vol, d_loc)

            subtraction_vol = (aspiration_vol if is_single_pip is True else
                               aspiration_vol * 8)
            vol_remaining -= subtraction_vol
        pip.drop_tip()
        # Reset flow rates
        pip.flow_rate.aspirate, pip.flow_rate.dispense = fr_copy
    # reagents

    '''
    Define where all reagents are on the deck using the labware defined above.

    e.g.

    water = reservoir12.wells()[-1]
    waste = reservoir.wells()[0]
    samples = plate.rows()[0][0]
    dnase = tuberack.wells_by_name()['A4']

    '''
    mastermix_target = (tuberack_mm_target if is_target_tube else res12)

    y_offsets = []
    target_well_type = mastermix_target.wells()[0]
    # If the mastermix target is a tuberack, the reagent sources are also tubes
    # for tube targets
    y_offsets.append(0)  # Always start in the center of the well
    if target_well_type.diameter is not None:
        pos_offset = target_well_type.diameter/2-tube_edge_offset
        pos_offset = pos_offset if pos_offset > 0 else 0
        neg_offset = -pos_offset
        y_offsets.append(pos_offset)
        y_offsets.append(neg_offset)
    # Reservoir target
    elif target_well_type.width is not None:
        resv_well_width = target_well_type.width/8
        pos_offset = resv_well_width/2 - resv_well_edge_offset
        neg_offset = -pos_offset
        y_offsets.append(pos_offset)
        y_offsets.append(neg_offset)
    # Error?
    else:
        msg = "The well {} does not have a diameter or width/length"
        msg.format(target_well_type)
        raise Exception(msg)

    ml_multiplier = 10**3
    # Source wells of binding buffer
    source_labware = tuberack_mm_target if is_target_tube else res12
    bb_source = VolTracker(
        labware=source_labware,
        well_vol=vol_source_bb_per_well*ml_multiplier,
        start=bb_start_index,
        end=bb_end_index,
        mode='reagent',
        msg="Refill binding buffer wells",
        reagent_name='Binding buffer',
        pip_type='single' if is_single_pip else 'multi',
        is_verbose=is_verbose,
        is_strict_mode=True)

    bb_source_init = copy.deepcopy(bb_source)

    # Source wells of bead mix
    bead_mix_source = VolTracker(
        labware=source_labware,
        well_vol=vol_source_bead_mix_per_well*ml_multiplier,
        start=bead_start_index,
        end=bead_end_index,
        mode='reagent',
        msg="Refill binding buffer wells",
        reagent_name='Bead mix',
        pip_type='single' if is_single_pip else 'multi',
        is_verbose=is_verbose,
        is_strict_mode=True)

    bead_mix_source_init = copy.deepcopy(bead_mix_source)

    bb_target = VolTracker(
        labware=mastermix_target,
        # Add one uL for margin of error in any float rounding
        well_vol=max_bb_vol_per_well+1,
        start=well_index_after_reagent_wells,
        end=well_index_after_reagent_wells + n_mm_target_wells,
        mode='target',
        # Should not happen, but:
        msg="All mastermix target wells/tubes are full, please replace them",
        reagent_name='Binding buffer',
        pip_type='single' if is_single_pip else 'multi',
        is_verbose=is_verbose,
        is_strict_mode=True
        )

    bb_target_init = copy.deepcopy(bb_target)

    bead_mix_target = VolTracker(
        labware=mastermix_target,
        well_vol=max_bead_vol_per_well,
        # Same target wells as for the binding buffer
        start=well_index_after_reagent_wells,
        end=well_index_after_reagent_wells + n_mm_target_wells,
        mode='target',
        # Should not happen, but:
        msg="All mastermix target wells/tubes are full, please replace them",
        reagent_name='Bead mix',
        pip_type='single' if is_single_pip else 'multi',
        is_verbose=is_verbose,
        is_strict_mode=True
    )
    bead_mix_target_init = copy.deepcopy(bead_mix_target)

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

    # Mastermix creation
    # Step 7-8: Transfer binding buffer
    transfer_reagent(
        source=bb_source,
        vol=total_bb_vol,
        reagent_name="Binding Buffer",
        target=bb_target,
        starting_well_index=starting_mm_well_index,
        is_pip_single=is_single_pip,
        aspiration_rate_multiplier=bb_asp_rate_multiplier,
        dispense_rate_multiplier=bb_disp_rate_multipler)
    # # Step 9: Mix the bead solutions in the reservoir
    pip = p300 if is_target_tube else m300
    bead_wells = bead_mix_source.get_wells()

    pick_up_tip_decorator(pip.pick_up_tip, pip)
    for well in bead_wells:
        z_offset = 0.1
        if is_target_tube:
            well_vol = bead_mix_source.get_current_vol_by_key(well)
            height = tube_liq_height(well_vol, well, False)
            z_offset = max(0.1, height-10)
            pass
        pip.mix(10, pip.max_volume, well.bottom(z_offset))
        if is_verbose:
            msg = "Mixing bead mix source at a z-offset of {}"
            msg = msg.format(z_offset)
            ctx.comment(msg)
        pip.blow_out(well)
        pip.touch_tip(well)

    # # Step 10: Transfer bead solution to target wells
    # Dispense 1/3rd in the center of the well, 1/3rd at the top
    # and 1/3rd at the bottom.

    transfer_reagent(
        source=bead_mix_source,
        vol=total_bead_vol,
        reagent_name="Bead Mix",
        target=bead_mix_target,
        starting_well_index=starting_mm_well_index,
        is_pip_single=is_single_pip,
        aspiration_rate_multiplier=bead_asp_rate_multiplier,
        dispense_rate_multiplier=bead_disp_rate_multiplier,
        fractional_dispense_y_offsets=y_offsets,
        new_tip=False)

    # Mix the mastermix
    pip = p300 if is_target_tube else m300
    if pip.has_tip:
        pip.drop_tip()
    pip.pick_up_tip()

    bb_target_tracker_list = bb_target.to_list()
    bead_target_tracker_list = bead_mix_target.to_list()

    if n_mm_mixes > 0:
        ctx.comment("\nMixing the mastermix\n")
        n_tips = 1 if is_target_tube else 8
        for bb, bead in zip(bb_target_tracker_list, bead_target_tracker_list):
            msg = "The target wells should be the same for both reagents"
            assert bb[0] == bead[0], msg
            mixing_well = bb[0]
            if bb[1][0] + bead[1][0] < 1:
                break
            mix_vol = min(bb[1][0] + bead[1][0], pip.max_volume*n_tips)
            mix_vol = mix_vol/n_tips
            pip.mix(n_mm_mixes, mix_vol, mixing_well,
                    mastermix_mix_rate_multiplier)

    if is_debug_mode:
        # Error check our results - accept a mean of 1 uL error per well
        bb_target_diff = abs(
            total_bb_vol - bb_target.total_vol_changed)
        bead_mix_target_diff = abs(
            total_bead_vol - bead_mix_target.total_vol_changed)
        # Add volumes here since they should be negative (i.e. consumed)
        bb_source_diff = abs(
            total_bb_vol - bb_source.total_vol_changed)
        bead_mix_source_diff = abs(
            total_bead_vol - bead_mix_source.total_vol_changed)
        vol_err_template = ("The difference between stated and transferred {} "
                            "vol was too great: {}")

        for diff, name in zip([bb_target_diff,
                               bead_mix_target_diff,
                               bb_source_diff,
                               bead_mix_source_diff],
                              ["binding buffer target",
                               "bead mix target",
                               "binding buffer source",
                               ]):
            msg = vol_err_template.format(name, diff)
            # Accept 1 uL abs mean difference per well
            try:
                assert diff < n_mm_target_wells, msg
            except AssertionError as e:
                ctx.comment(
                    ("Assertion error comparing volumes transferred to stated "
                     "volumes transferred "))
                ctx.comment(str(e))
                ctx.comment("\n" + str(bb_source) + str(bead_mix_source)
                            + str(bb_target) + str(bead_mix_target) + "\n")

        # Print info about the volume trackers
        ctx.comment("\n\nVolTrackers before transfer")
        for vt in [bb_source_init, bead_mix_source_init,
                   bb_target_init, bead_mix_target_init]:
            ctx.comment(str(vt))
        ctx.comment("\n\nVolTrackers after transfer")
        for vt in [bb_source, bead_mix_source,
                   bb_target, bead_mix_target]:
            ctx.comment(str(vt))
            ctx.comment("Volume change:" + str(vt.total_vol_changed))

    ctx.comment("\n\n - Protocol finished! - \n")
