from opentrons import protocol_api
import csv

# DNA concentration quantified samples normalization
metadata = {
    'protocolName': '466f93-5 - Automated LifeCell_NIPT_35Plex_HV',
    'author': 'Eskil Andersen <eskil.andersen@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.11'   # CHECK IF YOUR API LEVEL HERE IS UP TO DATE
                         # IN SECTION 5.2 OF THE APIV2 "VERSIONING"
}


def get_values(*names):
    import json
    _all_values = json.loads(
        """{"num_samples": 36,
            "normalization_csv": "well,concentration\\n1,3.6\\n2,3.63\\n3,5.86\\n4,1.75\\n5,1.19\\n6,2.77\\n7,1.63\\n8,5.16\\n9,5.63\\n10,1.62\\n11,1.78\\n12,4.56\\n13,1.6\\n14,1.7\\n15,1.32\\n16,2.93\\n17,1.27\\n18,1.03\\n19,4.62\\n20,3.67\\n21,1.35\\n22,3.74\\n23,5.51\\n24,4.06\\n25,4.66\\n26,4.65\\n27,2.18\\n28,3.65\\n29,3.03\\n30,1.37\\n31,4.54\\n32,5.5\\n33,1.55\\n34,3.26\\n35,4.12\\n36,2.54"
           }
        """)
    return [_all_values[n] for n in names]


def run(ctx: protocol_api.ProtocolContext):
    [
     num_samples,
     normalization_csv
    ] = get_values(  # noqa: F821 (<--- DO NOT REMOVE!)
        "num_samples",
        "normalization_csv")

    # load modules
    mag_mod = ctx.load_module('magnetic module gen2', '3')

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
    mag_bead_cleanup_plate \
        = mag_mod.load_labware('nest_96_wellplate_100ul_pcr_full_skirt',
                               'Magnetic module sample plate')
    SPRI_bead_plate \
        = ctx.load_labware('nest_96_wellplate_100ul_pcr_full_skirt', '9',
                           'Magnetic bead plate')
    reservoir \
        = ctx.load_labware('nest_12_reservoir_15ml', '6',
                           'Reagent reservoir')
    qubit_sample_plate \
        = ctx.load_labware('nest_96_wellplate_100ul_pcr_full_skirt', '1',
                           'quantification plate')
    PCR_amplified_sample_plate \
        = ctx.load_labware('nest_96_wellplate_100ul_pcr_full_skirt', '2',
                           'quantification plate')
    normalization_plate \
        = ctx.load_labware('nest_96_wellplate_100ul_pcr_full_skirt', '4',
                           'Normalization plate')

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
    water_well = reservoir.wells_by_name()['A2']

    qubit_sample_wells = qubit_sample_plate.wells()[0:num_samples]
    norm_destination_wells = normalization_plate.wells()[0:num_samples]
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
    # Load CSV into a Nx2 list of lists (LoL) (well, concentration [ng/µL])
    # Start by splitting by newline to get the rows
    csv_rows = normalization_csv.split("\n")
    norm_LoL = [[] for _ in range(num_samples+1)]  # +1 row for header
    for csv_row, norm_lol_row in zip(csv_rows[0:num_samples+1], norm_LoL):
        for cell in csv_row.split(","):
            norm_lol_row.append(cell)

    #  Find the min value in the LoL
    def key_func_norm_row(row):
        return row[1]

    min_conc = float(min(norm_LoL, key=key_func_norm_row)[1])

    ctx.comment("\n\nNormalizing DNA sample's concentration")
    for s_well, d_well, norm_LoL_row in zip(qubit_sample_wells,
                                            norm_destination_wells,
                                            norm_LoL[1:]):
        sample_vol = 10*(min_conc/float(norm_LoL_row[1]))
        water_vol = 10 - sample_vol
        p20.transfer(sample_vol, s_well, d_well)
        p20.transfer(water_vol, water_well, d_well)

    ctx.comment("\n\n~~~ End of protocol part 5 ~~~")
