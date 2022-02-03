"""DNA cleanup and quantification prep."""
from opentrons import protocol_api
import math

# Post PCR bead cleanup and then preparation for Qubit HS DNA quantification
metadata = {
    'protocolName': '466f93-4 - Automated LifeCell_NIPT_35Plex_HV',
    'author': 'Eskil Andersen <eskil.andersen@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.11'   # CHECK IF YOUR API LEVEL HERE IS UP TO DATE
                         # IN SECTION 5.2 OF THE APIV2 "VERSIONING"
}


def get_values(*names):
    import json
    _all_values = json.loads(
        """{
           "num_samples": 36,
           "mag_engage_time": 5
           }
        """)
    return [_all_values[n] for n in names]


def run(ctx: protocol_api.ProtocolContext):
    """Protocol entry point."""
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
    # Bead starting well: Since some of the bead wells have been used
    # in step 3 of the protocols we need to calculate which bead well to start
    # from
    bead_vol_per_sample_part3 = 25  # 25 µL per sample in step 3
    bead_vol_per_sample = 25  # Bead solution volume for this protocol
    bead_source_well_volume = 127
    n_bead_mixes = 25  # Number of times to mix each bead well before use
    bead_starting_well_offset = 1 + \
        math.ceil(
            num_samples*bead_vol_per_sample_part3/bead_source_well_volume)
    # Starting well to aspirate SPRI beads from on the bead plate
    bead_start_well = bead_starting_well_offset

    # Volume of PCR amplified DNA to transfer to the mag plate for cleanup
    PCR_amp_DNA_sample_vol = 25

    supernatant_removal_volume = 50
    ethanol_wash_vol = 75  # 2x75 µL washes with 80 % ethanol
    water_resuspension_vol = 22  # H2O vol to resusd. after EtOH washx2

    DNA_supernatant_transfer_vol = 20  # volume of cleaned DNA for PCR plate
    qubit_ws_vol_per_sample = 198  # QWS per DNA sample to be quant.
    qubit_working_sol_vol = num_samples*qubit_ws_vol_per_sample

    qubit_assay_dna_vol = 2  # volume of DNA to mix w/ QWS

    well_plate_loadname = 'azenta_96_wellplate_200ul'

    # load modules
    mag_mod = ctx.load_module('magnetic module gen2', '3')

    mag_engage_height = 13.5

    '''

    Add your modules here with:

    module_name = ctx.load_module('{module_loadname}', '{slot number}')

    Note: if you are loading a thermocycler, you do not need to specify
    a slot number - thermocyclers will always occupy slots 7, 8, 10, and 11.

    For all other modules, you can load them on slots 1, 3, 4, 6, 7, 9, 10.

    '''

    # load labware
    mag_bead_cleanup_plate \
        = mag_mod.load_labware(well_plate_loadname,
                               'Magnetic module sample plate (DP-4)')
    SPRI_bead_plate \
        = ctx.load_labware(well_plate_loadname, '9',
                           'Magnetic bead well plate')
    reservoir \
        = ctx.load_labware('nest_12_reservoir_15ml', '6',
                           'Reagent reservoir')
    quantification_destination_plate \
        = ctx.load_labware(well_plate_loadname, '1',
                           'quantification plate (DP-5)')
    PCR_amplified_sample_plate \
        = ctx.load_labware(well_plate_loadname, '2',
                           'sample plate (DP-3)')

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
            Tracker function: Track well volume and switch when too low to use.

            Tracker() will track how much liquid
            was used up per well. If the volume of
            a given well is greater than self.well_vol
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

    def engage_magnets():
        nonlocal mag_mod, mag_engage_height
        mag_mod.engage(height_from_base=mag_engage_height)

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
    qubit_ws_tracker = VolTracker(reservoir, qubit_working_sol_vol, 2, 3)

    bead_well_tracker = VolTracker(SPRI_bead_plate, bead_source_well_volume,
                                   bead_start_well, 96)

    mag_plate_sample_wells = mag_bead_cleanup_plate.wells()[0:num_samples]
    PCR_amp_sample_wells = PCR_amplified_sample_plate.wells()[0:num_samples]
    quant_DNA_sample_wells = \
        quantification_destination_plate.wells()[0:num_samples]

    # Use the wells starting at column 6 to the end for mixing DNA
    # With Qubit HS working solution (8*5+1=41 [=40 with 0-inclusive index])
    qubit_quant_wells = \
        quantification_destination_plate.wells()[40:40+num_samples]
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
    ctx.comment("\n\nTransferring PCR amplified DNA to magnetic cleanup plate")
    for s_well, d_well in zip(PCR_amp_sample_wells,
                              mag_plate_sample_wells):
        try:
            p300.transfer(PCR_amp_DNA_sample_vol, s_well, d_well)
        except protocol_api.labware.OutOfTipsError:
            ctx.pause("Please replace empty 200 uL tipracks")
            p300.transfer(PCR_amp_DNA_sample_vol, s_well, d_well)

    ctx.comment("\n\nMixing and transferring beads to the samples")

    bead_well, _ = bead_well_tracker.tracker(bead_vol_per_sample)
    try:
        p300.pick_up_tip()
    except protocol_api.labware.OutOfTipsError:
        ctx.pause("Please replace empty 200 uL tipracks")
        p300.pick_up_tip()
    p300.mix(n_bead_mixes, bead_source_well_volume/2, bead_well)

    for d_well in mag_plate_sample_wells:
        bead_well, is_new_well = bead_well_tracker.tracker(bead_vol_per_sample)
        if is_new_well:
            if not p300.has_tip:
                try:
                    p300.pick_up_tip()
                except protocol_api.labware.OutOfTipsError:
                    ctx.pause("Please replace empty 200 uL tipracks")
                    p300.pick_up_tip()
            p300.mix(n_bead_mixes, bead_source_well_volume/2, bead_well)
        try:
            if not p300.has_tip:
                p300.pick_up_tip()
        except protocol_api.labware.OutOfTipsError:
            ctx.pause("Please replace empty 200 uL tipracks")
            if not p300.has_tip:
                p300.pick_up_tip()
        p300.aspirate(bead_vol_per_sample, bead_well)
        p300.dispense(bead_vol_per_sample, d_well)
        p300.drop_tip()

    ctx.comment("\n\nIncubating samples")
    ctx.delay(0, 5)
    ctx.pause("\n\nPulse spin bead/sample plate for 5s before continuing")

    ctx.comment("\n\nEngaging magnets for {} minutes".
                format(mag_engage_time))
    engage_magnets()
    ctx.delay(0, mag_engage_time)

    ctx.comment("\n\nRemoving supernatant\n")
    for dest_well in mag_plate_sample_wells:
        try:
            p300.transfer(supernatant_removal_volume, dest_well, waste_well)
        except protocol_api.labware.OutOfTipsError:
            ctx.pause("Please replace empty 200 uL tipracks")
            p300.transfer(supernatant_removal_volume, dest_well, waste_well)

    ctx.comment("\n\nWashing beads with 80% ethanol")
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
    ctx.pause("\n\nPulse spin the sample plate on the magnetic module for " +
              "5 seconds, then place it back on the magnetic module")
    engage_magnets()
    ctx.delay(0, mag_engage_time, "Binding the beads to the magnets")
    ctx.comment("\n\nRemoving remaining wash supernatant from the wells\n")
    for dest_well in mag_plate_sample_wells:
        try:
            p20.transfer(20, dest_well, waste_well)
        except protocol_api.labware.OutOfTipsError:
            ctx.pause("Please replace empty 200 uL tipracks")
            p20.transfer(20, dest_well, waste_well)

    ctx.delay(0, 5, "Drying the beads")

    # Resuspend, mix and incubate beads in water
    for well in mag_plate_sample_wells:
        pip = p20 if water_resuspension_vol <= 20 else p300
        try:
            pip.pick_up_tip()
        except protocol_api.labware.OutOfTipsError:
            ctx.pause("Please replace empty tipracks before continuing\n")
            pip.reset_tipracks()
            pip.pick_up_tip()
        pip.aspirate(water_resuspension_vol, water_well)
        pip.dispense(water_resuspension_vol, well)
        pip.mix(5, 10, well)
        pip.drop_tip()

    ctx.comment("Incubating beads in water")
    ctx.delay(0, 3)
    ctx.pause("Pulse spin the sample/bead plate for 5 seconds, then place " +
              "it back on the magnetic module")
    ctx.comment("Attracting beads")
    ctx.delay(0, mag_engage_time)
    ctx.comment("\n\nTransferring DNA containing supernatant to quant. plate")

    # Transfer DNA containing bead well supernatant to quantification plate
    pip = p20 if DNA_supernatant_transfer_vol <= 20 else p300
    for s_well, d_well in zip(mag_plate_sample_wells,
                              quant_DNA_sample_wells):
        try:
            pip.transfer(DNA_supernatant_transfer_vol, s_well, d_well)
        except protocol_api.labware.OutOfTipsError:
            ctx.pause("Please replace empty tipracks before continuing\n")
            pip.reset_tipracks()
            pip.transfer(DNA_supernatant_transfer_vol, s_well, d_well)

    # Prepare quant. samples for quantification with Qubit HS kit
    qubit_ws_well, _ = qubit_ws_tracker.tracker(0)

    try:
        p300.pick_up_tip()
    except protocol_api.labware.OutOfTipsError:
        ctx.pause("Please replace empty tipracks before continuing\n")
        p300.reset_tipracks()
        p300.pick_up_tip()
    p300.mix(10, 200, qubit_ws_well)

    # Mix quant. samples with Qubit working solution
    # First, distribute the QWS
    for d_well in qubit_quant_wells:
        p300.transfer(qubit_ws_vol_per_sample, qubit_ws_well, d_well,
                      new_tip='never')
    p300.drop_tip()

    # Transfer DNA to quant wells.
    for s_well, d_well in zip(quant_DNA_sample_wells, qubit_quant_wells):
        p20.transfer(qubit_assay_dna_vol, s_well, d_well)

    ctx.comment("\n\nVortex plate for 2-3 seconds and incubate at RT " +
                "for 2 minutes before continuing")
    ctx.comment("\n\n~~~ End of protocol part 4 ~~~")
