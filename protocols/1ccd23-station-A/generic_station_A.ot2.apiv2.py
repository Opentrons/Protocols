from opentrons import protocol_api
import json
import os
# import math

# metadata
metadata = {
    'protocolName': 'Sample plating protocol',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.0'
}


def run(ctx: protocol_api.ProtocolContext):

    num_samples, vol_sample, tip_track = get_values(  # noqa: F821
        'num_samples', 'vol_sample', 'tip_track')

    # load labware
    tempdeck = ctx.load_module('temperature module gen2', '1')
    ic_pk = tempdeck.load_labware(
        'opentrons_24_aluminumblock_nest_2ml_screwcap',
        'chilled tubeblock for internal control (well A1)')
    source_racks = [
        ctx.load_labware(
            'opentrons_24_tuberack_eppendorf_2ml_safelock_snapcap', slot,
            'source tuberack ' + str(i+1))
        for i, slot in enumerate(['2', '3', '5', '6'])
    ]
    dest_plate = ctx.load_labware(
        'nest_96_wellplate_2ml_deep', '4', '96-deepwell sample plate')
    tipracks20 = [
        ctx.load_labware('opentrons_96_filtertiprack_20ul', slot,
                         '20µl filter tiprack')
        for slot in ['7', '8', '9']]
    tipracks1000 = [ctx.load_labware('opentrons_96_filtertiprack_1000ul', slot,
                                     '1000µl filter tiprack')
                    for slot in ['10', '11']]

    # load pipette
    p20 = ctx.load_instrument('p20_single_gen2', 'left', tip_racks=tipracks20)
    p1000 = ctx.load_instrument(
        'p1000_single_gen2', 'right', tip_racks=tipracks1000)

    # setup samples
    sources = [
        well for rack in source_racks for well in rack.wells()][:num_samples]
    dests_single = dest_plate.wells()[:num_samples]
    # num_cols = math.ceil(num_samples/8)
    ic = ic_pk.wells()[0]
    pk = ic_pk.wells()[1]

    tip_log = {'count': {}}
    folder_path = '/data/A'
    tip_file_path = folder_path + '/tip_log.json'
    if tip_track and not ctx.is_simulating():
        if os.path.isfile(tip_file_path):
            with open(tip_file_path) as json_file:
                data = json.load(json_file)
                if 'tips1000' in data:
                    tip_log['count'][p1000] = data['tips1000']
                else:
                    tip_log['count'][p1000] = 0
                if 'tips20' in data:
                    tip_log['count'][p20] = data['tips20']
                else:
                    tip_log['count'][p20] = 0
    else:
        tip_log['count'] = {p1000: 0, p20: 0}

    tip_log['tips'] = {
        p1000: [tip for rack in tipracks1000 for tip in rack.wells()],
        p20: [tip for rack in tipracks20 for tip in rack.wells()]
    }
    tip_log['max'] = {
        pip: len(tip_log['tips'][pip])
        for pip in [p1000, p20]
    }

    def pick_up(pip):
        nonlocal tip_log
        if tip_log['count'][pip] == tip_log['max'][pip]:
            ctx.pause('Replace ' + str(pip.max_volume) + 'µl tipracks before \
resuming.')
            pip.reset_tipracks()
            tip_log['count'][pip] = 0
        pip.pick_up_tip(tip_log['tips'][pip][tip_log['count'][pip]])
        tip_log['count'][pip] += 1

    # transfer sample
    for s, d in zip(sources, dests_single):
        pick_up(p1000)
        p1000.transfer(vol_sample, s.bottom(5), d.bottom(5), air_gap=100,
                       new_tip='never')
        p1000.air_gap(100)
        p1000.drop_tip()

    # transfer internal control + proteinase K
    for reagent in [ic, pk]:
        for d in dests_single:
            pick_up(p20)
            p20.transfer(10, reagent.bottom(2), d.bottom(10), air_gap=5,
                         new_tip='never')
            p20.air_gap(5)
            p20.drop_tip()

    ctx.comment('Move deepwell plate (slot 4) to Station B for RNA \
extraction.')

    # track final used tip
    if not ctx.is_simulating():
        if not os.path.isdir(folder_path):
            os.mkdir(folder_path)
        data = {
            'tips1000': tip_log['count'][p1000],
            'tips20': tip_log['count'][p20]
        }
        with open(tip_file_path, 'w') as outfile:
            json.dump(data, outfile)
