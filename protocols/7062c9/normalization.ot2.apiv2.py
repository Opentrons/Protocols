metadata = {
    'protocolName': 'Capping Assay: Steps 1-2',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Protocol Library',
    'apiLevel': '2.11'
    }


def run(ctx):
    [input_csv, p300_mount, p20_mount] = get_values(  # noqa: F821
        'input_csv', 'p300_mount', 'p20_mount')

    # labware
    sample_plate = ctx.load_labware('nest_96_wellplate_100ul_pcr_full_skirt',
                                    '1', 'sample plate')
    final_plate = ctx.load_labware('nest_96_wellplate_100ul_pcr_full_skirt',
                                   '2', 'normalized plate')
    reservoir = ctx.load_labware('nest_12_reservoir_15ml', '4',
                                 'reagent reservoir')
    tuberack = ctx.load_labware('opentrons_24_tuberack_nest_1.5ml_screwcap',
                                '5', 'buffer + probe tuberack')
    tipracks20 = [ctx.load_labware('opentrons_96_filtertiprack_20ul', '3')]
    tipracks200 = ctx.load_labware('opentrons_96_filtertiprack_200ul', '9')

    # pipettes
    p300 = ctx.load_instrument('p300_multi_gen2', p300_mount,
                               tip_racks=[tipracks200])
    p20 = ctx.load_instrument('p20_single_gen2', p20_mount,
                              tip_racks=tipracks20)

    ctx._implementation._hw_manager.hardware._attached_instruments[
        p300._implementation.get_mount()].update_config_item(
            'pick_up_current', 0.1)

    # reagents
    water = reservoir.wells()[0]
    buffer = tuberack.wells()[0]
    protease = tuberack.wells()[1]

    def drop_all_tips():
        for pipette in ctx.loaded_instruments.values():
            if pipette.has_tip:
                pipette.drop_tip()

    tip_data = {
        'single': {
            'count': 0,
            'tips': [
                well for col in tipracks200.columns()
                for well in col[::-1]]
        },
        'multi': {
            'count': 0,
            'tips': [tipracks200.rows()[0][::-1]]
        }
    }

    def pickup_p300(mode='single'):
        p300.pick_up_tip(tip_data[mode]['tips'][tip_data[mode]['count']])
        tip_data[mode]['count'] += 1

    # parse csv
    data = [
        [val for val in line.split(',')]
        for line in input_csv.splitlines()][1:]

    # prealocate water,
    for i, line in enumerate(data):
        water_vol = float(line[2])
        pip = p20 if water_vol <= 20 else p300
        dest_well = final_plate.wells()[i]
        if not pip.has_tip:
            if pip == p20:
                pip.pick_up_tip()
            else:
                pickup_p300('single')
        pip.aspirate(water_vol, water)
        pip.dispense(water_vol, dest_well)
    drop_all_tips()

    # prealocate buffer
    for i, line in enumerate(data):
        buffer_vol = float(line[3])
        pip = p20 if water_vol <= 20 else p300
        dest_well = final_plate.wells()[i]
        if not pip.has_tip:
            if pip == p20:
                pip.pick_up_tip()
            else:
                pickup_p300('single')
        pip.aspirate(buffer_vol, buffer)
        pip.dispense(buffer_vol, dest_well)
    drop_all_tips()

    last_probe = None
    for i, line in enumerate(data):
        probe_vol = float(line[4])
        probe = tuberack.wells_by_name()[line[5].upper().strip()]
        pip = p20 if water_vol <= 20 else p300
        dest_well = final_plate.wells()[i]
        if not probe == last_probe:
            if pip.has_tip:
                pip.drop_tip()
            if pip == p20:
                pip.pick_up_tip()
            else:
                pickup_p300('single')
        pip.aspirate(probe_vol, probe)
        pip.dispense(probe_vol, dest_well)
    drop_all_tips()

    # transfer sample and mix
    for i, line in enumerate(data):
        sample_vol = float(line[1])
        total_vol = float(line[6])
        pip = p20 if sample_vol <= 20 else p300
        sample_well, dest_well = [
            sample_plate.wells()[i], final_plate.wells()[i]]
        if 0.8*total_vol < pip.max_volume:
            mix_vol = 0.8*total_vol
        else:
            mix_vol = 0.8*pip.max_volume
        if pip == p20:
            pip.pick_up_tip()
        else:
            pickup_p300('single')
        pip.aspirate(sample_vol, sample_well)
        pip.dispense(sample_vol, dest_well)
        pip.mix(3, mix_vol, dest_well)
        drop_all_tips()

    ctx.pause('Put sample plate in the thermal cycler for 30min')

    # transfer protease
    for i, line in enumerate(data):
        dest_well = final_plate.wells()[i]
        p20.transfer(5, protease, dest_well)
