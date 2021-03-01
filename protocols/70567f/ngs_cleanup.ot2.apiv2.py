import math
import os
import json
from opentrons.types import Point

metadata = {
    'protocolName': 'NGS Library Cleanup with Ampure XP Beads',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.9'
}

MAG_HEIGHT = 6.8


def run(ctx):

    [p300_multi_mount, number_of_samples, volume_of_beads,
     bead_incubation_time_in_minutes, bead_settling_time_on_magnet_in_minutes,
     drying_time_in_minutes, vol_etoh, mix_etoh, volume_EB_in_ul,
     volume_final_elution_in_ul, park_tips,
     tip_track, drop_threshold] = get_values(  # noqa: F821
        'p300_multi_mount', 'number_of_samples', 'volume_of_beads',
        'bead_incubation_time_in_minutes',
        'bead_settling_time_on_magnet_in_minutes',
        'drying_time_in_minutes', 'vol_etoh', 'mix_etoh', 'volume_EB_in_ul',
        'volume_final_elution_in_ul', 'park_tips', 'tip_track',
        'drop_threshold')

    # check
    if number_of_samples > 96 or number_of_samples < 1:
        raise Exception('Invalid number of samples.')

    num_cols = math.ceil(number_of_samples/8)

    # load labware
    magdeck = ctx.load_module('magnetic module gen2', '1')
    mag_plate = magdeck.load_labware(
        'nest_96_wellplate_100ul_pcr_full_skirt', 'magnetic plate')
    elution_plate = ctx.load_labware(
        'nest_96_wellplate_100ul_pcr_full_skirt', '2', 'elution plate')
    tips300 = [
        ctx.load_labware('opentrons_96_filtertiprack_200ul', slot)
        for slot in ['5', '6', '8', '9', '10', '11', '3']]
    if park_tips:
        rack = ctx.load_labware(
            'opentrons_96_tiprack_300ul', '4', 'tiprack for parking')
        parking_spots = rack.rows()[0][:num_cols]
    else:
        rack = ctx.load_labware(
            'opentrons_96_tiprack_300ul', '4', '200µl filtertiprack')
        parking_spots = [None for none in range(12)]
    tips300.insert(0, rack)

    res12 = ctx.load_labware('nest_12_reservoir_15ml', '7',
                             'reagent reservoir')

    # sample setup
    mag_samples = mag_plate.rows()[0][:num_cols]
    elution_samples = elution_plate.rows()[0][:num_cols]

    # reagents
    beads = res12.wells()[0]
    etoh = res12.wells()[1]
    eb_buff = res12.wells()[2]
    waste = [chan.top(-2) for chan in res12.wells()[10:]]

    # pipettes
    m300 = ctx.load_instrument(
        'p300_multi_gen2', mount=p300_multi_mount, tip_racks=tips300)
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 200

    tip_log = {val: {} for val in ctx.loaded_instruments.values()}
    folder_path = '/data/bead_cleanup'
    tip_file_path = folder_path + '/tip_log.json'
    if tip_track and not ctx.is_simulating():
        if os.path.isfile(tip_file_path):
            with open(tip_file_path) as json_file:
                data = json.load(json_file)
                for pip in tip_log:
                    if pip.name in data:
                        tip_log[pip]['count'] = data[pip.name]
                    else:
                        tip_log[pip]['count'] = 0
        else:
            for pip in tip_log:
                tip_log[pip]['count'] = 0
    else:
        for pip in tip_log:
            tip_log[pip]['count'] = 0

    for pip in tip_log:
        if pip.type == 'multi':
            tip_log[pip]['tips'] = [tip for rack in pip.tip_racks
                                    for tip in rack.rows()[0]]
        else:
            tip_log[pip]['tips'] = [tip for rack in pip.tip_racks
                                    for tip in rack.wells()]
        tip_log[pip]['max'] = len(tip_log[pip]['tips'])

    def pick_up(pip, loc=None):
        if tip_log[pip]['count'] == tip_log[pip]['max'] and not loc:
            ctx.pause('Replace ' + str(pip.max_volume) + 'µl tipracks before \
resuming.')
            pip.reset_tipracks()
            tip_log[pip]['count'] = 0
        if loc:
            pip.pick_up_tip(loc)
            return loc
        else:
            loc = tip_log[pip]['tips'][tip_log[pip]['count']]
            pip.pick_up_tip(loc)
            tip_log[pip]['count'] += 1
            return loc

    switch = True
    drop_count = 0
    # number of tips trash will accommodate before prompting user to empty

    def drop(pip, loc=None):
        nonlocal switch
        nonlocal drop_count
        if not loc:
            if pip.type == 'multi':
                drop_count += 8
            else:
                drop_count += 1
            if drop_count >= drop_threshold:
                ctx.home()
                ctx.pause('Please empty tips from waste before resuming.')
                drop_count = 0
            side = 30 if switch else -18
            drop_loc = ctx.loaded_labwares[12].wells()[0].top().move(
                Point(x=side))
            pip.drop_tip(drop_loc)
            switch = not switch

    # mix beads
    ctx.max_speeds['A'] = 50
    ctx.max_speeds['Z'] = 50
    # transfer beads and mix samples
    for m, p in zip(mag_samples, parking_spots):
        pick_up(m300)
        m300.mix(5, volume_of_beads, beads)
        m300.blow_out(beads.top(-5))
        m300.transfer(volume_of_beads, beads, m.bottom(2), new_tip='never')
        m300.blow_out()
        m300.mix(10, volume_of_beads, m.bottom(2))
        m300.blow_out(m.top(-5))
        drop(m300, p)
    ctx.max_speeds['A'] = 125
    ctx.max_speeds['Z'] = 125

    # incubation
    ctx.delay(minutes=bead_incubation_time_in_minutes, msg='Incubating off \
magnet for ' + str(bead_incubation_time_in_minutes) + ' minutes.')
    magdeck.engage(height=MAG_HEIGHT)
    ctx.delay(minutes=bead_settling_time_on_magnet_in_minutes, msg='Incubating \
on magnet for ' + str(bead_settling_time_on_magnet_in_minutes) + ' minutes.')

    # remove supernatant
    for m, p in zip(mag_samples, parking_spots):
        pick_up(m300, p)
        m300.transfer(
            120, m.bottom(0.5), waste[1], new_tip='never')
        m300.blow_out(waste[1])
        drop(m300, p)

    # 2x EtOH washes
    etoh_loc = None
    for wash in range(2):

        magdeck.disengage()

        # transfer EtOH
        if wash == 0:
            etoh_loc = pick_up(m300)
        else:
            pick_up(m300, etoh_loc)

        m300.distribute(vol_etoh, etoh, [m.top(2) for m in mag_samples],
                        air_gap=20, new_tip='never')
        if wash == 0:
            drop(m300, etoh_loc)
        else:
            drop(m300)
        if mix_etoh:
            for m, p in zip(mag_samples, parking_spots):
                pick_up(m300, p)
                m300.mix(10, vol_etoh*0.8, m)
                m300.blow_out(m.top())
                drop(m300, p)

        magdeck.engage(height=MAG_HEIGHT)
        ctx.delay(minutes=bead_settling_time_on_magnet_in_minutes,
                  msg='Incubating on magnet for \
' + str(bead_settling_time_on_magnet_in_minutes) + ' minutes.')

        # remove supernatant
        if wash == 0:
            for m, p in zip(mag_samples, parking_spots):
                if mix_etoh:
                    pick_up(m300, p)
                else:
                    if not m300.has_tip:
                        pick_up(m300, p)
                m300.transfer(vol_etoh, m.bottom(0.5), waste[0],
                              new_tip='never')
                m300.blow_out(waste[0])
                drop(m300, p)
        else:
            for m, p in zip(mag_samples, parking_spots):
                if mix_etoh:
                    pick_up(m300, p)
                else:
                    if not m300.has_tip:
                        pick_up(m300, p)
                m300.transfer(vol_etoh - 15, m.bottom(0.5), waste[0],
                              new_tip='never')
                drop(m300, p)

            ctx.pause('Briefly centrifuge plate to pellet any residual \
material on the side of the wells. Then, replace plate on magnetic module.')

            for m, p in zip(mag_samples, parking_spots):
                pick_up(m300, p)
                m300.transfer(20, m.bottom(0.5), waste[0], new_tip='never')
                m300.blow_out(waste[0])
                drop(m300)

    ctx.delay(
        minutes=drying_time_in_minutes, msg='Drying for \
' + str(drying_time_in_minutes) + ' minutes.')
    magdeck.disengage()

    # transfer EB buffer
    for m, p in zip(mag_samples, parking_spots):
        pick_up(m300)
        m300.transfer(volume_EB_in_ul, eb_buff, m,
                      mix_after=(10, 0.8*volume_EB_in_ul), new_tip='never')
        m300.blow_out(m.top())
        drop(m300)

    ctx.delay(minutes=bead_incubation_time_in_minutes, msg='Incubating off \
magnet for ' + str(bead_incubation_time_in_minutes) + ' minutes.')
    magdeck.engage(height=MAG_HEIGHT)
    ctx.delay(minutes=bead_settling_time_on_magnet_in_minutes, msg='Incubating \
on magnet for ' + str(bead_settling_time_on_magnet_in_minutes) + ' minutes.')

    # transfer supernatant to new PCR plate
    for m, e, p in zip(mag_samples, elution_samples, parking_spots):
        pick_up(m300)
        m300.transfer(volume_final_elution_in_ul, m, e, new_tip='never')
        m300.blow_out(e.top(-2))
        drop(m300)

    magdeck.disengage()

    # track final used tip
    if tip_track and not ctx.is_simulating():
        if not os.path.isdir(folder_path):
            os.mkdir(folder_path)
        data = {pip.name: tip_log[pip]['count'] for pip in tip_log}
        with open(tip_file_path, 'w') as outfile:
            json.dump(data, outfile)
