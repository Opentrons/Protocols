from opentrons import protocol_api
from opentrons.protocol_api.labware import Labware, Well
from opentrons.protocol_api.contexts import TemperatureModuleContext
from typing import List, Sequence
import csv
import math

# The first part of this protocol mixes the DNA samples with end repair
# buffer and enzyme and ends when the samples are ready for thermal incubation
metadata = {
    'protocolName': '466f93-6 - Mastermix creation protocol',
    'author': 'Eskil Andersen <eskil.andersen@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.11'   # CHECK IF YOUR API LEVEL HERE IS UP TO DATE
                         # IN SECTION 5.2 OF THE APIV2 "VERSIONING"
}


def parse_csv(csv_string) -> List:
    csv_string = csv_string.strip()
    lines = str(csv_string).splitlines()
    csv_reader = csv.reader(lines, delimiter=',')
    data_matrix = []
    for row in csv_reader:
        data_matrix.append(row)
    return data_matrix


def get_line_by_reagent_name(name: str, reagent_data: List[List]) -> List:
    for line in reagent_data:
        if name == line[0]:
            return line
    msg = ("the \"{}\" reagent name was not found in the reagent lists. "
           "The reagents list contains the following entries: {}")
    msg = msg.format(name, reagent_data)
    raise Exception(msg)


def get_values(*names):
    import json
    _all_values = json.loads("""{
                                  "n_samples":36,
                                  "n_over_reactions":1,
                                  "input_csv":"Reagent name,Starting well,Starting volume,Flow rate multiplier\\nEnd repair buffer,2,12,0.7\\nEnd repair enzyme,1,100,0.2\\nAdaptor ligation buffer,1,45,0.7\\nAdaptor ligation enzyme I,2,27,0.2\\nAdaptor ligation enzyme II,1,39,0.2\\nPCR mix,1,117,0.2\\nPrimer,1,45,1",
                                  "mixing_rate_multiplier":0.5,
                                  "n_mixes":10,
                                  "pip_left_lname":"p1000_single_gen2",
                                  "is_filtered_left":true,
                                  "pip_right_lname":"p1000_single_gen2",
                                  "is_filtered_right":true,
                                  "mm_type":"create_ER_mix",
                                  "mastermix_target_lname":"opentrons_24_tuberack_nest_1.5ml_snapcap",
                                  "is_verbose_mode":false,
                                  "temp_mod_reag_plate":false,
                                  "temp_mod_tuberack":false,
                                  "tmod_temperature":4
                                  }
                                  """)  # noqa
    return [_all_values[n] for n in names]


