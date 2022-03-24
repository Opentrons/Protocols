from opentrons import protocol_api
import csv
from typing import List

metadata = {
    'protocolName': '022548-2 - DNA extraction',
    'author': 'Eskil Andersen <protocols@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.11'   # CHECK IF YOUR API LEVEL HERE IS UP TO DATE
                         # IN SECTION 5.2 OF THE APIV2 "VERSIONING"
}


def get_values(*names):
    import json
    _all_values = json.loads("""{
                                  "n_tuberacks":3,
                                  "n_samples_rack_1":32,
                                  "n_samples_rack_2":32,
                                  "n_samples_rack_3":32,
                                  "is_create_mastermix":true,
                                  "mastermix_csv":"source well,component name,volume,,,,\\\\nA1,component 1,100,,,,",
                                  "bindbuf_target_well_no":11,
                                  "master_bead_mix_well_no":12
                                  }
                                  """)
    return [_all_values[n] for n in names]


def run(ctx: protocol_api.ProtocolContext):

    [n_tuberacks,
     n_samples_rack_1,
     n_samples_rack_2,
     n_samples_rack_3,
     is_create_mastermix,
     mastermix_csv,
     bindbuf_target_well_no,
     master_bead_mix_well_no] = get_values(  # noqa: F821
     "n_tuberacks",
     "n_samples_rack_1",
     "n_samples_rack_2",
     "n_samples_rack_3",
     "is_create_mastermix",
     "mastermix_csv",
     "bindbuf_target_well_no",
     "master_bead_mix_well_no")

    def parse_csv(csv_string) -> List:
        csv_string = csv_string.strip()
        lines = str(csv_string).splitlines()
        csv_reader = csv.reader(lines, delimiter=',')
        mastermix_list = []
        for row in csv_reader:
            mastermix_list.append(row)
        return mastermix_list

    tuberack_upper_bound = 2 if is_create_mastermix else 3
    if n_tuberacks > tuberack_upper_bound or n_tuberacks < 1:
        raise Exception(("Sample tube racks should be between 1 to {}"
                         "Are you creating a mastermix? If so 2 tuberacks "
                         "is max").format(tuberack_upper_bound))

    for i, n in enumerate([n_samples_rack_1,
                           n_samples_rack_2,
                           n_samples_rack_3]):
        if n < 0 or n > 32:
            raise Exception(
                "Invalid number of samples (n={}) on tuberack #{}".format(
                    n, i+1)
                )
    n_total_samples = (n_samples_rack_1 + n_samples_rack_2
                       if is_create_mastermix else n_samples_rack_1
                       + n_samples_rack_2 + n_samples_rack_3)
    total_bind_buf_vol = n_total_samples*1.5*265
    total_bead_vol = (10/265) * total_bind_buf_vol
    total_mm_vol = total_bind_buf_vol + total_bead_vol
    # The volume of mastermix in each reservoir well should be 9.65 mL max
    # and also accounting for 1 mL dead volume in the resevoir
    vol_per_reservoir_well = 9.65 - 1
    n_resevoir_wells = ceil(total_mm_vol/vol_per_reservoir_well)

    mastermix_list = parse_csv(mastermix_csv)
    sample_tuberack_lname = "nest_32_tuberack_8x15ml_8x15ml_8x15ml_8x15ml"
    plate_lname = "thermofisherkingfisherdeepwell_96_wellplate_2000ul"

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
    tiprack_200 = [ctx.load_labware('opentrons_96_filtertiprack_200ul', '6')]
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
