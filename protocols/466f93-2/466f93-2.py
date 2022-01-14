from opentrons import protocol_api
import math

metadata = {
    'protocolName': '466f93-2 - Automated LifeCell_NIPT_35Plex_HV',
    'author': 'Eskil Andersen <eskil.andersen@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.11'   # CHECK IF YOUR API LEVEL HERE IS UP TO DATE
                         # IN SECTION 5.2 OF THE APIV2 "VERSIONING"
}


def get_values(*names):
    import json
    _all_values = json.loads(
        """{"num_samples": 36,
            "barcode_csv": "sample_well,barcode_well\\n1,31\\n2,26\\n3,54\\n4,2\\n5,9\\n6,52\\n7,54\\n8,30\\n9,29\\n10,48\\n11,35\\n12,42\\n13,26\\n14,35\\n15,11\\n16,54\\n17,27\\n18,37\\n19,9\\n20,40\\n21,56\\n22,54\\n23,31\\n24,16\\n25,54\\n26,40\\n27,51\\n28,31\\n29,7\\n30,50\\n31,49\\n32,10\\n33,47\\n34,15\\n35,11\\n36,44"}
        """)
    return [_all_values[n] for n in names]


def run(ctx: protocol_api.ProtocolContext):

    [
     num_samples,
     barcode_csv
    ] = get_values(  # noqa: F821 (<--- DO NOT REMOVE!)
        "num_samples",
        "barcode_csv")

    n_standard_mixes = 1  # Standard number of mixes, 10 in the bench ptcl.

    # define all custom variables above here with descriptions:
    ALB_vol_per_sample = 2.50  # Addaptor ligation buffer
    ALB_vol_per_well = 45

    ALE_I_vol_per_sample = 1.50  # Adaptor ligation enzyme I
    ALE_I_vol_per_well = 27

    ALE_II_vol_per_sample = 0.25  # Adaptor ligation enzyme II
    ALE_II_vol_per_well = 39

    water_vol_per_sample = 3.75  # Volume of water per sample for AL rxn

    end_repaired_sample_vol = 15  # 15 uL to be mixed with 8 uL mastermix
    mastermix_vol_per_sample = 8

    barcode_vol_per_sample = 2  # Add 2 uL of barcode to each sample
    csv_rows = barcode_csv.split("\n")
    # +1 row for the CSV header
    barcoding_LoL = [[None, None] for _ in range(num_samples+1)]
    barcoding_LoL[0] = csv_rows[0].split(",")
    for csv_row, barcode_row in zip(csv_rows[1:num_samples+1],
                                    barcoding_LoL[1:]):
        dest_well, barcode_well = [int(cell) for cell in csv_row.split(",")]

        # Validate the data
        if (barcode_well < 0 or (barcode_well > 16 and barcode_well < 25) or
                barcode_well > 56):
            raise ValueError("""The barcode well index is invalid (#{})
                             for sample well #{}. Please correct your CSV
                             input file.""".
                             format(barcode_well, dest_well))
        if dest_well < 0:
            raise ValueError("The CSV sample well index is less than 0, " +
                             "well index:{} """.format(dest_well))
        if dest_well > num_samples:
            raise ValueError("The CSV sample well index value is greater " +
                             "than the total number of samples: {}".
                             format(dest_well))

        barcode_row[0] = dest_well
        barcode_row[1] = barcode_well

    # load modules

    '''

    Add your modules here with:

    module_name = ctx.load_module('{module_loadname}', '{slot number}')

    Note: if you are loading a thermocycler, you do not need to specify
    a slot number - thermocyclers will always occupy slots 7, 8, 10, and 11.

    For all other modules, you can load them on slots 1, 3, 4, 6, 7, 9, 10.

    '''
    mag_mod = ctx.load_module('magnetic module gen2', '3')

    # load labware

    '''

    Add your labware here with:

    labware_name = ctx.load_labware('{loadname}', '{slot number}')

    If loading labware on a module, you can load with:

    labware_name = module_name.load_labware('{loadname}')
    where module_name is defined above.

    '''
    yourgene_reagent_plate_I \
        = ctx.load_labware('nest_96_wellplate_100ul_pcr_full_skirt', '7',
                           'Reagent Plate - I')

    yourgene_reagent_plate_III \
        = ctx.load_labware('nest_96_wellplate_100ul_pcr_full_skirt', '2',
                           'Reagent Plate - III - Barcodes')
    end_repaired_sample_plate \
        = ctx.load_labware('nest_96_wellplate_100ul_pcr_full_skirt', '1',
                           'End repaired sample plate')
    reservoir \
        = ctx.load_labware('nest_12_reservoir_15ml', '6',
                           'Reagent reservoir')
    destination_plate \
        = mag_mod.load_labware('nest_96_wellplate_100ul_pcr_full_skirt',
                               'Destination plate')

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
    tiprack20s = [ctx.load_labware('opentrons_96_filtertiprack_20ul', slot)
                  for slot in ['10', '11']]
    tiprack200s = [ctx.load_labware('opentrons_96_filtertiprack_200ul', slot)
                   for slot in ['5', '8']]

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
    p20 = ctx.load_instrument("p20_single_gen2", "left", tip_racks=tiprack20s)
    p300 = ctx.load_instrument("p300_single_gen2", "right",
                               tip_racks=tiprack200s)

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
    def drop_all_tips():
        for pip in [p20, p300]:
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

    # reagents

    '''
    Define where all reagents are on the deck using the labware defined above.

    e.g.

    water = reservoir12.wells()[-1]
    waste = reservoir.wells()[0]
    samples = plate.rows()[0][0]
    dnase = tuberack.wells_by_name()['A4']

    '''

    water_well = reservoir.wells()[1]
    ALB_I_column = yourgene_reagent_plate_I.columns()[2]
    ALE_I_column = yourgene_reagent_plate_I.columns()[3]
    ALE_II_well = yourgene_reagent_plate_I.wells_by_name()['A5']
    # Mastermix could be up to 288 uL, might need 2 wells
    mastermix_wells = yourgene_reagent_plate_I.columns()[4][1:3]

    end_repaired_sample_wells = \
        end_repaired_sample_plate.wells()[0:num_samples]
    destination_wells = destination_plate.wells()[0:num_samples]

    # Every other well starting at B6 ending at H9
    barcodes_plate_I = yourgene_reagent_plate_I.wells()[41:72:2]
    barcode_plate_I_vol = 21

    barcodes_plate_III = yourgene_reagent_plate_III.wells()[1:64:2]

    all_barcodes = barcodes_plate_I.copy()

    # There is a gap between plate I and plate II in barcode numbering.
    # On plate I they end on 16, and on III they begin with 25
    # Add the in-betweens as empty entries
    for i in range(17, 25):
        all_barcodes.append(None)

    for well in barcodes_plate_III:
        all_barcodes.append(well)

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
    ctx.comment('\nCreating Adaptor Ligation Mastermix')
    # The nastermix is 4 components: water, AL buffer I, AL enzyme I & II

    # Mastermix is put into well B5 and possibly C5 depending on total volume
    # Each well holds a max of 200 uL. Max volume of mastermix is 296
    # Each well may hold up to 25 reaction volumes (200/8=25)
    # There should be one excess MM volume in each well so there's no risk
    # of any reaction getting less volume than needed.

    n_wells = math.ceil(num_samples/24)
    mastermix_counter = num_samples
    ALB_I_iter = iter(ALB_I_column)
    ALE_I_iter = iter(ALE_I_column)
    ALE_II_is_mixed = False

    for i in range(0, n_wells):
        mastermix_multiples = \
            (25 if mastermix_counter > 24 else mastermix_counter+1)
        water_vol = mastermix_multiples * water_vol_per_sample
        pip = p20 if water_vol <= 20 else p300
        try:
            pip.transfer(water_vol, water_well, mastermix_wells[i])
        except protocol_api.labware.OutOfTipsError:
            ctx.pause("Replace empty tip racks")
            pip.reset_tipracks()
            pip.transfer(water_vol, water_well, mastermix_wells[i])

        ALB_I_vol = mastermix_multiples * ALB_vol_per_sample
        ALE_I_vol = mastermix_multiples * ALE_I_vol_per_sample

        # Add AL Buffer I and AL Enzyme I from their source columns
        for vol, vol_per_well, mix_vol, s_iter \
                in zip([ALB_I_vol, ALE_I_vol],
                       [ALB_vol_per_well, ALE_I_vol_per_well],
                       [ALB_vol_per_well/2, 20.0],
                       [ALB_I_iter, ALE_I_iter]):
            while True:
                well = next(s_iter)
                if not p300.has_tip:
                    try:
                        p300.pick_up_tip()
                    except protocol_api.labware.OutOfTipsError:
                        ctx.pause("Replace empty tip racks")
                        p300.reset_tipracks()
                        p300.pick_up_tip()
                p300.mix(n_standard_mixes, mix_vol, well)
                if vol > (vol_per_well-1):
                    p300.transfer(vol_per_well-1, well, mastermix_wells[i],
                                  new_tip='never')
                    vol = vol - (vol_per_well-1)
                else:
                    pip = p20 if vol <= 20 else p300
                    if not pip.has_tip:
                        try:
                            pip.pick_up_tip()
                        except protocol_api.labware.OutOfTipsError:
                            ctx.pause("Replace empty tip racks")
                            pip.reset_tipracks()
                            pip.pick_up_tip()
                    pip.transfer(vol, well, mastermix_wells[i],
                                 new_tip='never')
                    drop_all_tips()
                    break

        # Add Adaptor Ligation Enzyme II to mastermix_wells
        # Max volume transfer per mastermix well: 0.25 uL * 25 = 6.25 uL
        ALE_II_vol = mastermix_multiples * ALE_II_vol_per_sample
        if not ALE_II_is_mixed:
            try:
                p20.pick_up_tip()
            except protocol_api.labware.OutOfTipsError:
                ctx.pause("Replace empty tip racks")
                p20.reset_tipracks()
                p20.pick_up_tip()
            p20.mix(n_standard_mixes, ALE_II_vol_per_well/2, ALE_II_well)
            p20.transfer(ALE_II_vol, ALE_II_well, mastermix_wells[i],
                         new_tip='never')
            ALE_II_is_mixed = True
        else:
            try:
                p20.transfer(ALE_II_vol, ALE_II_well, mastermix_wells[i])
            except protocol_api.labware.OutOfTipsError:
                ctx.pause("Replace empty tip racks")
                p20.reset_tipracks()
                p20.pick_up_tip()

        # Mix the mastermix 10x
        mm_well_volume = 8 * mastermix_multiples
        pip = p20 if mm_well_volume/2 <= 20 else p300
        if not pip.has_tip:
            try:
                pip.pick_up_tip()
            except protocol_api.labware.OutOfTipsError:
                ctx.pause("Replace empty tip racks")
                pip.reset_tipracks()
                pip.pick_up_tip()
        pip.mix(n_standard_mixes, mm_well_volume/2, mastermix_wells[i])
        drop_all_tips()
        mastermix_counter = mastermix_counter - 24

    ctx.comment("\n\nMixing end-repaired samples and AL mastermix")

    # Transfer mastermix to samples
    mm_iter = iter(mastermix_wells)
    n_mastermix_wells = math.ceil(num_samples/24)
    n_transfers = num_samples
    try:
        p20.pick_up_tip()
    except protocol_api.labware.OutOfTipsError:
        ctx.pause("Replace empty tip racks")
        p20.reset_tipracks()
        p20.pick_up_tip()
    print(n_mastermix_wells)
    for i in range(0, n_mastermix_wells):
        transfers_in_well = 24 if n_transfers >= 24 else n_transfers
        s_well = next(mm_iter)
        for j in range(i*24, i*24+transfers_in_well):
            p20.transfer(mastermix_vol_per_sample, s_well,
                         destination_wells[j], new_tip='never')
        n_transfers = n_transfers - transfers_in_well
    p20.drop_tip()

    ctx.comment("\n\nTransferring DNA samples")
    # Transfer the samples from the end repaired plate to target
    for s_well, d_well in zip(end_repaired_sample_wells, destination_wells):
        try:
            p20.transfer(end_repaired_sample_vol, s_well, d_well)
        except protocol_api.labware.OutOfTipsError:
            ctx.pause("Replace empty tip racks")
            pipette.reset_tipracks()
            p20.transfer(end_repaired_sample_vol, s_well, d_well)

    # Parse the csv data that defines which barcode well contents gets mixed
    # with which sample. Data is loaded in csv LoL (list of lists)
    # where each sub-list contains the sample well number and the barcode
    # well number

    # The assumption according to the customer is that each barcode well
    # will be used only once (although the test csv input may have duplicates
    # since it was auto-generated)
    for row in barcoding_LoL[1:]:
        try:
            dest_index = int(row[0])-1
            dest_well = destination_wells[dest_index]  # -1 bc. array 0-based

            barcode_index = int(row[1])-1
            barcode_well = all_barcodes[barcode_index]
        except IndexError:
            ctx.comment("""Index out of bounds. dest index: {},
                        barcode index:{}""".format(dest_index, barcode_index))
        try:
            p20.pick_up_tip()
        except protocol_api.labware.OutOfTipsError:
            ctx.pause("Replace empty tip racks")
            p20.reset_tipracks()
            p20.pick_up_tip()
        ctx.comment("\nPipetting barcode #{} into sample #{}\n".
                    format(barcode_index, dest_index))
        p20.mix(n_standard_mixes, 15, barcode_well)
        p20.aspirate(barcode_vol_per_sample, barcode_well)
        p20.dispense(barcode_vol_per_sample,
                     dest_well)
        # Last pipetting operation before PCR, so mix the sample wells now
        p20.mix(n_standard_mixes, 25/2, dest_well)
        p20.drop_tip()

    ctx.pause("\n\nPulse spin the destination plate for 5 seconds")
    ctx.comment("Perform PCR step")
    ctx.comment("~~~ End of protocol part 2 ~~~")
