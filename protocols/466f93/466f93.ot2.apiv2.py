"""End-repair reaction preparation."""
from opentrons import protocol_api
import math

# The first part of this protocol mixes the DNA samples with end repair
# buffer and enzyme and ends when the samples are ready for thermal incubation
metadata = {
    'protocolName': '466f93 - Automated LifeCell_NIPT_35Plex_HV',
    'author': 'Eskil Andersen <eskil.andersen@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.11'   # CHECK IF YOUR API LEVEL HERE IS UP TO DATE
                         # IN SECTION 5.2 OF THE APIV2 "VERSIONING"
}


def get_values(*names):
    import json
    _all_values = json.loads(
        """{ "pipette_l":"p20_single_gen2",
        "pipette_r":"p300_single_gen2",
        "plate_type":"azenta_96_wellplate_200ul",
        "reservoir_type":"nest_12_reservoir_15ml",
        "temperature_module":"temperature module gen2",
        "num_samples": 36,
        "magnetic_module":"magnetic module gen2"}
        """)
    return [_all_values[n] for n in names]


def run(ctx: protocol_api.ProtocolContext):
    """End-repair reaction preparation protocol entry point."""
    [
     num_samples
    ] = get_values(  # noqa: F821 (<--- DO NOT REMOVE!)
        "num_samples")

    if not 7 <= num_samples <= 36:
        raise Exception("The number of samples should be between 7 and 36")

    # define all custom variables above here with descriptions:
    ER_buffer_I_vol_per_well = 27
    ER_enz_vol_per_well = 126
    ER_buffer_per_sample = 1.5
    ER_enz_vol_per_sample = 0.75
    mastermix_vol_per_sample = ER_buffer_per_sample + ER_enz_vol_per_sample
    DNA_sample_transfer_vol = 12.75  # vol of DNA sample for rxn
    total_rxn_vol = mastermix_vol_per_sample + DNA_sample_transfer_vol

    n_standard_mixes = 10  # Standard number of times to mix a sample (10)
    well_plate_loadname = 'azenta_96_wellplate_200ul'
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

    yourgene_reagent_plate_I \
        = ctx.load_labware(well_plate_loadname, '7',
                           'Yourgene Reagent plate - 1')

    # DNA sample plate
    sample_plate = \
        ctx.load_labware(well_plate_loadname,
                         '4', "DNA Sample plate")

    # Destination plate - will be physically changed by the operator through-
    # out
    destination_plate = \
        ctx.load_labware(well_plate_loadname,
                         '1', "Destination plate 1")

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
    # Load left and right pipettes
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

    # End repair buffer - I is in column one of yourgene_reagent_plate_I
    # End repair enzyme is in well A2 of the sample plate
    ER_buffer_I_column = yourgene_reagent_plate_I.columns()[0]
    ER_enzyme_well = yourgene_reagent_plate_I.wells_by_name()['A2']
    ER_mastermix_destination = yourgene_reagent_plate_I.wells_by_name()['B2']
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
    # PROTOCOL BEGINS HERE

    # Prepare End Repair Mastermix
    # 1.2.7 - Mix end repair buffer I (column 1, prep plate 1) and End repair
    # enzyme I (in well pos. A2, prep plate 1) - mix by pipetting 10 times
    # Create a mastermix of the two
    # The mastermix will be placed in the unused well B2 of reagent plate I
    er_buffer_volume = ER_buffer_per_sample * (num_samples+1)
    er_enzyme_volume = ER_enz_vol_per_sample * (num_samples+1)

    for i in range(0, math.ceil(er_buffer_volume/ER_buffer_I_vol_per_well)):
        well = ER_buffer_I_column[i]
        # Mix the buffer 10x
        vol = (er_buffer_volume if er_buffer_volume
               < ER_buffer_I_vol_per_well else ER_buffer_I_vol_per_well)
        pip = p20 if vol < 20 else p300
        if not pip.has_tip:
            try:
                pip.pick_up_tip()
            except protocol_api.labware.OutOfTipsError:
                ctx.pause("Replace empty tip racks")
                pip.reset_tipracks()
                pip.pick_up_tip()
        pip.mix(n_standard_mixes, 20, well)
        pip.transfer(vol, well, ER_mastermix_destination, new_tip='never')
        er_buffer_volume = er_buffer_volume - vol

    drop_all_tips()

    # Mix the ER enzyme, total volume of enz. 126 µL,
    # max volume for mastermix is 0.75 µL*36=27 µL
    try:
        p300.pick_up_tip()
    except protocol_api.labware.OutOfTipsError:
        ctx.pause("Replace empty tip racks")
        p300.reset_tipracks()
        p300.pick_up_tip()
    p300.mix(n_standard_mixes, ER_enz_vol_per_well/2, ER_enzyme_well)
    p300.drop_tip()

    pip = p20 if er_enzyme_volume <= 20 else p300
    try:
        pip.transfer(er_enzyme_volume, ER_enzyme_well,
                     ER_mastermix_destination)
    except protocol_api.labware.OutOfTipsError:
        ctx.pause("Replace empty tip racks")
        pip.reset_tipracks()
        pip.transfer(er_enzyme_volume, ER_enzyme_well,
                     ER_mastermix_destination)

    # 1.2.7 to 1.2.9, page 2
    # Move 12.75 uL of sample to the destination plate
    # Add required volume of buffer and enzyme to the sample wells
    # See Table "End repair reaction" on page 2 of the protocol
    # This will use up one 20 uL tiprack
    ctx.comment("\nTransferring DNA")
    for s, d in zip(sample_plate.wells()[0:num_samples],
                    destination_plate.wells()[0:num_samples]):
        try:
            p20.transfer(DNA_sample_transfer_vol, s, d)
        except protocol_api.labware.OutOfTipsError:
            ctx.pause("Replace empty tip racks")
            p20.reset_tipracks()
            p20.transfer(DNA_sample_transfer_vol, s, d)

    # Transfer mastermix to each well and mix each sample ten times
    ctx.comment("\nTransferring End repair mastermix")
    for well in destination_plate.wells()[0:num_samples]:
        try:
            p20.pick_up_tip()
        except protocol_api.labware.OutOfTipsError:
            ctx.pause("Replace empty tip racks")
            p20.reset_tipracks()
            p20.pick_up_tip()
        p20.aspirate(mastermix_vol_per_sample, ER_mastermix_destination)
        p20.dispense(mastermix_vol_per_sample, well)
        # Mix each sample ten (n_standard_mixes) times
        p20.mix(n_standard_mixes, total_rxn_vol/2)
        p20.drop_tip()

    ctx.comment("\nPulse spin the destination plate for 5 seconds")
    ctx.comment("Perform the end repair reaction in the thermocycler")
    ctx.comment("Remember to thaw (30 minutes) and pulse spin Reagent plate " +
                "3 before inserting it for protocol part 2")
    ctx.comment("~~~ End of protocol part 1 ~~~~\n")
