from opentrons import protocol_api
from opentrons.protocol_api.labware import Labware
from opentrons.protocol_api.labware import Well
from typing import List, Sequence

# The first part of this protocol mixes the DNA samples with end repair
# buffer and enzyme and ends when the samples are ready for thermal incubation
metadata = {
    'protocolName': '466f93-6 - Mastermix creation protocol',
    'author': 'Eskil Andersen <eskil.andersen@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.11'   # CHECK IF YOUR API LEVEL HERE IS UP TO DATE
                         # IN SECTION 5.2 OF THE APIV2 "VERSIONING"
}


def run(ctx: protocol_api.ProtocolContext):

    [n_samples,
     n_over_reactions,
     aspiration_rate_multiplier,
     dispensing_rate_multiplier,
     mixing_rate_multiplier,
     n_mixes,
     pip_left_lname,
     is_filtered_left,
     pip_right_lname,
     is_filtered_right,
     is_create_end_repair_mm,
     is_create_adaptor_ligation_mm,
     is_create_pcr_mm,
     mastermix_target_lname,
     is_verbose_mode] = get_values(  # noqa: F821
     "n_samples",
     "n_over_reactions",
     "aspiration_rate_multiplier",
     "dispensing_rate_multiplier",
     "mixing_rate_multiplier",
     "n_mixes",
     "pip_left_lname",
     "is_filtered_left",
     "pip_right_lname",
     "is_filtered_right",
     "is_create_end_repair_mm",
     "is_create_adaptor_ligation_mm",
     "is_create_pcr_mm",
     "mastermix_target_lname",
     "is_verbose_mode")

    # General error checking
    if not pip_left_lname and not pip_right_lname:
        raise Exception("You must load at least one pipette")

    is_any_mm = False
    for is_mm in [is_create_end_repair_mm, is_create_adaptor_ligation_mm,
                  is_create_pcr_mm]:
        if is_mm:
            is_any_mm = True
            break

    if not is_any_mm:
        raise Exception("You have to create at least one mastermix")

    # define all custom variables above here with descriptions:
    # Source volumes of reagents, and number of wells containing the reagent
    # 1st mastermix: End repair
    ERB_vol_per_well = 27
    ERE_vol_per_well = 126

    n_ERB_wells = 8
    n_ERE_wells = 1

    total_ERB_vol = n_ERB_wells * ERB_vol_per_well
    total_ERE_vol = ERE_vol_per_well * n_ERE_wells
    # How much volume of reagents are used per sample
    ERB_vol_per_sample = 1.5
    ERE_vol_per_sample = 0.75
    # 225 uL per 100 samples
    max_ERB_samples = total_ERB_vol // ERB_vol_per_sample
    max_ERE_samples = total_ERE_vol // ERE_vol_per_sample
    ER_mm_vol_per_sample = ERB_vol_per_sample + ERE_vol_per_sample
    max_ER_mm_samples = min(max_ERB_samples, max_ERE_samples)
    # Well numbers
    ERB_start_index = 1
    ERB_end_index = ERB_start_index + n_ERB_wells - 1
    ERE_start_index = 9
    ERE_end_index = ERE_start_index + n_ERE_wells - 1

    # Required volumes for creating the mastermix
    total_ERE_mm_vol = n_samples * ERE_vol_per_sample
    total_ERB_mm_vol = n_samples * ERB_vol_per_sample
    total_ER_mm_vol = ER_mm_vol_per_sample * \
        n_samples if is_create_end_repair_mm else 0

    # Error checking
    if is_create_end_repair_mm and n_samples > max_ER_mm_samples:
        raise Exception(
            "You are trying to create {} aliquots of end-repair "
            "mastermix, but there is only enough reagent on the Yourgene "
            "reagent plate 1 for {} mastermix aliquots"
            .format(n_samples, int(max_ER_mm_samples)))

    # 2nd mastermix: Adaptor ligation
    ALB_vol_per_well = 45
    ALE_I_vol_per_well = 27
    ALE_II_vol_per_well = 39

    n_ALB_wells = 8
    n_ALE_I_wells = 8
    n_ALE_II_wells = 1

    ALB_start_index = 8*2+1
    ALB_end_index = ALB_start_index + n_ALB_wells - 1
    ALE_I_start_index = 8*3+1
    ALE_I_end_index = ALE_I_start_index + n_ALE_I_wells - 1
    ALE_II_start_index = 8*4+1
    ALE_II_end_index = ALE_II_start_index + n_ALE_II_wells - 1

    total_ALB_vol = ALB_vol_per_well * n_ALB_wells
    total_ALE_I_vol = ALE_I_vol_per_well * n_ALE_I_wells
    total_ALE_II_vol = ALE_II_vol_per_well * n_ALE_II_wells

    ALB_vol_per_sample = 2.50
    ALE_I_vol_per_sample = 1.50
    ALE_II_vol_per_sample = 0.25

    total_ALB_mm_vol = ALB_vol_per_sample * n_samples
    total_ALE_I_mm_vol = ALE_I_vol_per_sample * n_samples
    total_ALE_II_mm_vol = ALE_II_vol_per_sample * n_samples

    max_ALB_samples = total_ALB_vol // ALB_vol_per_sample
    max_ALE_I_samples = total_ALE_I_vol // ALE_I_vol_per_sample
    max_ALE_II_samples = total_ALE_II_vol // ALE_II_vol_per_sample
    max_AL_mm_samples = min(
        max_ALB_samples, max_ALE_I_samples, max_ALE_II_samples)

    # Error checking
    if is_create_adaptor_ligation_mm and n_samples > max_AL_mm_samples:
        raise Exception(
            ("You are trying to create {} aliquots of Adaptor-Ligation "
             "mastermix, but there is only enough reagent on the Yourgene "
             "reagent plate 1 for {} mastermix aliquots, designate fewer "
             "samples per run, and re-run the protocol as many times are "
             "needed")
            .format(n_samples, int(max_AL_mm_samples)))

    total_AL_mm_vol_per_sample = (ALB_vol_per_sample + ALE_I_vol_per_sample
                                  + ALE_II_vol_per_sample)
    total_AL_mm_vol = total_AL_mm_vol_per_sample * \
        n_samples if is_create_adaptor_ligation_mm else 0

    # 3rd mastermix: PCR mix + primers
    PCR_mix_vol_per_well = 117
    primer_vol_per_well = 45

    n_PCR_mix_wells = 16
    n_primer_wells = 2

    PCR_mix_start_index = 8*10+1
    PCR_mix_end_index = PCR_mix_start_index + n_PCR_mix_wells - 1
    primer_start_index = 8*9+1
    primer_end_index = primer_start_index + n_primer_wells-1

    # Total volume of reagents in all reagent wells
    total_PCR_mix_vol = PCR_mix_vol_per_well * n_PCR_mix_wells
    total_primer_vol = primer_vol_per_well * n_primer_wells

    PCR_mix_vol_per_sample = 2.50
    primer_vol_per_sample = 1.50
    PCR_mm_vol_per_sample = PCR_mix_vol_per_sample + primer_vol_per_sample

    max_PCR_mix_samples = total_PCR_mix_vol // PCR_mix_vol_per_sample
    max_primer_samples = total_primer_vol // primer_vol_per_sample
    max_PCR_mm_samples = min(max_PCR_mix_samples, max_primer_samples)
    total_PCR_mm_vol = (PCR_mm_vol_per_sample * n_samples if is_create_pcr_mm
                        else 0)
    # Total volumes to transfer to make mastermix
    totaL_PCR_mix_mm_vol = PCR_mix_vol_per_sample * n_samples
    total_primer_mm_vol = primer_vol_per_sample * n_samples

    # Error checking
    if is_create_pcr_mm and n_samples > max_PCR_mm_samples:
        raise Exception(
            "You are trying to create {} aliquots of PCR "
            "mastermix, but there is only enough reagent on the Yourgene "
            "reagent plate 1 for {} mastermix aliquots"
            .format(n_samples, int(max_PCR_mm_samples)))

    source_well_plate_lname = 'azenta_96_wellplate_200ul'

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
    # 3 custom plates (waiting for specifications) - these will be NEST
    # I think these can be swapped sequentailly
    # 96 well PCR plates for now
    # 1 DNA sample plate
    # 3? target plates
    # Reservoir for 80 % ethanol, e.g. a tube rack with a falcon tube

    yourgene_reagent_plate_I\
        = ctx.load_labware(source_well_plate_lname, '7',
                           'Yourgene Reagent plate - 1')
    tuberack = ctx.load_labware(mastermix_target_lname, '4',
                                'Mastermix target tuberack')

    # Error check that the tubes are large enough to hold mastermix volumes
    largest_mm_vol = max(total_ER_mm_vol, total_AL_mm_vol, total_PCR_mm_vol)
    if largest_mm_vol > tuberack.wells()[0].max_volume:
        raise Exception(("One of your mastermixes requires a final volume of "
                         "{}, but your tubes can only handle a maximal volume "
                         "of {} uL")
                        .format(largest_mm_vol,
                                tuberack.wells()[0].max_volume))

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

    def load_tipracks(filtered_tips_lname: str, non_filtered_tips_lname: str,
                      is_filtered: bool, slots: list) -> list:
        tiprack_list = []
        for slot in slots:
            tip_type = filtered_tips_lname if is_filtered \
                else non_filtered_tips_lname
            tiprack_list.append(ctx.load_labware(tip_type, slot))
        return tiprack_list

    def process_tipracks(pip_lname, is_filtered, slots) -> list:
        tiprack_lnames = {
            "p20s_filtered": "opentrons_96_filtertiprack_20ul",
            "p20s_nonfiltered": "opentrons_96_tiprack_20ul",
            "p300s_filtered": "opentrons_96_filtertiprack_200ul",
            "p300s_nonfiltered": "opentrons_96_tiprack_300ul",
            "p1000s_filtered": "opentrons_96_filtertiprack_1000ul",
            "p1000s_nonfiltered": "opentrons_96_tiprack_1000ul"
        }

        tiprack_list = []
        if "20_" in pip_lname or "10_" in pip_lname:
            tiprack_list = load_tipracks(tiprack_lnames["p20s_filtered"],
                                         tiprack_lnames["p20s_nonfiltered"],
                                         is_filtered,
                                         slots)
        elif "300_" in pip_lname or "50_" in pip_lname:
            tiprack_list = load_tipracks(tiprack_lnames["p300s_filtered"],
                                         tiprack_lnames["p300s_nonfiltered"],
                                         is_filtered,
                                         slots)
        elif "1000_" in pip_lname:
            tiprack_list = load_tipracks(tiprack_lnames["p1000s_filtered"],
                                         tiprack_lnames["p1000s_nonfiltered"],
                                         is_filtered,
                                         slots)
        else:
            raise Exception("The pipette loadname does not match any tipracks "
                            "the loadname was {}".format(pip_lname))
        return tiprack_list

    tipracks_left_pip = None
    tipracks_right_pip = None
    if pip_left_lname:
        tipracks_left_pip = process_tipracks(pip_left_lname, is_filtered_left,
                                             ['5'])
    if pip_right_lname:
        tipracks_right_pip = process_tipracks(pip_right_lname,
                                              is_filtered_right, ['8'])
    print("left tiprack {}, right tiprack {}".format(tipracks_left_pip,
                                                     tipracks_right_pip))

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
    # Load left and right pipettes
    pip_left = None
    pip_right = None
    if pip_left_lname:
        pip_left = ctx.load_instrument(pip_left_lname, "left",
                                       tip_racks=tipracks_left_pip)
    if pip_right_lname:
        pip_right = ctx.load_instrument(pip_right_lname, "right",
                                        tip_racks=tipracks_right_pip)
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
    def drop_all_tips(pipettes: list):
        '''
        Drops the pipette tips of all the tips in pipettes if the are
        currently carrying them
        :param pipettes: list of pipettes
        '''
        for pip in pipettes:
            if pip.has_tip:
                pip.drop_tip()

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
                     is_strict_mode: bool = False):
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
            """
            # Boolean value: True if the well is full or has been depleted
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
            return (self.reagent_name + " " + self.mode
                    + " " + str(self.labware_wells)
                    + "volume change: " + str(self.total_vol_changed))

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

        def get_total_initial_vol(self):
            # Return the total initial vol = n_wells * well_vol
            if self.mode == 'reagent':
                return len(self.labware_wells) * self.well_vol
            else:
                # Always considered 0 initially for targets and waste trackers
                return 0

        def get_total_remaining_vol(self):
            # TODO: Return the total initial volume minus used/added volume
            return self.get_total_initial_vol() + self.total_vol_changed

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
            if self.mode == 'reagent':
                self.total_vol_changed -= vol
            else:
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

    def rank_pipettes(pipettes: list):
        '''
        Given a list of 2 pipettes (Where either may be None) this fn will
        return them in the order of smallest to largest. This function assumes
        that error checking for
        cases where no pipettes were loaded was already done.
        '''
        if pipettes[1] is None:
            return [pipettes[0], pipettes[0]]
        elif pipettes[0] is None:
            return [pipettes[1], pipettes[1]]
        elif len(pipettes) == 2:
            if pipettes[0].max_volume <= pipettes[1].max_volume:
                return [pipettes[0], pipettes[1]]
            else:
                return [pipettes[1], pipettes[0]]
        else:
            raise Exception("Unexpected number of pipettes loaded: {}".
                            format(len(pipettes)))
    # reagents

    '''
    Define where all reagents are on the deck using the labware defined above.

    e.g.

    water = reservoir12.wells()[-1]
    waste = reservoir.wells()[0]
    samples = plate.rows()[0][0]
    dnase = tuberack.wells_by_name()['A4']

    '''

    # Reagent wells for mastermix 1: End-repair
    ERB_wells = VolTracker(labware=yourgene_reagent_plate_I,
                           well_vol=ERB_vol_per_well,
                           start=ERB_start_index,
                           end=ERB_end_index,
                           msg=("Out of End-repair buffer, please replace "
                                "reagent plate"),
                           reagent_name="End repair buffer",
                           is_verbose=is_verbose_mode,
                           is_strict_mode=True)
    ERE_wells = VolTracker(labware=yourgene_reagent_plate_I,
                           well_vol=ERE_vol_per_well,
                           start=ERE_start_index,
                           end=ERE_end_index,
                           msg=("Out of End-repair enzyme, please replace "
                                "reagent plate"),
                           reagent_name="End Repair Enzyme",
                           is_verbose=is_verbose_mode,
                           is_strict_mode=True)

    # Reagent wells for mastermix 2: Adaptor ligation
    ALB_wells = VolTracker(labware=yourgene_reagent_plate_I,
                           well_vol=ALB_vol_per_well,
                           start=ALB_start_index,
                           end=ALB_end_index,
                           msg=("Out of End-repair enzyme, please replace "
                                "replace reagent plate"),
                           reagent_name="Adaptor Ligation Buffer",
                           is_verbose=is_verbose_mode,
                           is_strict_mode=True)
    ALE_I_wells = VolTracker(labware=yourgene_reagent_plate_I,
                             well_vol=ALE_I_vol_per_well,
                             start=ALE_I_start_index,
                             end=ALE_I_end_index,
                             msg=("Out of Adaptor ligation enzyme I, please "
                                  "replace reagent plate"),
                             reagent_name="Adaptor Ligation Enzyme I",
                             is_verbose=is_verbose_mode,
                             is_strict_mode=True)
    ALE_II_wells = VolTracker(labware=yourgene_reagent_plate_I,
                              well_vol=ALE_II_vol_per_well,
                              start=ALE_II_start_index,
                              end=ALE_II_end_index,
                              msg=("Out of Adaptor ligation enzyme II, please "
                                   "replace reagent plate"),
                              reagent_name="Adaptor Ligation enzyme II",
                              is_verbose=is_verbose_mode,
                              is_strict_mode=True)

    # Reagent wells for mastermix 3: PCR
    PCR_mix_wells = VolTracker(labware=yourgene_reagent_plate_I,
                               well_vol=PCR_mix_vol_per_well,
                               start=PCR_mix_start_index,
                               end=PCR_mix_end_index,
                               msg=("Out of PCR mix, please "
                                    "replace reagent plate"),
                               reagent_name="PCR mix",
                               is_verbose=is_verbose_mode,
                               is_strict_mode=True)
    primer_wells = VolTracker(labware=yourgene_reagent_plate_I,
                              well_vol=primer_vol_per_well,
                              start=primer_start_index,
                              end=primer_end_index,
                              msg=("Out of primers, please "
                                   "replace reagent plate"),
                              reagent_name="Primers",
                              is_verbose=is_verbose_mode,
                              is_strict_mode=True)

    # plate, tube rack maps

    '''
    Define any plate or tube maps here.

    e.g.

    plate_wells_by_row = [well for row in plate.rows() for well in row]

    '''
    # Mastermix destination tubes
    ER_mm_dest_tube = tuberack.wells()[0]
    AL_mm_dest_tube = tuberack.wells()[1]
    PCR_mm_dest_tube = tuberack.wells()[2]

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
    def create_mastermix(sources: List[VolTracker],
                         reagent_volumes: List[float],
                         template_message: str,
                         messages: List[str]) -> None:
        """
        Create a mastermix from a list of reagents drawing from the sources
        wells.
        :param sources: VolTrackers keeping track of the reagent wells
        :param reagent_volumes: The volume of reagent to transfer from
        the 'sources'
        :param template_message: A template comment to tell the user something
        about the reagents currently being transferred
        :param messages: Can be a string describing each reagent
        """
        nonlocal pip_s, pip_l
        for source, vol, msg in zip(sources,
                                    reagent_volumes,
                                    messages):
            ctx.comment(template_message.format(msg))
            source_well_volume = source.get_active_well_remaining_vol()
            while vol > 0:
                pip_vol = min(source_well_volume, vol)
                pip = pip_s if pip_vol < pip_s.max_volume else pip_l
                if not pip.has_tip:
                    pip.pick_up_tip()
                s_well = source.track(pip_vol)
                pip.transfer(pip_vol, s_well, ER_mm_dest_tube, new_tip='never')
                vol -= pip_vol
                if source.get_active_well_remaining_vol() <= 1:
                    source.advance_well()
            drop_all_tips([pip_s, pip_l])

    # PROTOCOL BEGINS HERE
    pip_s, pip_l = rank_pipettes([pip_left, pip_right])
    # 1st mastermix: End-repair
    if is_create_end_repair_mm:
        ctx.comment("\n\nCreating End repair mastermix in {}\n"
                    .format(ER_mm_dest_tube))
        create_mastermix([ERB_wells, ERE_wells],
                         [total_ERB_mm_vol, total_ERE_mm_vol],
                         "Transferring End Repair {}",
                         ["Buffer", "Enzyme"])

    if is_create_adaptor_ligation_mm:
        ctx.comment("\n\nCreating Adaptor Ligation mastermix in {}\n"
                    .format(AL_mm_dest_tube))
        create_mastermix([ALB_wells, ALE_I_wells, ALE_II_wells],
                         [total_ALB_mm_vol, total_ALE_I_mm_vol,
                         total_ALE_II_mm_vol],
                         "Transferring adaptor ligation {}",
                         ["Buffer", "Enzyme I", "Enzyme II"])

    if is_create_pcr_mm:
        ctx.comment("\n\nCreating PCR mastermix in {}\n"
                    .format(PCR_mm_dest_tube))
        create_mastermix([PCR_mix_wells, primer_wells],
                         [totaL_PCR_mix_mm_vol, total_primer_mm_vol],
                         "Transferring {}",
                         ["PCR mix", "primers"])

    if is_verbose_mode is True:

        # Check End repair reaction mastermix
        ctx.comment("\nTotal ERB vol to transfer: ", total_ERB_mm_vol, "\n")
        ctx.comment("ERB vol tracker: ", ERB_wells, "\n")
        ctx.comment("Total ERE vol to transfer: ", total_ERE_mm_vol, "\n")
        ctx.comment("ERE vol tracker: ", ERE_wells, "\n")

        # Check adaptor ligation reaction mastermix
        ctx.comment("\nTotal ALB vol to transfer: ", total_ALB_mm_vol, "\n")
        ctx.comment("ALB vol tracker: ", ALB_wells, "\n")
        ctx.comment("Total ALE I vol to transfer: ", total_ALE_I_mm_vol, "\n")
        ctx.comment("ALE I vol tracker: ", ALE_I_wells, "\n")
        ctx.comment("Total ALE II vol to transfer: ",
                    total_ALE_II_mm_vol, "\n")
        ctx.comment("ALE II vol tracker: ", ALE_II_wells, "\n")

        # Check PCR reaction mastermix
        ctx.comment("\nTotal PCR mix vol to transfer: ",
                    totaL_PCR_mix_mm_vol, "\n")
        ctx.comment("PCR mix vol tracker: ", PCR_mix_wells, "\n")
        ctx.comment("Total primer vol to transfer: ",
                    total_primer_mm_vol, "\n")
        ctx.comment("Primer vol tracker: ", primer_wells, "\n")
