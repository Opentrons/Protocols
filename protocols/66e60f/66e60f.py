from opentrons import protocol_api
import re

metadata = {
    'protocolName': 'Protocol Title',
    'author': 'AUTHOR NAME <authoremail@company.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.11'   # CHECK IF YOUR API LEVEL HERE IS UP TO DATE
                         # IN SECTION 5.2 OF THE APIV2 "VERSIONING"
}


def get_values(*names):
    import json
    _all_values = json.loads("""{"input_csv":"Well,Description,Concentration,Volume_to_transfer,,,,,,,\\nA01,13377_16S_Bac,3.28,12.52,,,,,,,\\nB01,13378_16S_Bac,2.76,14.88,,,,,,,\\nC01,13379_16S_Bac,3.28,12.52,,,,,,,\\nD01,13380_16S_Bac,4.76,8.63,,,,,,,\\nE01,13381_16S_Bac,5.78,7.11,,,,,,,\\nF01,13382_16S_Bac,3.08,13.34,,,,,,,\\nG01,13383_16S_Bac,3.36,12.23,,,,,,,\\nH01,13384_16S_Bac,6.22,6.6,,,,,,,\\nA02,13385_16S_Bac,2.98,13.78,,,,,,,\\nB02,13386_16S_Bac,2.68,15.33,,,,,,,\\nC02,13377_18S_Capra,4.86,15.91,,,,,,,\\nD02,13378_18S_Capra,3.04,25.43,,,,,,,\\nE02,13379_18S_Capra,2.44,31.68,,,,,,,\\nF02,13380_18S_Capra,2.84,27.22,,,,,,,                                                                                                                                                                                                                                                                                                                                                                                                                                                                  \\nG02,13381_18S_Capra,2.76,28.01,,,,,,,\\nH02,13382_18S_Capra,2.74,28.21,,,,,,,\\nA03,13383_18S_Capra,3.28,23.57,,,,,,,\\nB03,13384_18S_Capra,6.2,12.47,,,,,,,\\nC03,13385_18S_Capra,5.04,15.34,,,,,,,\\nD03,13386_18S_Capra,4.24,18.23,,,,,,,\\nE03,13377_ITS2_3F4R,5.98,9.02,,,,,,,\\nF03,13378_ITS2_3F4R,4.46,12.1,,,,,,,\\nG03,13379_ITS2_3F4R,3.7,14.58,,,,,,,\\nH03,13380_ITS2_3F4R,2.68,20.13,,,,,,,\\nA04,13381_ITS2_3F4R,4.26,12.67,,,,,,,\\nB04,13382_ITS2_3F4R,3.58,15.07,,,,,,,\\nC04,13383_ITS2_3F4R,3.54,15.24,,,,,,,\\nD04,13384_ITS2_3F4R,5.36,10.07,,,,,,,\\nE04,13385_ITS2_3F4R,2.34,23.06,,,,,,,\\nF04,13386_ITS2_3F4R,2.58,20.92,,,,,,,\\nG04,13563A_MIV,3.92,8.78,,,,,,,\\nH04,13564A_MIV,2.92,11.79,,,,,,,\\nA05,13565A_MIV,3.08,11.18,,,,,,,\\nB05,13566A_MIV,3.9,8.83,,,,,,,\\nC05,13567A_MIV,2.86,12.04,,,,,,,\\nD05,13568A_MIV,5.24,6.57,,,,,,,\\nE05,13569A_MIV,4.52,7.62,,,,,,,\\nF05,13570A_MIV,2.54,13.55,,,,,,,\\nG05,13571A_MIV,4.12,8.36,,,,,,,\\nH05,13572A_MIV,2.46,13.99,,,,,,,\\nA06,13573A_MIV,3.24,10.63,,,,,,,\\nB06,13574A_MIV,3.3,10.43,,,,,,,\\nC06,13575A_MIV,4.32,7.97,,,,,,,\\nD06,13576A_MIV,4.18,8.24,,,,,,,\\nE06,13577A_MIV,5.1,6.75,,,,,,,\\nF06,13578A_MIV,4.52,7.62,,,,,,,\\nG06,13579A_MIV,4.3,8.01,,,,,,,\\nH06,13580A_MIV,3.4,10.13,,,,,,,\\nA07,13581A_MIV,4.12,8.36,,,,,,,\\nB07,13582A_MIV,2.06,16.71,,,,,,,\\nC07,13583A_MIV,2.88,11.95,,,,,,,\\nD07,13584A_MIV,2.16,15.94,,,,,,,\\nE07,13585A_MIV,4.12,8.36,,,,,,,\\nF07,13586A_MIV,2.2,15.65,,,,,,,\\nG07,13587A_MIV,2.22,15.51,,,,,,,\\nH07,13588A_MIV,3.72,9.25,,,,,,,\\nA08,13589A_MIV,3,11.48,,,,,,,\\nB08,13590A_MIV,1.15,29.94,,,,,,,\\nC08,13591A_MIV,3.48,9.89,,,,,,,\\nD08,13593A_MIV,2.08,16.55,,,,,,,\\nE08,13594A_MIV,2.98,11.55,,,,,,,\\nF08,13595A_MIV,2.74,12.56,,,,,,,\\nG08,13660A_MIV,4.06,8.48,,,,,,,\\nH08,13563A_Kelly,4.08,7.2,,,,,,,\\nA09,13564A_Kelly,4.3,6.83,,,,,,,\\nB09,13565A_Kelly,4,7.34,,,,,,,\\nC09,13566A_Kelly,3.84,7.65,,,,,,,\\nD09,13567A_Kelly,3.36,8.74,,,,,,,\\nE09,13568A_Kelly,3.34,8.79,,,,,,,\\nF09,13569A_Kelly,3.62,8.11,,,,,,,\\nG09,13570A_Kelly,4.12,7.13,,,,,,,\\nH09,13571A_Kelly,2.92,10.05,,,,,,,\\nA10,13572A_Kelly,5.36,5.48,,,,,,,\\nB10,13573A_Kelly,3.14,9.35,,,,,,,\\nC10,13574A_Kelly,4.08,7.2,,,,,,,\\nD10,13575A_Kelly,2.66,11.04,,,,,,,\\nE10,13576A_Kelly,3.04,9.66,,,,,,,\\nF10,13577A_Kelly,4.12,7.13,,,,,,,\\nG10,13578A_Kelly,5.82,5.04,,,,,,,\\nH10,13579A_Kelly,4.4,6.67,,,,,,,\\nA11,13580A_Kelly,4.24,6.92,,,,,,,\\nB11,13581A_Kelly,2.86,10.26,,,,,,,\\nC11,13582A_Kelly,1.57,18.7,,,,,,,\\nD11,13583A_Kelly,2.7,10.87,,,,,,,\\nE11,13584A_Kelly,2,14.68,,,,,,,\\nF11,13585A_Kelly,2.76,10.64,,,,,,,\\nG11,13586A_Kelly,3.84,7.65,,,,,,,\\nH11,13587A_Kelly,1.67,17.58,,,,,,,\\nA12,13588A_Kelly,3.38,8.69,,,,,,,\\nB12,13589A_Kelly,2.96,9.92,,,,,,,\\nC12,13590A_Kelly,3.04,9.66,,,,,,,\\nD12,13591A_Kelly,2.04,14.39,,,,,,,\\nE12,13593A_Kelly,1.53,19.19,,,,,,,\\nF12,13594A_Kelly,1.29,22.76,,,,,,,\\nG12,13595A_Kelly,3.66,8.02,,,,,,,\\nH12,13660A_Kelly,3.42,8.58,,,,,,,\\n,,,,,,,,,,\\n,,,,,,,,,,\\n,,,,,,,,,,\\n,,,,,,,,,,\\n,,,,,,,,,,\\n,,,,,,,,,,\\n,,,,,,,,,,\\n,,,,,,,,,,\\n",
    "source_type":"biorad_96_wellplate_200ul_pcr",
    "dest_type":"biorad_96_wellplate_200ul_pcr"}""")
    return [_all_values[n] for n in names]