def run(ctx: protocol_api.ProtocolContext):

    [n_samples,
     n_over_reactions,
     input_csv,
     mixing_rate_multiplier,
     n_mixes,
     pip_left_lname,
     is_filtered_left,
     pip_right_lname,
     is_filtered_right,
     mm_type,
     mastermix_target_lname,
     is_verbose_mode,
     temp_mod_reag_plate,
     temp_mod_tuberack,
     tmod_temperature] = get_values(  # noqa: F821
     "n_samples",
     "n_over_reactions",
     "input_csv",
     "mixing_rate_multiplier",
     "n_mixes",
     "pip_left_lname",
     "is_filtered_left",
     "pip_right_lname",
     "is_filtered_right",
     "mm_type",
     "mastermix_target_lname",
     "is_verbose_mode",
     "temp_mod_reag_plate",
     "temp_mod_tuberack",
     "tmod_temperature")

    # Parse reagent definition csv input
    reagent_data = parse_csv(input_csv)

    # Input error checking:---------------------------------------------------

    # Check that the reagent names are recognized (not case sensitive)
    # Set of recognized reagent names:
    recognized_reagents = \
        {"end repair buffer", "end repair enzyme",
         "adaptor ligation buffer", "adaptor ligation enzyme i",
         "adaptor ligation enzyme ii", "pcr mix", "primer"}

    # String surrounding whitespace/lowercase reagent names and:
    # Check that the data is properly formatted, skip header
    for line in reagent_data[1:]:
        line[0] = line[0].strip().lower()
        if not line[0] in recognized_reagents:
            msg = ("{} is not a valid reagent name, allowed names are {}. "
                   + "The names are not case sensitive")
            msg = msg.format(line[0], str(recognized_reagents))
            raise Exception(msg)

    if not pip_left_lname and not pip_right_lname:
        raise Exception("You must load at least one pipette")

    # define all custom variables above here with descriptions:
    # Source volumes of reagents, and number of wells containing the reagent
    # 1st mastermix: End repair
    n_total_samples = n_samples + n_over_reactions

    ERB_reagent_data = get_line_by_reagent_name(
        "end repair buffer", reagent_data)

    ERB_start_index = int(ERB_reagent_data[1])
    ERB_vol_per_well = 27
    ERB_vol_first_well = float(ERB_reagent_data[2])
    ERB_initial_well_vol_used = ERB_vol_per_well - ERB_vol_first_well
    n_ERB_wells = 8
    ERB_vol_per_sample = 1.5
    ERB_end_index = n_ERB_wells
    total_ERB_mm_vol = n_total_samples * ERB_vol_per_sample

    ERE_reagent_data = get_line_by_reagent_name(
        "end repair enzyme", reagent_data)
    ERE_vol_per_well = 126
    ERE_vol_first_well = float(ERE_reagent_data[2])
    ERE_initial_well_vol_used = ERE_vol_per_well - ERE_vol_first_well
    n_ERE_wells = 1
    ERE_vol_per_sample = 0.75
    total_ERE_mm_vol = n_total_samples * ERE_vol_per_sample
    # 225 uL per 100 samples
    ER_mm_vol_per_sample = ERB_vol_per_sample + ERE_vol_per_sample
    # Well numbers
    ERE_start_index = 9
    ERE_end_index = ERE_start_index + n_ERE_wells - 1
    # Required volumes for creating the mastermix
    total_ER_mm_vol = n_total_samples * ER_mm_vol_per_sample
    # Calculate the maximum number of samples for which ER mm can
    # be created based on the remaining volume
    max_ERB_source_vol = n_ERB_wells * ERB_vol_per_well
    remaining_ERB_source_vol = \
        (max_ERB_source_vol - (ERB_start_index-1)*ERB_vol_per_well
         - ERB_initial_well_vol_used)
    max_ERB_samples = math.floor(remaining_ERB_source_vol/ERB_vol_per_sample)
    max_ERE_source_vol = n_ERE_wells * ERE_vol_per_well
    remaining_ERE_source_vol = max_ERE_source_vol - ERE_initial_well_vol_used
    max_ERE_samples = math.floor(remaining_ERE_source_vol/ERE_vol_per_sample)
    max_ER_mm_samples_left = min(max_ERB_samples, max_ERE_samples)

    # 2nd mastermix: Adaptor ligation
    # ALB_reagent_data = get_line_by_reagent_name(
    #     "adaptor ligation buffer", reagent_data)
    ALB_vol_per_well = 45
    ALB_start_index = 8*2+1
    n_ALB_wells = 8
    ALB_end_index = ALB_start_index + n_ALB_wells - 1
    total_ALB_vol = ALB_vol_per_well * n_ALB_wells

    ALE_I_vol_per_well = 27
    n_ALE_I_wells = 8
    ALE_I_start_index = 8*3+1
    ALE_I_end_index = ALE_I_start_index + n_ALE_I_wells - 1
    total_ALE_I_vol = ALE_I_vol_per_well * n_ALE_I_wells

    ALE_II_vol_per_well = 39
    n_ALE_II_wells = 1
    ALE_II_start_index = 8*4+1
    ALE_II_end_index = ALE_II_start_index + n_ALE_II_wells - 1

    total_ALE_II_vol = ALE_II_vol_per_well * n_ALE_II_wells

    ALB_vol_per_sample = 2.50
    ALE_I_vol_per_sample = 1.50
    ALE_II_vol_per_sample = 0.25

    total_ALB_mm_vol = n_total_samples * ALB_vol_per_sample
    total_ALE_I_mm_vol = n_total_samples * ALE_I_vol_per_sample
    total_ALE_II_mm_vol = n_total_samples * ALE_II_vol_per_sample

    max_ALB_samples = math.floor(total_ALB_vol/ALB_vol_per_sample)
    max_ALE_I_samples = math.floor(total_ALE_I_vol/ALE_I_vol_per_sample)
    max_ALE_II_samples = math.floor(total_ALE_II_vol/ALE_II_vol_per_sample)
    max_AL_mm_samples = min(
        max_ALB_samples, max_ALE_I_samples, max_ALE_II_samples)

    # Error checking

    total_AL_mm_vol_per_sample = (ALB_vol_per_sample + ALE_I_vol_per_sample
                                  + ALE_II_vol_per_sample)
    total_AL_mm_vol = n_total_samples * total_AL_mm_vol_per_sample

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

    max_PCR_mix_samples = math.floor(total_PCR_mix_vol/PCR_mix_vol_per_sample)
    max_primer_samples = math.floor(total_primer_vol/primer_vol_per_sample)
    max_PCR_mm_samples = min(max_PCR_mix_samples, max_primer_samples)
    total_PCR_mm_vol = n_total_samples * PCR_mm_vol_per_sample
    # Total volumes to transfer to make mastermix
    totaL_PCR_mix_mm_vol = PCR_mix_vol_per_sample * n_total_samples
    total_primer_mm_vol = primer_vol_per_sample * n_total_samples

    # Error check that we can make the required amount of mastermix
    if mm_type == "create_ER_mix" and n_total_samples > max_ER_mm_samples_left:
        raise Exception(
            "You are trying to create {} aliquots of PCR "
            "mastermix, but there is only enough reagent on the Yourgene "
            "reagent plate 1 for {} mastermix aliquots"
            .format(n_total_samples, int(max_PCR_mm_samples)))
    elif mm_type == "create_AL_mix" and n_total_samples > max_AL_mm_samples:
        raise Exception(
            ("You are trying to create {} aliquots of Adaptor-Ligation "
             "mastermix, but there is only enough reagent on the Yourgene "
             "reagent plate 1 for {} mastermix aliquots, designate fewer "
             "samples per run, and re-run the protocol as many times are "
             "needed")
            .format(n_total_samples, int(max_AL_mm_samples)))
    if mm_type == "create_PCR_mix" and n_total_samples > max_PCR_mm_samples:
        raise Exception(
            "You are trying to create {} aliquots of PCR "
            "mastermix, but there is only enough reagent on the Yourgene "
            "reagent plate 1 for {} mastermix aliquots"
            .format(n_total_samples, int(max_PCR_mm_samples)))

    source_well_plate_lname = (
        "azenta_96_wellplate_semiskirted_adapter_300ul"
        if temp_mod_reag_plate is False else
        "azenta_96_aluminumblock_300ul")

    # load modules

    '''

    Add your modules here with:

    module_name = ctx.load_module('{module_loadname}', '{slot number}')

    Note: if you are loading a thermocycler, you do not need to specify
    a slot number - thermocyclers will always occupy slots 7, 8, 10, and 11.

    For all other modules, you can load them on slots 1, 3, 4, 6, 7, 9, 10.

    '''
    reagent_plate_slot = '4'
    mm_tuberack_slot = '7'
    temp_mod_reag: TemperatureModuleContext = None
    temp_mod_rack: TemperatureModuleContext = None
    if temp_mod_reag_plate is True:
        temp_mod_reag = ctx.load_module(
            'temperature module gen2', reagent_plate_slot)
    if temp_mod_tuberack is True:
        temp_mod_rack = ctx.load_module(
            'temperature module gen2', mm_tuberack_slot)

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
    yourgene_reagent_plate_I = None
    tuberack = None

    if temp_mod_reag is not None:
        yourgene_reagent_plate_I = temp_mod_reag.load_labware(
            source_well_plate_lname, 'Yourgene Reagent plate - 1')
    else:
        yourgene_reagent_plate_I \
            = ctx.load_labware(source_well_plate_lname, reagent_plate_slot,
                               'Yourgene Reagent plate - 1')

    if temp_mod_rack is not None:
        tuberack = temp_mod_rack.load_labware(mastermix_target_lname,
                                              'Mastermix target tuberack')
    else:
        tuberack = ctx.load_labware(mastermix_target_lname, mm_tuberack_slot,
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
    # Track previously used volume:
    ERB_wells.track(ERB_initial_well_vol_used)

    # Only one well so it always starts and ends on the 1st well of col 2.
    ERE_wells = VolTracker(labware=yourgene_reagent_plate_I,
                           well_vol=ERE_vol_per_well,
                           start=ERE_start_index,
                           end=ERE_end_index,
                           msg=("Out of End-repair enzyme, please replace "
                                "reagent plate"),
                           reagent_name="End Repair Enzyme",
                           is_verbose=is_verbose_mode,
                           is_strict_mode=True)
    ERE_wells.track(ERE_initial_well_vol_used)

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
    def create_mastermix(sources: Sequence[VolTracker],
                         dest_tube,
                         reagent_volumes: List[float],
                         template_message: str,
                         reagent_names: List[str],
                         n_mixes: int = 0,
                         flow_rate_multipliers: Sequence[float] = None,
                         mixing_rate: float = 1) -> None:
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

        total_vol = sum(reagent_volumes)
        i = 0
        for source, vol, msg in zip(sources,
                                    reagent_volumes,
                                    reagent_names):
            for pip in pip_s, pip_l:
                pip.flow_rate.aspirate *= flow_rate_multipliers[i]
                pip.flow_rate.dispense *= flow_rate_multipliers[i]
            ctx.comment(template_message.format(msg))
            source_well_volume = source.get_active_well_remaining_vol()
            while vol > 0:
                pip_vol = min(source_well_volume, vol)
                pip = pip_s if pip_vol < pip_s.max_volume else pip_l
                if not pip.has_tip:
                    pip.pick_up_tip()
                s_well = source.track(pip_vol)
                pip.transfer(pip_vol, s_well, dest_tube, new_tip='never')
                vol -= pip_vol
                if source.get_active_well_remaining_vol() <= 1:
                    source.advance_well()
            drop_all_tips([pip_s, pip_l])
            for pip in pip_s, pip_l:
                pip.flow_rate.aspirate /= flow_rate_multipliers[i]
                pip.flow_rate.dispense /= flow_rate_multipliers[i]
            i += 1

        # step 2: mix
        pip = (pip_l if total_vol > pip_s.max_volume else pip_s)
        pip.pick_up_tip()
        mix_vol = min(pip.max_volume, total_vol-2)
        pip.mix(n_mixes, mix_vol, dest_tube, mixing_rate)
        pip.drop_tip()

    # PROTOCOL BEGINS HERE
    # set tmod temperatures
    for tmod in [temp_mod_reag, temp_mod_rack]:
        if tmod is not None:
            tmod.set_temperature(tmod_temperature)

    pip_s, pip_l = rank_pipettes([pip_left, pip_right])
    # 1st mastermix: End-repair
    if "create_ER_mix" == mm_type:
        ctx.comment("\n\nCreating End repair mastermix in {}\n"
                    .format(ER_mm_dest_tube))
        # import pdb
        # pdb.set_trace()
        flow_rates = [float(ERB_reagent_data[3]), float(ERE_reagent_data[3])]
        create_mastermix(sources=[ERB_wells, ERE_wells],
                         dest_tube=ER_mm_dest_tube,
                         reagent_volumes=[total_ERB_mm_vol, total_ERE_mm_vol],
                         template_message="Transferring End Repair {}",
                         reagent_names=["Buffer", "Enzyme"],
                         n_mixes=n_mixes,
                         flow_rate_multipliers=flow_rates,
                         mixing_rate=mixing_rate_multiplier)

    elif "create_AL_mix" == mm_type:
        ctx.comment("\n\nCreating Adaptor Ligation mastermix in {}\n"
                    .format(AL_mm_dest_tube))
        create_mastermix(sources=[ALB_wells, ALE_I_wells, ALE_II_wells],
                         dest_tube=AL_mm_dest_tube,
                         reagent_volumes=[total_ALB_mm_vol, total_ALE_I_mm_vol,
                         total_ALE_II_mm_vol],
                         template_message="Transferring adaptor ligation {}",
                         reagent_names=["Buffer", "Enzyme I", "Enzyme II"],
                         n_mixes=n_mixes,
                         mixing_rate=mixing_rate_multiplier)

    elif "create_PCR_mix" == mm_type:
        ctx.comment("\n\nCreating PCR mastermix in {}\n"
                    .format(PCR_mm_dest_tube))
        create_mastermix(sources=[PCR_mix_wells, primer_wells],
                         dest_tube=PCR_mm_dest_tube,
                         reagent_volumes=[
                             totaL_PCR_mix_mm_vol, total_primer_mm_vol],
                         template_message="Transferring {}",
                         reagent_names=["PCR mix", "primers"],
                         n_mixes=n_mixes,
                         mixing_rate=mixing_rate_multiplier)
    else:
        msg = ("Unrecognized mastermix option {}, valid choices are: "
               + "create_ER_mix, create_AL_mix or create_PCR_mix")
        msg = msg.format(mm_type)
        raise Exception(msg)

    if is_verbose_mode is True:

        # Check End repair reaction mastermix
        ctx.comment("\nTotal ERB vol to transfer: "
                    + str(total_ERB_mm_vol) + "\n")
        ctx.comment("ERB vol tracker: " + str(ERB_wells) + "\n")
        ctx.comment("Total ERE vol to transfer: "
                    + str(total_ERE_mm_vol) + "\n")
        ctx.comment("ERE vol tracker: " + str(ERE_wells) + "\n")

        # Check adaptor ligation reaction mastermix
        ctx.comment("\nTotal ALB vol to transfer: "
                    + str(total_ALB_mm_vol) + "\n")
        ctx.comment("ALB vol tracker: " + str(ALB_wells) + "\n")
        ctx.comment("Total ALE I vol to transfer: "
                    + str(total_ALE_I_mm_vol) + "\n")
        ctx.comment("ALE I vol tracker: " + str(ALE_I_wells) + "\n")
        ctx.comment("Total ALE II vol to transfer: "
                    + str(total_ALE_II_mm_vol) + "\n")
        ctx.comment("ALE II vol tracker: " + str(ALE_II_wells) + "\n")

        # Check PCR reaction mastermix
        ctx.comment("\nTotal PCR mix vol to transfer: "
                    + str(totaL_PCR_mix_mm_vol) + "\n")
        ctx.comment("PCR mix vol tracker: " + str(PCR_mix_wells) + "\n")
        ctx.comment("Total primer vol to transfer: "
                    + str(total_primer_mm_vol) + "\n")
        ctx.comment("Primer vol tracker: " + str(primer_wells) + "\n")
        ctx.comment("Primer vol tracker: " + str(primer_wells) + "\n")
