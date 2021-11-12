metadata = {
    'protocolName': 'FluRibogreen Assay',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.11'
}


def run(ctx):

    [p1000_mount, p300_mount] = get_values(  # noqa: F821
        'p1000_mount', 'p300_mount')

    final_transfer_vol = 150
    sample_vol = 200

    # load labwarex
    sample_rack = ctx.load_labware(
        'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', '1',
        'sample tuberack')
    deepplate = ctx.load_labware('nest_96_wellplate_2ml_deep', '2',
                                 'standard preparation plate')
    flatplate = ctx.load_labware('corning_96_wellplate_360ul_flat', '5',
                                 'final plate')
    reservoir = ctx.load_labware('nest_12_reservoir_15ml', '3')
    tipracks1000 = ctx.load_labware('opentrons_96_filtertiprack_1000ul', '6')
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

    working_standard_1 = reservoir.wells()[0]
    working_standard_2 = reservoir.wells()[1]
    assay_buffer_1 = reservoir.wells()[2]
    assay_buffer_2 = reservoir.wells()[3]
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

    """ PART 1 """

    # TE preparation
    standard_prep(working_standard_1, assay_buffer_1, deepplate.columns()[0])

    # TR preparation
    standard_prep(working_standard_2, assay_buffer_2, deepplate.columns()[6])

    """ PART 2 """

    # sample transfer
    for source, dest1, dest2 in zip(
            starting_samples, samples_1[0], samples_2[0]):
        p1000.distribute(sample_vol, source, [dest1, dest2])

    # sample normalization (TE) from 60µg/ml to 2.5µg/ml - 24:1 (1 fold)
    sample_volume = 1000/24
    p1000.transfer(1000-sample_volume, assay_buffer_1, samples_1[1])
    pickup_p300('multi')
    p300.transfer(sample_volume, samples_1[0][0], samples_1[1][0],
                  new_tip='never')
    p300.mix(5, 150, samples_1[1][0])
    p300.drop_tip()

    # sample normalization (TR) from 60µg/ml to 0.5µg/ml - 120:1 (2 fold)
    sample_1_vol = 1000/10
    sample_2_vol = 1000/12
    dil1_vol = 1000 - sample_1_vol
    dil2_vol = 1000 - sample_2_vol
    pickup_p300('multi')
    p300.transfer(dil1_vol, assay_buffer_2, samples_2[1][0],
                  new_tip='never')
    p300.transfer(dil2_vol, assay_buffer_2, samples_2[2][0],
                  new_tip='never')

    p300.transfer(sample_1_vol, samples_2[0][0], samples_2[1][0],
                  new_tip='never', mix_after=(5, 150))
    p300.transfer(sample_2_vol, samples_2[1][0], samples_2[2][0],
                  new_tip='never', mix_after=(5, 150))

    p300.drop_tip()

    """ PART 3 """

    # transfer to final black plate
    for i, source in enumerate(
            [deepplate.rows()[0][i] for i in [0, 5, 9, 10]]):
        pickup_p300('multi')
        dest_set = flatplate.rows()[0][i*3:(i+1)*3]
        for dest in dest_set:
            p300.transfer(final_transfer_vol, source, dest, new_tip='never')
        p300.drop_tip()