def run(ctx: protocol_api.ProtocolContext):

    [input_csv, source_type, dest_type] = get_values(  # noqa: F821
        'input_csv', 'source_type', 'dest_type')

    # define all custom variables above here with descriptions:
    left_pipette_loadname = 'p20_single_gen2'
    right_pipette_loadname = 'p300_single_gen2'

    target_plate_loader = (dest_type, '1',
                           'target plate')
    DNA_sample_plate_loader = (dest_type, '7',
                               'DNA sample plate')
    tiprack_300uL_loader = ('opentrons_96_filtertiprack_200ul', '2')
    tiprack_20uL_loader = ('opentrons_96_filtertiprack_20ul', '5')

    reservoir_loader = ('nest_12_reservoir_15ml', '4', 'water reservoir')

    # Initial 40 uL water for each well of the target
    initial_water_volume = 40

    # Read CSV and format the inputs
    # csv format: Well | Description | Concentration | volume to transfer
    #              [0]       [1]           [2]                [3]
    data = [
        [val.strip().upper() for val in line.split(',')
            if val != '']
        for line in input_csv.splitlines()[1:]
        if line and line.split(',')[0]]

    # Convert any well designation in column 1 from [A-H]0[1-9] to [A-H][1-9]
    # e.g. A01 -> A1 etc.
    pattern = re.compile('[A-H]0[1-9]')
    for row in data:
        if pattern.match(row[0]):
            row[0] = row[0].replace('0', '')

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
    reservoir = ctx.load_labware(reservoir_loader[0], reservoir_loader[1],
                                 reservoir_loader[2])
    dna_sample_plate = ctx.load_labware(DNA_sample_plate_loader[0],
                                        DNA_sample_plate_loader[1],
                                        DNA_sample_plate_loader[2])
    target_plate = ctx.load_labware(target_plate_loader[0],
                                    target_plate_loader[1],
                                    target_plate_loader[2])

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
    tiprack_20_filter = [ctx.load_labware(tiprack_20uL_loader[0],
                                          tiprack_20uL_loader[1])]
    tiprack_300_filter = [ctx.load_labware(tiprack_300uL_loader[0],
                                           tiprack_300uL_loader[1])]

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
    # Load m20 and p20, m20 switches out for p300 in step 2
    p20 = ctx.load_instrument(
                        left_pipette_loadname,
                        "left",
                        tip_racks=tiprack_20_filter
                        )
    p300 = ctx.load_instrument(
                        right_pipette_loadname,
                        "right",
                        tip_racks=tiprack_300_filter
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

    # reagents

    '''
    Define where all reagents are on the deck using the labware defined above.

    e.g.

    water = reservoir12.wells()[-1]
    waste = reservoir.wells()[0]
    samples = plate.rows()[0][0]
    dnase = tuberack.wells_by_name()['A4']

    '''
    water_well = reservoir.wells_by_name()['A1']
    waste_well = reservoir.wells_by_name()['A2']

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

    ctx.comment("\nTransferring water to target plate\n")
    p300.pick_up_tip()
    for well in target_plate.wells():
        if p300.current_volume < 40:
            p300.aspirate(200-p300.current_volume, water_well)
        p300.dispense(40, well)
    p300.blow_out(water_well)
    p300.return_tip()
    p300.reset_tipracks()

    # Transfering DNA samples to target
    ctx.comment("\nTransferring DNA sample to target plate\n")
    for line in data:
        description = line[1]
        well = line[0]
        volume = float(line[3])

        ctx.comment("Normalizing sample {}".format(description))

        if volume <= 20:
            p20.pick_up_tip()
            p20.transfer(volume,
                         target_plate.wells_by_name()[well],
                         water_well, new_tip="never")
            p20.transfer(volume,
                         dna_sample_plate.wells_by_name()[well],
                         target_plate.wells_by_name()[well], new_tip="never")
            p20.drop_tip()
        else:
            p300.pick_up_tip()
            p300.transfer(volume,
                         target_plate.wells_by_name()[well],
                         water_well, new_tip="never")
            p300.transfer(volume,
                         dna_sample_plate.wells_by_name()[well],
                         target_plate.wells_by_name()[well], new_tip="never")
            p300.drop_tip()
