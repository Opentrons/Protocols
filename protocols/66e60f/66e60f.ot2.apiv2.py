from opentrons import protocol_api
import re

metadata = {
    'protocolName': 'Normalization protocol',
    'author': 'Eskil Andersen <eskil.andersen@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.11'   # CHECK IF YOUR API LEVEL HERE IS UP TO DATE
                         # IN SECTION 5.2 OF THE APIV2 "VERSIONING"
}


def get_values(*names):
    import json
    _all_values = json.loads("""{
                                  "input_csv":"Plate,Well,SampleID,Concentration,VolumeToDispense\\nA,A1,SAMPLE1,10.5,13.2\\nA,H12,SAMPLE96,16.7,7.5\\nB,A1,SAMPLE97,18.2,5.6\\nB,H12,SAMPLE192,16.0,8.1",
                                  "source_type":"biorad_96_wellplate_200ul_pcr",
                                  "dest_type":"biorad_96_wellplate_200ul_pcr",
                                  "bin_tuberack_type":"opentrons_24_tuberack_nest_0.5ml_screwcap",
                                  "p300_type":"p300_multi_gen2"
                                  }
                                  """)
    return [_all_values[n] for n in names]


def run(ctx: protocol_api.ProtocolContext):

    [input_csv,
     source_type,
     dest_type,
     bin_tuberack_type,
     p300_type] = get_values(  # noqa: F821
     "input_csv",
     "source_type",
     "dest_type",
     "bin_tuberack_type",
     "p300_type")

    # define all custom variables above here with descriptions:
    left_pipette_loadname = 'p20_single_gen2'
    right_pipette_loadname = p300_type

    final_plate_loader_A = (dest_type, '6',
                            'Final plate A')
    final_plate_loader_B = (dest_type, '4',
                            'Final plate B')
    DNA_sample_plate_loader_A = (source_type, '9',
                                 'DNA plate A')
    DNA_sample_plate_loader_B = (source_type, '7',
                                 'DNA plate B')
    bins_tuberack_loader = (bin_tuberack_type, '5',
                            'binning tuberack')
    tiprack_300uL_loader = ('opentrons_96_filtertiprack_200ul', '10')
    tiprack_20uL_loader_A = ('opentrons_96_filtertiprack_20ul', '3')
    tiprack_20uL_loader_B = ('opentrons_96_filtertiprack_20ul', '1')

    reservoir_loader = ('nest_12_reservoir_15ml', '11', 'water reservoir')

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
    dna_sample_plate_A = ctx.load_labware(DNA_sample_plate_loader_A[0],
                                          DNA_sample_plate_loader_A[1],
                                          DNA_sample_plate_loader_A[2])
    dna_sample_plate_B = ctx.load_labware(DNA_sample_plate_loader_B[0],
                                          DNA_sample_plate_loader_B[1],
                                          DNA_sample_plate_loader_B[2])

    final_plate_A = ctx.load_labware(final_plate_loader_A[0],
                                     final_plate_loader_A[1],
                                     final_plate_loader_A[2])
    final_plate_B = ctx.load_labware(final_plate_loader_B[0],
                                     final_plate_loader_B[1],
                                     final_plate_loader_B[2])
    bin_tuberack = ctx.load_labware(bins_tuberack_loader[0],
                                    bins_tuberack_loader[1],
                                    bins_tuberack_loader[2])

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
    tiprack_20_filter_A = [ctx.load_labware(tiprack_20uL_loader_A[0],
                                            tiprack_20uL_loader_A[1])]
    tiprack_20_filter_B = [ctx.load_labware(tiprack_20uL_loader_B[0],
                                            tiprack_20uL_loader_B[1])]
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
                        tip_racks=tiprack_20_filter_A
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
    liquid_waste = reservoir.wells_by_name()['A2'].top(-2)

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
    # Find all wells and columns in the csv so that water dispension can
    # be limited to  those columns or wells

    # Lists of well names
    well_list_A = []
    well_list_B = []
    # Lists of well locations on the final plates
    wells_A = []
    wells_B = []
    i = 2
    for plate, well, _, _, _ in data:
        if plate == 'A':
            well_list_A.append(well)
        elif plate == 'B':
            well_list_B.append(well)
        else:
            raise Exception(("The plate name on line {} in the csv " +
                             "seems malformed: {}").
                            format(i, plate))
        i += 1

    # If the set and the list are not the same length there must be duplicates
    if len(well_list_A) != len(list(set(well_list_A))):
        raise Exception('Duplicate wells found for plate A, check your csv')
    if len(well_list_B) != len(list(set(well_list_B))):
        raise Exception('Duplicate wells found for plate B, check your csv')

    if 'single' in p300_type:
        wells_A = [final_plate_A.wells_by_name()[well] for well in well_list_A]
        wells_B = [final_plate_B.wells_by_name()[well] for well in well_list_B]

    col_set_A = []
    col_set_B = []
    if 'multi' in p300_type:
        col_list_A = [well[1:] for well in well_list_A]
        col_list_B = [well[1:] for well in well_list_B]
        # Create a a list of the set of all unique column values
        # and sort from lowest to highest column
        col_set_A = list(set(col_list_A))
        col_set_B = list(set(col_list_B))
        # Chaining sort() doesn't work
        col_set_A.sort()
        col_set_B.sort()
        wells_A = [final_plate_A.columns()[int(col)-1][0] for col in col_set_A]
        wells_B = [final_plate_B.columns()[int(col)-1][0] for col in col_set_B]

    p300.pick_up_tip()
    for wells, plate_name in zip([wells_A, wells_B], ['A', 'B']):
        if len(wells) > 0:
            ctx.comment("\nTransferring water to final plate {}\n".
                        format(plate_name))
            for well in wells:
                if p300.current_volume < initial_water_volume:
                    p300.aspirate(200-p300.current_volume, water_well)
                p300.dispense(initial_water_volume, well)
            p300.blow_out(water_well)
    p300.drop_tip()

    # Transfering DNA samples to target
    # ctx.comment("\nTransferring DNA sample to target plate\n")
    # for line in data:
        # well = line[0]
        # description = line[1]
        # concentration = line[2]
        # volume = float(line[3])
#
        # ctx.comment("Normalizing sample {} with concentration {}"
                    # .format(description, concentration))
        # pip = p20 if volume <= 20 or 'multi' in p300_type else p300
        # pip.pick_up_tip()
        # pip.transfer(volume,
                     # target_plate.wells_by_name()[well],
                     # liquid_waste, new_tip="never")
        # pip.transfer(volume,
                     # dna_sample_plate.wells_by_name()[well],
                     # target_plate.wells_by_name()[well], new_tip="never")
        # pip.mix(3, 20)
        # pip.blow_out(liquid_waste)
        # pip.drop_tip()
