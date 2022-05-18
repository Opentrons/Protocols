from opentrons.types import Point
import json
import os
import math

metadata = {
    'protocolName': 'NEBNext® Ultra™ II DNA Library Prep Kit for Illumina®',
    'author': 'Opentrons <protocols@opentrons.com>',
    'apiLevel': '2.12'
}


# Start protocol
def run(ctx):

    [num_samples, _ratio_beads_dna, time_mag_incubation,
     mount_m300, mount_m20, _dry_run] = get_values(  # noqa: F821
        'num_samples', '_ratio_beads_dna', 'time_mag_incubation', 'mount_m300',
        'mount_m20', '_dry_run')
    park_tips = True
    tip_track = False
    mag_height = 11
    x_offset = 2.0
    z_offset_beads = 2.0
    z_offset_supernatant = 1.0

    magdeck = ctx.load_module('magnetic module gen2', '1')
    magdeck.disengage()
    mag_plate = magdeck.load_labware('eppendorftwin.tec_96_wellplate_150ul')
    tips20 = [
        ctx.load_labware('opentrons_96_filtertiprack_20ul', slot)
        for slot in ['2', '4', '5']]
    tempdeck = ctx.load_module('Temperature Module Gen2', '3')
    tempdeck.set_temperature(12)
    elution_plate = tempdeck.load_labware(
        'eppendorftwin.tec_96_aluminumblock_150ul')
    tc = ctx.load_module('thermocycler')
    tc.open_lid()
    tc.set_block_temperature(20)
    tc.set_lid_temperature(105)
    tc_plate = tc.load_labware('eppendorftwin.tec_96_wellplate_150ul',
                               'DNA plate')
    tips300 = [ctx.load_labware('opentrons_96_filtertiprack_200ul', slot)
               for slot in ['6']]
    reservoir = ctx.load_labware('nest_96_wellplate_2ml_deep', '9',
                                 'reagent reservoir')

    num_cols = math.ceil(num_samples/8)
    if park_tips:
        parking_spots300 = tips300[0].rows()[0][:num_cols]
        parking_spots20 = tips20[0].rows()[0][:num_cols]
    else:
        parking_spots300 = [None for none in range(12)]
        parking_spots20 = [None for none in range(12)]

    # load pipette
    m300 = ctx.load_instrument(
        'p300_multi_gen2', mount_m300, tip_racks=tips300)
    m20 = ctx.load_instrument(
        'p20_multi_gen2', mount_m20, tip_racks=tips20)

    tip_log = {val: {} for val in ctx.loaded_instruments.values()}

    """
    Here is where you can define the locations of your reagents.
    """
    mastermix = reservoir.rows()[0][0]
    adaptor = reservoir.rows()[0][1]
    mastermix2 = reservoir.rows()[0][2]
    user = reservoir.rows()[0][3]
    etoh = reservoir.rows()[0][4]
    elution_buffer = reservoir.rows()[0][5]
    waste = reservoir.rows()[0][-1]

    mag_samples_m = mag_plate.rows()[0][:num_cols]
    elution_samples_m = elution_plate.rows()[0][:num_cols]
    tc_samples_m = tc_plate.rows()[0][:num_cols]

    magdeck.disengage()  # just in case

    m300.flow_rate.aspirate = 50
    m300.flow_rate.dispense = 150
    m300.flow_rate.blow_out = 300

    folder_path = '/data/B'
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

    def _pick_up(pip, loc=None):
        if tip_log[pip]['count'] == tip_log[pip]['max'] and not loc:
            ctx.pause('Replace ' + str(pip.max_volume) + 'µl tipracks before \
resuming.')
            pip.reset_tipracks()
            tip_log[pip]['count'] = 0
        if loc:
            pip.pick_up_tip(loc)
        else:
            pip.pick_up_tip(tip_log[pip]['tips'][tip_log[pip]['count']])
            tip_log[pip]['count'] += 1

    switch = True
    drop_count = 0
    # number of tips trash will accommodate before prompting user to empty
    drop_threshold = 120

    def _drop(pip, loc=None):
        nonlocal switch
        nonlocal drop_count
        if loc:
            pip.drop_tip(loc)
        else:
            side = 30 if switch else -18
            drop_loc = ctx.loaded_labwares[12].wells()[0].top().move(
                Point(x=side))
            pip.drop_tip(drop_loc)
            switch = not switch
            if pip.type == 'multi':
                drop_count += 8
            else:
                drop_count += 1
            if drop_count == drop_threshold:
                ctx.pause('Please empty tips from waste before \
    resuming.')
                drop_count = 0

    def remove_supernatant(vol, pip=m300, park=False):
        pip.flow_rate.aspirate /= 5
        parking_spots = parking_spots300 if pip == m300 else parking_spots20
        for i, (m, p) in enumerate(zip(mag_samples_m, parking_spots)):
            if park:
                _pick_up(pip, p)
            else:
                _pick_up(pip)
            side = -1 if i % 2 == 0 else 1
            loc = m.bottom(0).move(Point(x=side, z=z_offset_supernatant))
            pip.move_to(m.center())
            pip.transfer(vol, loc, waste, new_tip='never',
                         air_gap=pip.min_volume)
            pip.blow_out(waste)
            pip.air_gap(pip.min_volume)
            _drop(pip)
        pip.flow_rate.aspirate *= 5

    """ 1. NEBNext End Prep """
    for t in tc_samples_m:
        _pick_up(m20)
        m20.transfer(10, mastermix, t, mix_after=(10, 20), new_tip='never')
        _drop(m20)

    profile = [
      {'temperature': 20, 'hold_time_minutes': 30},
      {'temperature': 65, 'hold_time_minutes': 30}]
    tc.close_lid()
    tc.execute_profile(steps=profile, repetitions=1, block_max_volume=60)
    tc.set_block_temperature(12)
    tc.open_lid()

    """ 2. Adapter Ligation """
    for t in tc_samples_m:
        _pick_up(m20)
        m20.transfer(2.5, adaptor, t, mix_after=(10, 20), new_tip='never')
        _drop(m20)

    for t in tc_samples_m:
        _pick_up(m300)
        m300.transfer(31, mastermix2, t, mix_after=(10, 50), new_tip='never')
        _drop(m300)

    tc.close_lid()
    tc.set_block_temperature(20, hold_time_minutes=15)
    tc.open_lid()

    for t in tc_samples_m:
        _pick_up(m20)
        m20.transfer(3, user, t, mix_after=(10, 20), new_tip='never')
        _drop(m20)

    tc.close_lid()
    tc.set_block_temperature(37, hold_time_minutes=15)
    tc.set_block_temperature(12)
    tc.open_lid()

    """ 3. Clean Up """
    dna_vol_total = 96.5
    elution_vol_total = 17
    num_washes = math.ceil(_ratio_beads_dna/0.9)
    dna_vol_wash = dna_vol_total/num_washes
    elution_vol_wash = elution_vol_total/num_washes
    elution_vol_final = 15/num_washes

    for wash_ind in range(num_washes):
        # add sample
        for t, m, p in zip(tc_samples_m, mag_samples_m, parking_spots300):
            if wash_ind == 0:
                _pick_up(m300)
            else:
                _pick_up(m300, p)
            m300.transfer(dna_vol_wash, t, m, mix_after=(10, 50),
                          new_tip='never')
            _drop(m300, p)
        if not _dry_run:
            ctx.delay(minutes=time_mag_incubation, msg=f'Incubating off magnet \
for {time_mag_incubation} minutes.')
        magdeck.engage(height=mag_height)
        if not _dry_run:
            ctx.delay(minutes=time_mag_incubation, msg=f'Incubating on magnet \
for {time_mag_incubation} minutes.')
        remove_supernatant(200, pip=m300, park=True)

        # wash 2x
        for _ in range(2):
            _pick_up(m300)
            for i, m in enumerate(mag_samples_m):
                m300.aspirate(200, etoh)
                m300.dispense(200, m.top())
            if not _dry_run:
                ctx.delay(seconds=30, msg='Incubating on magnet for 30 \
seconds.')
            m300.drop_tip()
            remove_supernatant(200, pip=m300, park=True)

        # remove residual
        remove_supernatant(20, pip=m20, park=False)

        # air dry
        if not _dry_run:
            ctx.delay(minutes=5, msg='Air drying for 5 minutes.')
        magdeck.disengage()

        # elute
        for i, m in enumerate(mag_samples_m):
            _pick_up(m20)
            side = 1 if i % 2 == 0 else -1
            loc = m.bottom().move(Point(x=x_offset*side, z=z_offset_beads))
            m20.aspirate(elution_vol_wash, elution_buffer)
            m20.move_to(m.center())
            m20.dispense(elution_vol_wash, loc)
            for _ in range(10):  # custom mix
                m20.aspirate(20, m.bottom(1))
                m20.dispense(20, loc)
            _drop(m20)

        if not _dry_run:
            ctx.delay(minutes=time_mag_incubation, msg=f'Incubating off magnet \
for {time_mag_incubation} minutes.')
        magdeck.engage(height=mag_height)
        if not _dry_run:
            ctx.delay(minutes=time_mag_incubation, msg=f'Incubating on magnet \
for {time_mag_incubation} minutes.')

        # elute
        for m, e in zip(mag_samples_m, elution_samples_m):
            _pick_up(m20)
            m20.flow_rate.aspirate /= 5
            m20.transfer(elution_vol_final, m.bottom(0.5), e, new_tip='never')
            m20.flow_rate.aspirate *= 5
            m20.mix(10, 20, e)
            _drop(m20)

    magdeck.disengage()
    tc.deactivate_lid()
    tc.deactivate_block()

    # track final used tip
    if not ctx.is_simulating():
        if not os.path.isdir(folder_path):
            os.mkdir(folder_path)
        data = {pip.name: tip_log[pip]['count'] for pip in tip_log}
        with open(tip_file_path, 'w') as outfile:
            json.dump(data, outfile)
