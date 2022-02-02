"""DNA cleanup and PCR amplification protocol."""
from opentrons import protocol_api
import math

# Protocol part 3 - DNA cleanup and PCR amplification
metadata = {
    'protocolName': '466f93-3 - Automated LifeCell_NIPT_35Plex_HV',
    'author': 'Eskil Andersen <eskil.andersen@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.11'   # CHECK IF YOUR API LEVEL HERE IS UP TO DATE
                         # IN SECTION 5.2 OF THE APIV2 "VERSIONING"
}


def run(ctx: protocol_api.ProtocolContext):
    """DNA cleanup and PCR amplification protocol entry point."""
    [
     num_samples,
     mag_engage_time
    ] = get_values(  # noqa: F821 (<--- DO NOT REMOVE!)
        "num_samples",
        "mag_engage_time"
        )

    if not 7 <= num_samples <= 36:
        raise Exception("The number of samples should be between 7 and 36")

    # define all custom variables above here with descriptions:
    bead_volume = 25  # volume of bead solution for each sample
    bead_source_well_volume = 127
    ethanol_wash_vol = 75  # Volume of EtOH per bead wash
    water_resuspension_vol = 14  # Volume to resuspend SPRI beads in
    DNA_supernat_transfer_volume = 12  # Amount of DNA supernat. per PCR sample

    PCR_mastermix_vol_per_sample = 12.5  # Amount of mm per PCR sample
    PCR_mm_vol_per_source_well = 117  # Volume of mm per well in RP-I
    primer_vol_per_sample = 0.5  # Primer volume per PCR sample on dest plate
    # Combined PCR mastermix + primer mix per PCR sample`
    PCR_smm_vol_per_sample = \
        (PCR_mastermix_vol_per_sample + primer_vol_per_sample)

    PCR_sample_total_vol = 25  # Volume of DNA + super-mastermix

    n_standard_mixes = 10  # Standard number of times to mix a sample (10)
    # Standard number of times to mix mag soln. (25)
    n_bead_solution_mixes = 25

    well_plate_loadname = 'azenta_96_wellplate_200ul'

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
    yourgene_reagent_plate_I \
        = ctx.load_labware(well_plate_loadname, '7',
                           'Yourgene Reagent plate - 1')
    barcoded_sample_mag_plate \
        = mag_mod.load_labware(well_plate_loadname,
                               'Magnetic module sample plate (DP-2)')
    SPRI_bead_plate \
        = ctx.load_labware(well_plate_loadname, '9',
                           'Magnetic bead plate')
    reservoir \
        = ctx.load_labware('nest_12_reservoir_15ml', '6',
                           'Reagent reservoir')
    PCR_destination_plate \
        = ctx.load_labware(well_plate_loadname, '2',
                           'Destination plate 3 (DP-3) - PCR')

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
        except protocol_api.labware.protocol_api.labware.OutOfTipsError:
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
    # Volume Tracking
    class VolTracker:
        def __init__(self, labware, well_vol,
                     start=0, end=8,
                     mode='reagent', pip_type='single',
                     msg='Reset labware volumes'):
            """Voltracker tracks the volume(s) used in a piece of labware.

            Args:
                labware: The labware to track
                well_vol: The volume of the liquid in the wells
                pip_type: The pipette type used 'single' or 'multi'
                mode: 'reagent' or 'waste'
                start: The starting well
                end: The ending well
                msg: Message to send to the user when all wells are empty

            """
            self.labware_wells = dict.fromkeys(
                labware.wells()[start:end], 0)
            self.labware_wells_backup = self.labware_wells.copy()
            self.well_vol = well_vol
            self.pip_type = pip_type
            self.mode = mode
            self.start = start
            self.end = end
            self.msg = msg

        def tracker(self, vol):
            """
            Tracker() will track how much liquid was used up per well.

            If the volume of a given well is greater than self.well_vol
            it will remove it from the dictionary and iterate
            to the next well which will act as the reservoir.
            """
            well = next(iter(self.labware_wells))
            new_well = False
            if self.labware_wells[well] + vol >= self.well_vol:
                del self.labware_wells[well]
                if len(self.labware_wells) < 1:
                    ctx.pause(self.msg)
                    self.labware_wells = self.labware_wells_backup.copy()
                well = next(iter(self.labware_wells))
                new_well = True
            if self.pip_type == 'multi':
                self.labware_wells[well] = self.labware_wells[well] + vol*8
            elif self.pip_type == 'single':
                self.labware_wells[well] = self.labware_wells[well] + vol
            if self.mode == 'waste':
                ctx.comment(f'''{well}: {int(self.labware_wells[well])} uL of
                            total waste''')
            else:
                ctx.comment(f'''{int(self.labware_wells[well])} uL of liquid
                            used from {well}''')
            return well, new_well
    # reagents

    '''
    Define where all reagents are on the deck using the labware defined above.

    e.g.

    water = reservoir12.wells()[-1]
    waste = reservoir.wells()[0]
    samples = plate.rows()[0][0]
    dnase = tuberack.wells_by_name()['A4']

    '''
    ethanol = reservoir.wells_by_name()['A1']
    water_well = reservoir.wells_by_name()['A2']
    waste_well = reservoir.wells()[-1]
    bead_wells = VolTracker(SPRI_bead_plate, bead_source_well_volume, 0, 96)

    mag_plate_sample_wells = barcoded_sample_mag_plate.wells()[0:num_samples]
    PCR_dest_wells = PCR_destination_plate.wells()[0:num_samples]

    # PCR (super) mastermix is the predefined PCR mastermix + primers
    # Super-mastermix (smm) total volume could be up to 468 µL total (36*13)
    # This would also require an overage of 2*3 rxns = 13*3=39 µl
    # Final max volume = 468/200 = 2.34
    # ceil(2.34)=3, Maximally 3 wells will be needed for SMM
    PCR_smm_start_well = 9*8+2  # Well C10
    PCR_smm_end_well = 9*8+4  # Well E10

    # All wells available to make SMM in
    PCR_smm_wells = \
        yourgene_reagent_plate_I.wells()[PCR_smm_start_well:PCR_smm_end_well+1]
    # Super-mastermix wells that actually contain reagent (to be appended
    # as smm is made in those wells)
    PCR_smm_used_wells = []

    PCR_start_well = 80  # A11
    PCR_end_Well = 96  # H12
    PCR_mastermix_wells = \
        yourgene_reagent_plate_I.wells()[PCR_start_well:PCR_end_Well]

    PCR_primer_start = 9*8  # Well A10
    PCR_primer_end = 9*8+1  # Well B10
    PCR_primer_wells = \
        yourgene_reagent_plate_I.wells()[PCR_primer_start:PCR_primer_end]

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

    ctx.comment('\n\nAdding beads to samples and mixing\n')

    destination_wells = iter(mag_plate_sample_wells)
    well_1 = next(destination_wells)
    bead_well, _ = bead_wells.tracker(25)
    try:
        p300.pick_up_tip()
    except protocol_api.labware.OutOfTipsError:
        ctx.pause("Replace empty tip racks")
        p300.reset_tipracks()
        p300.pick_up_tip()
    p300.mix(n_bead_solution_mixes, 60, bead_well)
    p300.aspirate(bead_volume, bead_well)
    p300.dispense(bead_volume, well_1)
    p300.mix(n_standard_mixes, 25, well_1)
    p300.drop_tip()

    for d_well in destination_wells:
        bead_well, is_new_well = bead_wells.tracker(25)
        try:
            p300.pick_up_tip()
        except protocol_api.labware.OutOfTipsError:
            ctx.pause("Please replace 200 uL tipracks before continuing\n")
            p300.reset_tipracks()
            p300.pick_up_tip()
        if is_new_well:
            p300.mix(n_bead_solution_mixes, 60, bead_well)
        p300.aspirate(bead_volume, bead_well)
        p300.dispense(bead_volume, d_well)
        p300.mix(n_standard_mixes, 25, d_well)
        p300.drop_tip()

    ctx.comment("\n\nRemember to seal bead strips")
    ctx.delay(0, 5, "Incubating samples with beads")
    ctx.pause("\n\nPulse spin plate for 5 seconds")
    ctx.comment("\n\nEngaging magnets")
    mag_mod.engage()
    ctx.delay(0, mag_engage_time, "binding samples to beads")

    ctx.comment("\n\nDiscarding supernatant")
    for source_well in mag_plate_sample_wells:
        try:
            p300.transfer(50, source_well, waste_well)
        except protocol_api.labware.OutOfTipsError:
            ctx.pause("Please replace 200 uL tipracks before continuing\n")
            p300.reset_tipracks()
            p300.transfer(50, source_well, waste_well)

    # Wash beads in 80 % ethanol x 2
    for i in range(0, 2):
        for dest_well in mag_plate_sample_wells:
            try:
                p300.transfer(ethanol_wash_vol, ethanol, dest_well)
            except protocol_api.labware.OutOfTipsError:
                ctx.pause("Please replace 200 uL tipracks before continuing\n")
                p300.reset_tipracks()
                p300.transfer(ethanol_wash_vol, ethanol, dest_well)

        ctx.delay(30, 0, "\n\nIncubation #{} in 80% EtOH\n".format(i+1))
        for source_well in mag_plate_sample_wells:
            try:
                p300.transfer(ethanol_wash_vol, source_well, waste_well)
            except protocol_api.labware.OutOfTipsError:
                ctx.pause("Please replace 200 uL tipracks before continuing\n")
                p300.reset_tipracks()
                p300.transfer(ethanol_wash_vol, source_well, waste_well)

    mag_mod.disengage()
    ctx.pause("\n\nPulse spin the plate for 5 seconds and replace\n")

    # Remove spun-down supernatant
    mag_mod.engage()
    ctx.delay(0, mag_engage_time, "Attracting beads to magnets")
    for source_well in mag_plate_sample_wells:
        try:
            p300.transfer(ethanol_wash_vol, source_well, waste_well)
        except protocol_api.labware.OutOfTipsError:
            ctx.pause("Please replace 200 uL tipracks before continuing\n")
            p300.reset_tipracks()
            p300.transfer(ethanol_wash_vol, source_well, waste_well)

    ctx.comment("\n\nAir drying beads")
    ctx.delay(0, 5)

    ctx.comment("\n\nResuspending DNA samples in {} uL of nuc. free water\n".
                format(water_resuspension_vol))
    # Resuspend DNA/bead samples in water
    for well in mag_plate_sample_wells:
        try:
            p20.pick_up_tip()
        except protocol_api.labware.OutOfTipsError:
            ctx.pause("Please replace 20 uL tipracks before continuing\n")
            p20.reset_tipracks()
            p20.pick_up_tip()
        p20.aspirate(water_resuspension_vol, water_well)
        p20.dispense(water_resuspension_vol, well)
        p20.mix(n_standard_mixes, 10, well)
        p20.drop_tip()

    ctx.comment("Incubating beads in water")
    ctx.delay(0, 3)
    mag_mod.disengage()
    ctx.pause("Pulse spin the sample/bead plate for 5 seconds, then place " +
              "it back on the magnetic module")
    ctx.comment("Attracting beads")
    mag_mod.engage()
    ctx.delay(0, mag_engage_time)

    # Transfer the bead supernatant to the PCR destination plate
    ctx.comment("\n\nTransferring DNA supernatant to PCR plate")
    for s_well, d_well in zip(mag_plate_sample_wells, PCR_dest_wells):
        try:
            p20.transfer(DNA_supernat_transfer_volume, s_well, d_well)
        except protocol_api.labware.OutOfTipsError:
            ctx.pause("Please replace 20 uL tipracks before continuing\n")
            p20.reset_tipracks()
            p20.transfer(DNA_supernat_transfer_volume, s_well, d_well)

    # Create a PCR (super)mastermix from the PCR mastermix and the primers
    ctx.comment("\n\nCreating PCR Mastermix\n")
    # Total volume of PCR mastermix needed for the samples
    PCR_mm_total_vol = num_samples * PCR_mastermix_vol_per_sample
    # Total volume of PCR primer mix needed for the samples
    PCR_primer_total_vol = num_samples * primer_vol_per_sample
    # Total vol of super-mastermix (mastermix + primer mix) for the samples
    smm_total_vol = PCR_mm_total_vol + PCR_primer_total_vol
    # Number of smm reactions that fit into one well
    smm_rxns_per_well = math.floor(200/PCR_smm_vol_per_sample)
    # How many wells are needed for the super-mastermix
    n_super_mm_wells = math.ceil((smm_total_vol)/200)
    # One excess reaction per smm well to account for any
    # negative errors in total volume
    # An overage of two reactions will be created per well
    n_total_rxns = (math.ceil(smm_total_vol/PCR_smm_vol_per_sample) +
                    n_super_mm_wells*2)

    PCR_mm_iter = iter(PCR_mastermix_wells)
    PCR_mm_well = next(PCR_mm_iter)
    smm_well_iterator = iter(PCR_smm_wells)

    rxns_left = n_total_rxns

    try:
        p300.pick_up_tip()
    except protocol_api.labware.OutOfTipsError:
        ctx.pause("Please replace empty 200 uL tipracks")
        p300.pick_up_tip()
    p300.mix(n_standard_mixes, PCR_mm_vol_per_source_well/2, PCR_mm_well)
    vol_left_in_PCR_mm_well = PCR_mm_vol_per_source_well-1

    try:
        p20.pick_up_tip()
    except protocol_api.labware.OutOfTipsError:
        ctx.pause("Please replace empty 20 uL tipracks")
        p20.pick_up_tip()
    p20.mix(n_standard_mixes, 20, PCR_primer_wells[0])

    drop_all_tips()

    # Create smm in as many wells as needed
    while(rxns_left > 0):
        d_well = next(smm_well_iterator)
        n_rxns_this_well = (rxns_left if rxns_left < smm_rxns_per_well
                            else smm_rxns_per_well)
        # Transfer PCR mastermixc
        PCR_mm_vol_this_well = n_rxns_this_well * PCR_mastermix_vol_per_sample
        while PCR_mm_vol_this_well > 0:
            if vol_left_in_PCR_mm_well < PCR_mastermix_vol_per_sample:
                PCR_mm_well = next(PCR_mm_iter)
                vol_left_in_PCR_mm_well = PCR_mm_vol_per_source_well-1
                # Mix the well before use
                try:
                    p300.pick_up_tip()
                except protocol_api.labware.OutOfTipsError:
                    ctx.pause("Please replace empty 200 uL tipracks")
                    p300.pick_up_tip()
                p300.mix(n_standard_mixes, PCR_mm_vol_per_source_well/2,
                         PCR_mm_well)
                p300.drop_tip()
            pip = p20 if PCR_mm_vol_this_well < 20 else p300
            vol = (vol_left_in_PCR_mm_well if PCR_mm_vol_this_well >
                   vol_left_in_PCR_mm_well else PCR_mm_vol_this_well)
            if pip.has_tip:
                pip.drop_tip()
            try:
                pip.transfer(vol, PCR_mm_well, d_well)
            except protocol_api.labware.OutOfTipsError:
                ctx.pause("Please replace empty tipracks before continuing\n")
                pip.reset_tipracks()
                pip.transfer(vol, PCR_mm_well, d_well)
            vol_left_in_PCR_mm_well = vol_left_in_PCR_mm_well - vol
            PCR_mm_vol_this_well = PCR_mm_vol_this_well - vol

        # Transfer primer mix (max primer vol =36*0.5 < primer_vol_per_well)
        # Therefore we can use one well for everything
        # Max volume of primer per smm well: 7.5 uL - using the p20 for tfer.
        primer_transfer_vol = n_rxns_this_well * primer_vol_per_sample
        p20.transfer(primer_transfer_vol, PCR_primer_wells[0], d_well)
        rxns_left = rxns_left - n_rxns_this_well
        PCR_smm_used_wells.append(d_well)

        # Mix the smm
        vol = (n_rxns_this_well*PCR_smm_vol_per_sample)/2
        pip = p20 if vol <= 20 else p300
        try:
            pip.pick_up_tip()
        except protocol_api.labware.OutOfTipsError:
            ctx.pause("Please replace empty tipracks")
            pip.pick_up_tip()
        pip.mix(n_standard_mixes, vol, d_well)

    # Distribute smm to DNA sample wells
    PCR_smm_tracker = \
        VolTracker(yourgene_reagent_plate_I, 200-2*PCR_smm_vol_per_sample,
                   PCR_smm_start_well,
                   PCR_smm_start_well+len(PCR_smm_wells),
                   msg="Out of super-mastermix")

    for d_well in PCR_dest_wells:
        smm_well, _ = PCR_smm_tracker.tracker(PCR_smm_vol_per_sample)
        try:
            p20.pick_up_tip()
        except protocol_api.labware.OutOfTipsError:
            ctx.pause("Please replace empty 20 uL tipracks")
            p20.pick_up_tip()
        p20.transfer(PCR_smm_vol_per_sample, smm_well, d_well,
                     new_tip="never")
        p20.mix(n_standard_mixes, PCR_sample_total_vol/2, d_well)
        p20.drop_tip()
    ctx.comment("\n\nTransfer the Yourgene cfdna reagent plate I back to " +
                "the freezer")
    ctx.comment("Pulse spin the PCR sample plate (DP-3) for 5 seconds and " +
                "transfer to the thermocycler and run the cycle " +
                "described in 1.2.47")
    ctx.comment("\n\n~~~ End of protocol part 3 ~~~")
