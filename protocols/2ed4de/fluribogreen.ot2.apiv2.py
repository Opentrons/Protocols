metadata = {
    'protocolName': 'FluRibogreen Assay',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.11'
}


def run(ctx):

    [reagent_labware, starting_conc, p1000_mount,
     p300_mount] = get_values(  # noqa: F821
        'reagent_labware', 'starting_conc', 'p1000_mount', 'p300_mount')

    final_transfer_vol = 100
    sample_vol = 25
    max_working_vol = 1000
    max_factor_1_dil = max_working_vol/sample_vol

    # load labwarex
    sample_rack = ctx.load_labware(
        'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', '7',
        'sample tuberack')
    deepplate = ctx.load_labware('nest_96_wellplate_2ml_deep', '5',
                                 'standard preparation plate')
    flatplate = ctx.load_labware('corning_96_wellplate_360ul_flat', '8',
                                 'final plate')
    reagent_labware = ctx.load_labware(reagent_labware, '6',
                                       'standards and buffers')
    tipracks1000 = ctx.load_labware('opentrons_96_filtertiprack_1000ul', '9')
    tipracks200 = ctx.load_labware('opentrons_96_filtertiprack_200ul', '4')

    # load pipettes
    p1000 = ctx.load_instrument('p1000_single_gen2', p1000_mount,
                                tip_racks=[tipracks1000])
    p300 = ctx.load_instrument('p300_multi_gen2', p300_mount,
                               tip_racks=[tipracks200])

    tip_data = {
        'single': {
            'count': 0,
            'tips': [
                well for col in tipracks200.columns()[::-1]
                for well in col[::-1]]
        },
        'multi': {
            'count': 0,
            'tips': tipracks200.rows()[0]
        }
    }

    def pickup_p300(mode='single'):
        current = 0.1 if mode == 'single' else 0.5
        ctx._implementation._hw_manager.hardware._attached_instruments[
            p300._implementation.get_mount()].update_config_item(
                'pick_up_current', current)

        p300.pick_up_tip(tip_data[mode]['tips'][tip_data[mode]['count']])
        tip_data[mode]['count'] += 1

    working_standard_1 = reagent_labware.wells()[0]
    assay_buffer_1 = reagent_labware.wells()[1]
    working_standard_2 = reagent_labware.wells()[2]
    assay_buffer_2 = reagent_labware.wells()[3]
    starting_samples = sample_rack.wells()[:8]
    samples_1 = deepplate.columns()[3:6]
    samples_2 = deepplate.columns()[9:]

    def standard_prep(standard, buffer, column):
        dilution_col = column[:7]
        pickup_p300('single')
        p300.aspirate(50, standard)
        p300.dispense(50, dilution_col[5])
        p300.drop_tip()
        p1000.pick_up_tip()
        for vol, dest in zip([900, 700, 500, 300, 100], dilution_col[:5]):
            p1000.transfer(vol, standard, dest, new_tip='never')

        for vol, dest in zip([100, 300, 500, 700, 900, 950, 1000],
                             dilution_col):
            p1000.transfer(vol, buffer, dest, mix_after=(5, 800),
                           new_tip='never')
        p1000.drop_tip()

    def dilute(final_conc, dil_set, buffer):
        dil_factor = starting_conc/final_conc
        # find necessary dilution factor(s)
        if dil_factor > max_factor_1_dil:
            factors = [10, dil_factor/10]
        else:
            factors = [dil_factor]

        # pre add diluent
        for i, factor in enumerate(factors):
            dil_vol = (factor-1)*sample_vol
            for well in dil_set[i]:
                p1000.transfer(dil_vol, buffer, well)

        # transfer sample
        for i, s in enumerate(starting_samples):
            pickup_p300('single')
            p300.aspirate(sample_vol, s)
            p300.dispense(sample_vol, dil_set[0][i])
            p300.drop_tip()

        # perform dilution
        for i, factor in enumerate(factors):
            pickup_p300('multi')
            total_vol = sample_vol*factor
            mix_vol = total_vol*0.8 if total_vol*0.8 <= 175 else 175
            p300.transfer(sample_vol, dil_set[i][0], dil_set[i+1][0],
                          mix_before=(5, mix_vol), mix_after=(5, mix_vol),
                          new_tip='never')
            p300.drop_tip()

        return dil_set[len(factors)][0]

    """ PART 1 """

    # TE preparation
    standard_prep(working_standard_1, assay_buffer_1, deepplate.columns()[0])

    # TR preparation
    standard_prep(working_standard_2, assay_buffer_2, deepplate.columns()[6])

    """ PART 2 """

    # sample normalization (TE)
    # default from 60µg/ml to 2.5µg/ml - 24:1 (1 fold)
    sample_1_final_loc = dilute(2.5, samples_1, assay_buffer_1)

    # sample normalization (TR)
    # default from 60µg/ml to 0.5µg/ml - 120:1 (2 fold)
    sample_2_final_loc = dilute(0.5, samples_2, assay_buffer_2)

    """ PART 3 """

    # transfer to final black plate
    for i, source in enumerate(
            [deepplate.rows_by_name()['A'][0], sample_1_final_loc,
             deepplate.rows_by_name()['A'][6], sample_2_final_loc]):
        pickup_p300('multi')
        dest_set = flatplate.rows()[0][i*3:(i+1)*3]
        for dest in dest_set:
            p300.transfer(final_transfer_vol, source, dest, new_tip='never')
        p300.drop_tip()
