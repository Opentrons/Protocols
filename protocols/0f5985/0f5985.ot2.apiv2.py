from opentrons import ctx_api, types
import math

metadata = {
    'ctxName': 'ctx Title',
    'author': 'AUTHOR NAME <authoremail@company.com>',
    'source': 'Custom ctx Request',
    'apiLevel': '2.11'   # CHECK IF YOUR API LEVEL HERE IS UP TO DATE
                         # IN SECTION 5.2 OF THE APIV2 "VERSIONING"
}


def get_values(*names):
    import json
    _all_values = json.loads("""{ "n_samples":46,
                                  "sample_vol":400,
                                  "is_blood":true,
                                  "lwaste":true,
                                  "x_offset":1,
                                 }
                                  """)
    return [_all_values[n] for n in names]


def run(ctx: ctx_api.ctxContext):

    [
     n_samples,
     sample_vol,
     is_blood,
     lwaste,
     x_offset
    ] = get_values(  # noqa: F821 (<--- DO NOT REMOVE!)
        "n_samples",
        "sample_vol",
        "is_blood",
        "lwaste",
        "x_offset"
        )

    pip_lname = 'm300_multi_gen2'
    tips_lname = 'opentrons_96_filtertiprack_200ul'
    one_well_resv_lname = 'nest_1_reservoir_195ml'
    twelve_well_resv_lname = 'nest_12_reservoir_15ml'
    mag_mod_lname = 'magnetic module gen2'
    mag_plate_lname = 'nest_96_wellplate_2ml_deep'

    n_sample_columns = math.floor(n_samples/8)

    lysis_buf_lbb_vol = 2*sample_vol+100
    prot_k_vol = 0.15*sample_vol
    bind_bbb_vol = 1.5*sample_vol
    wash_wbb_vol = 4*sample_vol
    wash_wbc_vol = 1600

    elution_buf_vol = 200 if is_blood else 40

    # Offsets to pipette away from the magnetic beads
    sides = [-x_offset, x_offset] * (n_sample_columns // 2)
    total_liq_waste_vol = 0

    # load modules

    '''

    Add your modules here with:

    module_name = ctx.load_module('{module_loadname}', '{slot number}')

    Note: if you are loading a thermocycler, you do not need to specify
    a slot number - thermocyclers will always occupy slots 7, 8, 10, and 11.

    For all other modules, you can load them on slots 1, 3, 4, 6, 7, 9, 10.

    '''
    mag_mod = ctx.load_module(mag_mod_lname, '3')

    # load labware

    '''

    Add your labware here with:

    labware_name = ctx.load_labware('{loadname}', '{slot number}')

    If loading labware on a module, you can load with:

    labware_name = module_name.load_labware('{loadname}')
    where module_name is defined above.

    '''
    lysis_lbb_resv = ctx.load_labware(one_well_resv_lname, '1',
                                      label="lysis bbb reservoir")
    wash_bbb_resv = ctx.load_labware(one_well_resv_lname, '2',
                                     label="wash bbb reservoir")
    sample_plate = mag_mod.load_labware(one_well_resv_lname,
                                        label="sample plate")
    twelve_well_resv = ctx.load_labware(twelve_well_resv_lname, '4',
                                        label="multi-reagent reservoir")
    trash_resv_1 = ctx.load_labware(one_well_resv_lname, '6',
                                    label="liquid waste reservoir 1")
    wash_wbc_resv = ctx.load_labware(one_well_resv_lname, '7',
                                     label="wash wbc reservoir 1")
    trash_resv_2 = ctx.load_labware(one_well_resv_lname, '9',
                                    label="liquid waste reservoir 2")

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
    tipracks = [ctx.load_labware(tips_lname, slot)
                for slot in ['5', '8', '11']]

    # load instrument

    '''
    Nomenclature for pipette:

    use 'p'  for single-channel, 'm' for multi-channel,
    followed by number of microliters.

    p20, m300, p1000 (single channel pipettes)
    m20, m300 (multi-channel pipettes)

    If loading pipette, load with:

    ctx.load_instrument(
                        '{pipette api load name}',
                        pipette_mount ("left", or "right"),
                        tip_racks=tiprack
                        )
    '''
    m300 = ctx.load_instrument(
                              pip_lname,
                              'left',
                              tip_racks=tipracks
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

    For any functions in your ctx, describe the function as well as
    describe the parameters which are to be passed in as a docstring below
    the function (see below).

    def pick_up(pipette):
        """`pick_up()` will pause the ctx when all tip boxes are out of
        tips, prompting the user to replace all tip racks. Once tipracks are
        reset, the ctx will start picking up tips from the first tip
        box as defined in the slot order when assigning the labware definition
        for that tip box. `pick_up()` will track tips for both pipettes if
        applicable.

        :param pipette: The pipette desired to pick up tip
        as definited earlier in the ctx (e.g. m300, m20).
        """
        try:
            pipette.pick_up_tip()
        except ctx_api.labware.OutOfTipsError:
            ctx.pause("Replace empty tip racks")
            pipette.reset_tipracks()
            pipette.pick_up_tip()

    '''
    def pick_up(pipette):
        """`pick_up()` will pause the ctx when all tip boxes are out of
        tips, prompting the user to replace all tip racks. Once tipracks are
        reset, the ctx will start picking up tips from the first tip
        box as defined in the slot order when assigning the labware definition
        for that tip box. `pick_up()` will track tips for both pipettes if
        applicable.

        :param pipette: The pipette desired to pick up tip
        as definited earlier in the ctx (e.g. m300, m20).
        """
        try:
            pipette.pick_up_tip()
        except ctx_api.labware.OutOfTipsError:
            ctx.pause("Replace empty tip racks")
            pipette.reset_tipracks()
            pipette.pick_up_tip()

    # helper functions
    '''
    Define any custom helper functions outside of the pipette scope here, using
    the convention seen above.
    '''

    def remove_supernatant(source_columns, volume):
        '''
        Remove supernatant from the source columns and dispense it in the trash
        (the user may remove the waste to liquid waste reservoir if they so
        choose)

        :param source_columns: The columns to remove supernatant from
        :param volume: The volume of supernatant to remove
        '''
        nonlocal lwaste, trash, liq_trash_wells, m300, sides, \
            total_liq_waste_vol

        remainining_volume = volume
        for col, side in zip(source_columns, sides):
            pick_up(m300)
            trash_vol = (200 if remainining_volume > 200 else
                         remainining_volume)
            m300.aspirate(trash_vol,
                          src.bottom().move(types.Point(x=side, y=0, z=0.5)))
            trash_target = trash
            if lwaste:
                trash_target = liq_trash_wells[0].top() \
                    if total_liq_waste_vol < 1.95*10**5 else \
                    liq_trash_wells[1].top()

            m300.dispense(trash_vol, trash_target)
            m300.blow_out(trash_target)
            m300.drop_tip()
            total_liq_waste_vol += volume

    def wash(sample_columns, wash_vol, wash_vol_tracker, mag_engage_time):
        nonlocal lwaste, trash, liq_trash_wells, m300, sides, \
            total_liq_waste_vol

        for i in range(0, 2):
            remainining_volume = wash_vol
            for col in sample_columns:
                pick_up(m300)
                while remainining_volume > 0:
                    vol = 200 if remainining_volume >= 200 else \
                        remainining_volume
                    m300.aspirate(vol, wash_vol_tracker.tracker(vol))
                    m300.dispense(vol, col[0])
                mix_vol = 200 if wash_vol - 20 > 200 else wash_vol - 20
                m300.mix(20, mix_vol)
                m300.drop_tip()

            mag_mod.engage()
            ctx.delay(minutes=mag_engage_time)
            remove_supernatant(sample_columns, wash_vol)

    def transfer_samples_to_target():
        pass

    # Volume Tracking
    class VolTracker:
        def __init__(self, labware, well_vol,
                     column=0, start=0, end=8,
                     mode='reagent', pip_type='single',
                     msg='Reset labware volumes'):
            """
            Voltracker tracks the volume(s) used in a piece of labware

            :param labware: The labware to track
            :param well_vol: The volume of the liquid in the wells
            :param pip_type: The pipette type used 'single' or 'multi'
            :param mode: 'reagent' or 'waste'
            :param start: The starting well
            :param end: The ending well
            :param msg: Message to send to the user when all wells are empty

            """
            self.labware_wells = dict.fromkeys(
                labware.columns()[column][start:end], 0)
            self.labware_wells_backup = self.labware_wells.copy()
            self.well_vol = well_vol
            self.pip_type = pip_type
            self.mode = mode
            self.start = start
            self.end = end
            self.msg = msg

        def tracker(self, vol):
            '''tracker() will track how much liquid
            was used up per well. If the volume of
            a given well is greater than self.well_vol
            it will remove it from the dictionary and iterate
            to the next well which will act as the reservoir.'''
            well = next(iter(self.labware_wells))
            if self.labware_wells[well] + vol >= self.well_vol:
                del self.labware_wells[well]
                if len(self.labware_wells) < 1:
                    ctx.pause(self.msg)
                    self.labware_wells = self.labware_wells_backup.copy()
                well = next(iter(self.labware_wells))
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
            return well
    # reagents

    '''
    Define where all reagents are on the deck using the labware defined above.

    e.g.

    water = reservoir12.wells()[-1]
    waste = reservoir.wells()[0]
    samples = plate.rows()[0][0]
    dnase = tuberack.wells_by_name()['A4']

    '''
    lysis_lbb_well = lysis_bbb_resv.wells_by_name()['A1']
    wash_bbb_well = wash_bbb_resv.wells_by_name()['A1']
    wash_wbc_well = wash_wbc_resv.wells_by_name()['A1']
    prot_k_well = twelve_well_resv.wells_by_name()['A1']
    bind_bbb_wells = [twelve_well_resv.wells_by_name()['A2'],
                      twelve_well_resv.wells_by_name()['A3']]
    elutn_bfr_wells = [twelve_well_resv.wells_by_name()['A4'],
                       twelve_well_resv.wells_by_name()['A5']]
    liq_trash_wells = [trash_resv_1.wells_by_name()['A1'],
                       trash_resv_2.wells_by_name()['A2']]
    trash = m300.trash_container.wells()[0].top()  # trash container

    lysis_lbb_total_vol = lysis_buf_lbb_vol*n_samples
    lysis_resv_volume = 195 if lysis_lbb_total_vol > 195 \
        else lysis_lbb_total_vol
    lysis_lbb_tracker = VolTracker(lysis_bbb_resv, lysis_resv_volume,
                                   'multi', start=1, end=1,
                                   msg="Replenish lysis lbb buffer")

    wash_bbb_total_vol = wash_wbb_vol*n_samples
    lysis_resv_volume = 195 if lysis_lbb_total_vol > 195 \
        else lysis_lbb_total_vol
    lysis_lbb_tracker = VolTracker(lysis_bbb_resv, lysis_resv_volume,
                                   'multi', start=1, end=1,
                                   msg="Replenish lysis lbb buffer")

    # plate, tube rack maps

    '''
    Define any plate or tube maps here.

    e.g.

    plate_wells_by_row = [well for row in plate.rows() for well in row]

    '''
    sample_cols = sample_plate.columns()[0:n_samples]

    # ctx

    '''

    Include header sections as follows for each "section" of your ctx.

    Section can be defined as a step in a bench ctx.

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

    # step 1 - Add 2 samples volumes + 100 uL of lysis buffer BBB
    for col in sample_cols:
        m300.transfer(lysis_buf_lbb_vol, lysis_lbb_well, col[0])

    m300.drop_tip()

    # step 2 - Add proteinase K to samples and mix 10 times
    total_well_vol = sample_vol + lysis_buf_lbb_vol + prot_k_vol
    mix_vol = 200 if total_well_vol - 20 > 200 else total_well_vol - 20
    for col in sample_cols:
        pick_up(m300)
        m300.transfer(prot_k_vol, prot_k_well, col[0], new_tip='never')
        # Mix slowly to prevent bubble formation
        m300.mix(20, mix_vol, col[0], m300.flow_rate.aspirate/2)
        m300.drop_tip()

    # Step 3 - Incubate the samples with the buffer and enzyme
    ctx.comment('Incubation step: Seal the sample plate and incubate samples \
                for 10 minutes at 37 C or 30 minutes at room temperature \
                (see bench protocol step 3)')
    ctx.pause('Resume when the sample plate has been reinserted \
               on the mag deck and the Bind BBB buffer has been vortexed \
               or inverted 20 times')

    # Step 4 - Adding bind BBB buffer
    total_well_vol += bind_bbb_vol
    mix_vol = 200 if total_well_vol - 20 > 200 else total_well_vol - 20
    bbb_vol_used = 0
    for col in sample_cols:
        pick_up(m300)
        # 14 mL per NEST 12-well reservoir well (1 mL is wasted)
        bind_bbb_well = bind_bbb_wells[0] if bbb_vol_used < 1.4*10**4 \
            else bind_bbb_wells[1]
        m300.transfer(bind_bbb_vol, bind_bbb_well, col[0], new_tip='never')
        bbb_vol_used += bind_bbb_vol
        m300.mix(20, mix_vol, col[0])
        m300.drop_tip()

    # Step 5 - Incubate samples for 5 minutes
    ctx.comment('Beginning 5 minutes incubation at room temperature')
    ctx.delay(minutes=5)

    # Step 6 - Engage magnets for 15 minutes
    mag_mod.engage()
    ctx.delay(minutes=15)

    # step 7 - Aspirate off the supernatant and dump it in the waste
    remove_supernatant(sample_cols, total_well_vol)
    total_well_vol = 0

    # Step 8 through 11: Wash the beads two times
    for i in range(0, 2):
        mag_mod.disengage()
        wash()
        mag_mod.engage()
        ctx.delay(miutes=10)
        remove_supernatant()

    # Steps 12-15 - Disengage magnets and wash with buffer "Wash WBC" 2 times
    for i in range(0, 2):
        mag_mod.disengage()
        wash()
        mag_mod.engage()
        ctx.delay(miutes=8)
        remove_supernatant()

    # Step 16 - Add elution buffer and mix
    for col in sample_cols:
        m300.transfer(elution_buf_vol, elutn_bfr_wells, col[0])

    # Step 17 - Incubate samples for two minutes and mix with tips
    ctx.delay(minutes=2)

    # Step 18 - Engage magnets (5 min) and transfer to destination plate
    mag_mod.engage()
    ctx.delay(minutes=5)
    transfer_samples_to_target()
    ctx.comment("\n\n ~~~~ End of protocol ~~~~")
