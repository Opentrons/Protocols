import math
from opentrons.types import Point

metadata = {
    'title': 'NGS Library Prep - Protocol 1',
    'author': 'Nick Diehl <ndiehl@opentrons.com>',
    'apiLevel': '2.12'
}

SHAKE = False
VOLUME_SAMPLE_1 = 50
INCUBATION_TEMP = 4
INCUBATION_TIME_MINUTES = 10
NUM_SAMPLES_1 = 6
NUM_SAMPLES_2 = 2
WASH_VOLUMES_INCUBATION_2 = [200, 200]  # should list of length equivalent to length of sample columns


def run(ctx):

    if ctx.is_simulating():
        SHAKE = False
    if SHAKE:
        import sys
        sys.path.append("/var/lib/jupyter/notebooks/")
        import bioshake

    [NUM_SAMPLES_1, NUM_SAMPLES_2, pipette_p20, pipette_p300, mount_p20,
     mount_p300] = 3, 2, 'p20_single_gen2', 'p300_multi_gen2', 'right', 'left'

    num_samples = NUM_SAMPLES_1*NUM_SAMPLES_2
    time_mag_incubation = 2.0
    z_offset = 3.0
    x_offset_ratio = 0.7
    height_engage = 7.0

    # labware
    sample_plate = ctx.load_labware('agilent_96_wellplate_200ul', '6',
                                    'sample and elution plate')
    elution_plate = sample_plate
    prep_plate1 = ctx.load_labware('kingfisher_96_deepwell_plate_2ml', '4',
                                   'prep plate 1')
    prep_plate2 = ctx.load_labware('kingfisher_96_deepwell_plate_2ml', '5',
                                   'prep plate 2')
    tipracks20 = [ctx.load_labware('opentrons_96_filtertiprack_20ul', '7')]
    tipracks200 = [ctx.load_labware('opentrons_96_tiprack_300ul', '8')]
    tuberack = ctx.load_labware(
        'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', '2',
        '1.5ml tuberack')
    magdeck = ctx.load_module('magnetic module gen2', '9')
    mag_plate = magdeck.load_labware('kingfisher_96_deepwell_plate_2ml')
    reservoir = ctx.load_labware('agilent_3_reservoir_95ml', '11',
                                 'reservoir')

    if SHAKE:
        bioshake = bioshake.BioshakeDriver()
        bioshake.temp_on(4)
        shake_plate = ctx.load_labware(
            'thermoscientificnunc_96_wellplate_2000ul', '10',
            'Bioshake plate')
    else:
        shake_plate = ctx.load_labware(
            'thermoscientificnunc_96_wellplate_2000ul', '10',
            'Bioshake plate')

    # reagents
    beads_sample_1 = tuberack.wells()[0]
    buffer1, buffer2 = reservoir.wells()[:2]

    # pipettes
    p20 = ctx.load_instrument(pipette_p20, mount_p20, tip_racks=tipracks20)
    p300 = ctx.load_instrument(pipette_p300, mount_p300, tip_racks=tipracks200)

    vol_p300_max = p300.tip_racks[0].wells()[0].max_volume

    # reagents
    num_cols = math.ceil(num_samples/8)
    samples = sample_plate.rows()[0][:num_cols]
    buffer1, buffer2, buffer5 = reservoir.wells()[:3]
    waste = ctx.loaded_labwares[12].wells()[0].top()

    mm_tube = tuberack.wells()[0]
    water = tuberack.wells()[1]
    buffer3 = tuberack.wells()[2]
    buffer4 = tuberack.wells()[3]
    primer1 = tuberack.wells()[4]
    primer4 = tuberack.wells()[5]

    def pick_up(pip=p20, channels=p20.channels):
        def look():
            # iterate and look for required number of consecutive tips
            for rack in pip.tip_racks:
                for col in rack.columns():
                    counter = 0
                    for well in col[::-1]:
                        if well.has_tip:
                            counter += 1
                        else:
                            counter = 0
                        if counter == channels:
                            pip.pick_up_tip(well)
                            return True
            return False

        eval_pickup = look()
        if eval_pickup:
            return
        else:
            # refill rack if no tips available
            ctx.pause(f'Refill {pip} tipracks before resuming.')
            pip.reset_tipracks()
            look()

    index_ref_list = [well for row in mag_plate.rows() for well in row]

    def bead_mix(vol, reps, well, side):
        bead_loc = well.bottom().move(Point(
            x=side*well.diameter/2*x_offset_ratio, z=z_offset))

        vol = 200 if vol > 200 else vol

        for _ in range(reps):
            p300.aspirate(vol, well.bottom(1))
            p300.dispense(vol, bead_loc)

    def wash(wells, reagent, vol_initial, vols_wash, wash_reps, dests=None,
             remove_initial=True):

        # remove initial volume
        if remove_initial:
            magdeck.engage(height_engage)
            ctx.delay(minutes=time_mag_incubation, msg=f'Beads separating for \
{time_mag_incubation} minutes.')
            num_trans = math.ceil(
                vol_initial/vol_p300_max)
            vol_per_trans = vol_initial/num_trans
            for well in wells:
                if not p300.has_tip:
                    pick_up(p300, 1)
                for _ in range(num_trans):
                    p300.aspirate(vol_per_trans, well.bottom(1), rate=0.5)
                    p300.dispense(vol_per_trans, waste)
                p300.drop_tip()

        if not isinstance(vols_wash, list):
            vols_wash = [vols_wash for _ in range(num_cols)]

        for _ in range(wash_reps):
            magdeck.disengage()
            for well, vol_wash in zip(wells, vols_wash):
                num_trans = math.ceil(vol_wash/vol_p300_max)
                vol_per_trans = vol_wash/num_trans
                side = -1 if index_ref_list.index(well) % 2 == 0 else 1
                pick_up(p300, 1)
                for _ in range(num_trans):
                    p300.aspirate(vol_per_trans, reagent)
                    p300.dispense(vol_per_trans, well.top(-1))
                bead_mix(vol_wash*0.8, 10, well, side)
                p300.drop_tip()

            magdeck.engage(height_engage)
            ctx.delay(minutes=time_mag_incubation, msg=f'Beads separating for \
{time_mag_incubation} minutes.')

        if dests:
            pass
        else:
            for well in wells:
                pick_up(p300, 1)
                for _ in range(num_trans):
                    p300.aspirate(vol_per_trans, well.bottom(1), rate=0.5)
                    p300.dispense(vol_per_trans, waste)
                p300.drop_tip()

        magdeck.disengage()

    """ prep of beads for incubation 1 """

    beads_vol = num_samples*3*20
    wash_well_1 = mag_plate.wells()[0]
    pick_up(p300, 1)

    p300.mix(10, 200, beads_sample_1)
    num_trans = math.ceil(beads_vol/vol_p300_max)
    vol_per_trans = beads_vol/num_trans
    for _ in range(num_trans):
        p300.aspirate(vol_per_trans, beads_sample_1)
        p300.dispense(vol_per_trans, wash_well_1)
    wash([wash_well_1], buffer1, beads_vol, 500, 2)

    pick_up(p300, 1)
    p300.transfer(beads_vol, buffer1, wash_well_1, new_tip='never',
                  mix_after=(10, 200))
    p300.drop_tip()

    buffer3_vol = num_samples*3*5
    pick_up(p300, 1)
    p300.aspirate(buffer3_vol, buffer3)
    p300.dispense(buffer3_vol, wash_well_1)
    p300.drop_tip()

    """ prep of beads for incubation 2 """

    beads_vol = 150
    wash_well_2 = mag_plate.wells()[1]
    pick_up(p300, 1)
    p300.aspirate(beads_vol, beads_sample_1)
    p300.dispense(beads_vol, wash_well_2)
    wash([wash_well_2], buffer1, beads_vol, 500, 2)

    pick_up(p300, 1)
    p300.aspirate(beads_vol, buffer1)
    p300.dispense(beads_vol, wash_well_2)
    p300.mix(10, beads_vol*0.8, wash_well_2)
    shake_dests = shake_plate.rows()[0][:NUM_SAMPLES_2]  # shake plate
    shake_dests_2 = shake_plate.rows()[1][:NUM_SAMPLES_2]
    for d in shake_dests:
        p300.aspirate(50, wash_well_2)
        p300.dispense(50, d)
    p300.drop_tip()

    ctx.pause('Add sample type 2 to plate on Bioshake.')

    """ INCUBATION """
    pick_up(p300, 1)
    for _ in range(6):  # 30 minutes total
        # shake beads 2
        if SHAKE:
            actual_shake_time = 300  # 5 minutes (in seconds)
            bioshake.set_shake(500, actual_shake_time)
            bioshake.home_shaker()
            ctx.delay(seconds=actual_shake_time+10)

        # mix beads 1
        bead_mix(buffer3_vol, 10, wash_well_1, 1)
        p300.home()
    p300.drop_tip()

    # transfer beads back for washing
    wash_dests_2 = mag_plate.rows()[2][:NUM_SAMPLES_2]
    for s, d in zip(shake_dests, wash_dests_2):
        pick_up(p300, 1)
        p300.aspirate(50, s)
        p300.dispense(50, d)
        p300.drop_tip()

    wash([wash_well_1], buffer1, 90, 500, 2)
    wash(wash_dests_2, buffer1, 50, 500, 1)

    pick_up(p300, 1)
    p300.transfer(910, buffer2, wash_well_1, new_tip='never',
                  mix_after=(10, buffer3_vol*0.8))
    wells_per_col = 8 if num_samples >= 8 else num_samples
    bead_dests = [
        well for col in prep_plate1.columns()[:num_cols]
        for well in col[:wells_per_col]]
    for d in bead_dests:
        p300.aspirate(50, wash_well_1)
        p300.dispense(50, d)
    p300.drop_tip()

    for d in wash_dests_2:
        pick_up(p300, 1)
        p300.aspirate(100, buffer1)
        p300.dispense(100, d)
        p300.mix(10, 100*0.8, d)
        p300.drop_tip()

    for s in wash_dests_2:
        pick_up(p20, 1)
        p20.transfer(10, buffer3, s, new_tip='never',
                     mix_after=(10, 20))
        p20.drop_tip()

    for s, d in zip(wash_dests_2, shake_dests_2):
        pick_up(p300, 1)
        p300.aspirate(110, s)
        p300.dispense(110, d)
        p300.drop_tip()

    if SHAKE:
        actual_shake_time = 600  # 10 minutes (in seconds)
        bioshake.set_shake(500, actual_shake_time)
        bioshake.home_shaker()
        ctx.delay(seconds=actual_shake_time+10)

    # transfer beads back for washing
    wash_dests_3 = mag_plate.rows()[3][:NUM_SAMPLES_2]
    for s, d in zip(shake_dests_2, wash_dests_3):
        pick_up(p300, 1)
        p300.aspirate(110, s)
        p300.dispense(110, d)
        p300.drop_tip()

    wash(wash_dests_3, buffer1, 110, 500, 2)

    # resuspend in wash buffer 3 and transfer to incubation plate 2
    incubation_dest_sets = [
        prep_plate2.columns()[0][i*NUM_SAMPLES_1:(i+1)*NUM_SAMPLES_1]
        for i in range(NUM_SAMPLES_2)]
    num_trans = math.ceil(610/vol_p300_max)
    vol_per_trans = 610/num_trans
    for s, dest_set in zip(wash_dests_3, incubation_dest_sets):
        pick_up(p300, 1)
        for d in dest_set:
            for _ in range(num_trans):
                p300.aspirate(vol_per_trans, buffer2)
                p300.dispense(vol_per_trans, d)
            p300.mix(10, 200, d)
            p300.aspirate(100, s)
            p300.dispense(100, d)
        p300.drop_tip()

    """ BEAD PREP COMPLETE"""

    """ MM CREATION """

    # plate prep for incubation 1+2 (MM)
    num_samples_mm_creation = num_samples*3+3+1  # accounts for overage

    # add all constant reagents to each mix tube
    vol_water_mm = 16.7*num_samples_mm_creation
    vol_buffer3_mm = 5*num_samples_mm_creation
    vol_buffer4_mm = 2.5*num_samples_mm_creation
    vol_primer1_mm = 0.4*num_samples_mm_creation
    vol_primer4_mm = 0.4*num_samples_mm_creation

    for reagent, vol in zip(
            [water, buffer3, buffer4, primer1, primer4],
            [vol_water_mm, vol_buffer3_mm, vol_buffer4_mm, vol_primer1_mm,
             vol_primer4_mm]):
        pip = p300 if vol > 20 else p20
        tip_capacity = pip.tip_racks[0].wells()[0].max_volume
        num_transfers = math.ceil(vol/tip_capacity)
        vol_per_transfer = vol/num_transfers
        pick_up(pip, 1)
        for _ in range(num_transfers):
            pip.aspirate(vol_per_transfer, reagent)
            pip.dispense(vol_per_transfer, mm_tube.bottom(5))
        pip.drop_tip()

    # """ BUFFER 1 DISTRIBUTION """
    #
    # buffer_1_dests = [
    #     prep_plate1.rows()[0][:num_cols*3]] + \
    #     [prep_plate2.rows()[0][:num_cols]]
    #
    # pick_up(p300, 8)
    # for d in buffer_1_dests:
    #     p300.aspirate(200, buffer1)
    #     p300.dispense(200, d)
    # p300.drop_tip()

    ctx.pause('Store positive plate (slot 3) at 4C. Place incubation plate 1 \
(slot 2) on magnetic module. Place fresh plate on Bioshake.')

    bead_locs_1, bead_locs_2, sample_locs_1, sample_locs_2 = [
        elution_plate.rows()[0][i*num_cols:(i+1)*num_cols]
        for i in range(1, 5)]

    # add mm to elution plate
    vol_mm_per_well = 25
    wells_per_col = 8 if num_samples >= 8 else num_samples
    pick_up(p300, 1)
    for set in [bead_locs_1, bead_locs_2]:
        for well in set:
            col_ind = elution_plate.rows()[0].index(well)
            col = elution_plate.columns()[col_ind]
            for well in col[:wells_per_col]:
                p300.aspirate(vol_mm_per_well, mm_tube)
                p300.dispense(vol_mm_per_well, well)
    p300.drop_tip()

    # add sample to first set of beads
    if SHAKE:
        bioshake.temp_on(INCUBATION_TEMP)

    source_sets = [samples] + [
        mag_plate.rows()[0][i*num_cols:(i+1)*num_cols] for i in range(2)]
    dest_sets = [
        mag_plate.rows()[0][i*num_cols:(i+1)*num_cols]
        for i in range(3)]
    inc_sets = [
        shake_plate.rows()[0][i*num_cols:(i+1)*num_cols] for i in range(3)]
    source_volumes = [VOLUME_SAMPLE_1, 50, 50]
    num_pickups = num_samples if num_samples < 8 else 8
    dest_sets_inc_2 = prep_plate2.rows()[0][:num_cols]  # final for sample

    for set_ind, (vol, s_set, d_set, inc_set) in enumerate(zip(
            source_volumes, source_sets, dest_sets, inc_sets)):
        # transfer samples, then to incubation
        for s, d, inc in zip(s_set, d_set, inc_set):
            t_vol = (vol+50)*(set_ind+1)
            pick_up(p300, num_pickups)
            p300.transfer(vol, s, d, mix_after=(10, vol), new_tip='never')
            p300.transfer(t_vol, d, inc, new_tip='never')
            p300.drop_tip()
        if SHAKE:
            actual_shake_time = 30*60  # in secondss
            bioshake.set_shake(500, actual_shake_time)
            bioshake.home_shaker()
            ctx.delay(seconds=actual_shake_time+10)  # 10s safety
        # back to magdeck
        if set_ind < 2:
            for i, inc in enumerate(inc_set):
                pick_up(p300, num_pickups)
                p300.transfer(t_vol, inc, dest_sets[set_ind+1][i],
                              new_tip='never')
                p300.drop_tip()

            magdeck.engage(height_engage)
            ctx.delay(minutes=time_mag_incubation, msg=f'Beads separating for \
{time_mag_incubation} minutes.')
            num_trans = math.ceil(t_vol/vol_p300_max)
            vol_per_trans = t_vol/num_trans
            for s, d in zip(s_set, d_set):
                pick_up(p300, num_pickups)
                for _ in range(num_trans):
                    p300.aspirate(vol_per_trans, s.bottom(1), rate=0.5)
                    p300.dispense(vol_per_trans, d)
                p300.drop_tip()

            magdeck.disengage()
        else:  # transfer to second incubation plate
            for s, d in zip(dest_sets[-1], dest_sets_inc_2):
                pick_up(p300, num_pickups)
                p300.transfer(t_vol, s, d, new_tip='never')
                p300.drop_tip()

    # wash beads
    wash(dest_sets[-1], buffer1, 0, 200, 3, dests=None, remove_initial=False)

    # resuspend and transfer beads
    for s, d in zip(dest_sets[-1], bead_locs_1):
        pick_up(p300, num_pickups)
        p300.transfer(30, buffer5, s, new_tip='never', mix_after=(10, 20))
        p300.transfer(30, s.bottom(), d, new_tip='never')
        p300.drop_tip()

    ctx.pause('Place incubation plate 2 (slot 3) on magnetic module. Place \
fresh plate on Bioshake.')

    mag_set = mag_plate.rows()[0][:num_cols]
    inc_set = shake_plate.rows()[0][:num_cols]

    for m, inc in zip(mag_set, inc_set):
        pick_up(p300, num_pickups)
        p300.mix(10, 100, m)
        p300.transfer(t_vol+100, d, inc, new_tip='never')
        p300.drop_tip()
    if SHAKE:
        actual_shake_time = INCUBATION_TIME_MINUTES*60  # in seconds
        bioshake.set_shake(500, actual_shake_time)
        bioshake.home_shaker()
        ctx.delay(seconds=actual_shake_time+10)  # 10s safety
    for inc, m in zip(inc_set, mag_set):
        pick_up(p300, num_pickups)
        p300.transfer(t_vol+100, inc, m, new_tip='never')
        p300.drop_tip()

    magdeck.engage(height_engage)
    ctx.delay(minutes=time_mag_incubation, msg=f'Beads separating for \
{time_mag_incubation} minutes.')
    num_trans = math.ceil((t_vol+100)/vol_p300_max)
    vol_per_trans = (t_vol+100)/num_trans
    for m, e in zip(mag_set, sample_locs_2):
        pick_up(p300, num_pickups)
        for _ in range(num_trans):
            p300.aspirate(vol_per_trans, m.bottom(1), rate=0.5)
            p300.dispense(vol_per_trans, e)
        p300.drop_tip()

    # wash beads
    wash(mag_set, buffer1, 0, WASH_VOLUMES_INCUBATION_2, 3, dests=None, remove_initial=False)

    # resuspend and transfer beads
    for s, d in zip(mag_set, bead_locs_2):
        pick_up(p300, num_pickups)
        p300.transfer(30, buffer5, s, new_tip='never', mix_after=(10, 20))
        p300.transfer(30, s.bottom(), d, new_tip='never')
        p300.drop_tip()
