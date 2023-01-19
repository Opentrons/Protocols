import math
from opentrons.types import Point

metadata = {
    'protocolName': 'Mass Spec Sample Prep',
    'author': 'Nick Diehl <ndiehl@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.13'
}


def run(ctx):

    [num_samples, tip_start_samples, vol_sample, vol_meoh, vol_mq,
     col_meoh, col_mq, vol_sample_redissolved, mount_p300, mount_m300
     ] = get_values(  # noqa: F821
        'num_samples', 'tip_start_samples', 'vol_sample', 'vol_meoh', 'vol_mq',
         'col_meoh', 'col_mq', 'vol_sample_redissolved', 'mount_p300',
         'mount_m300')

    num_racks = math.ceil(num_samples/24)
    num_cols = math.ceil(num_samples/8)
    vol_air_gap = 20.0

    # labware
    source_racks = [
        ctx.load_labware(
            'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', slot,
            f'source plate {i+1}')
        for i, slot in enumerate(['1', '2', '3'][:num_racks])]
    tipracks300s = [ctx.load_labware('opentrons_96_tiprack_300ul', '9')]
    stacked_plate = ctx.load_labware(
        'spestackedoncollection_96_wellplate_1600ul', '5',
        'SPE stacked on collection plate')
    tipracks300m = [
        ctx.load_labware('opentrons_96_tiprack_300ul', slot)
        for slot in ['6', '11']]
    collection_plate = ctx.load_labware('greinerbioone_96_wellplate_2000ul',
                                        '7', 'collection plate')
    reservoir = ctx.load_labware('nest_12_reservoir_15ml', '8', 'reservoir')
    final_plate = ctx.load_labware('axygen_96_plate_200ul_pcr', '10')

    # pipettes
    p300 = ctx.load_instrument(
        'p300_single_gen2',
        mount_p300,
        tip_racks=tipracks300s)
    p300.starting_tip = tipracks300s[0].wells_by_name()[tip_start_samples]
    m300 = ctx.load_instrument(
        'p300_multi_gen2',
        mount_m300,
        tip_racks=tipracks300m)

    def wick(well, pip, side=1):
        pip.move_to(well.bottom().move(Point(x=side*well.diameter/2*0.8, z=3)))

    def slow_withdraw(well, pip):
        ctx.max_speeds['A'] = 25
        ctx.max_speeds['Z'] = 25
        pip.move_to(well.top())
        del ctx.max_speeds['A']
        del ctx.max_speeds['Z']

    # reagents
    samples_source = [
        well for rack in source_racks for well in rack.wells()][:num_samples]
    samples_stacked_s = stacked_plate.wells()[:num_samples]
    samples_stacked_m = stacked_plate.rows()[0][:num_cols]
    samples_collection_m = collection_plate.rows()[0][:num_cols]
    samples_final_m = final_plate.rows()[0][:num_cols]
    meoh = reservoir.rows()[0][col_meoh-1]
    mq = reservoir.rows()[0][col_mq-1]

    # transfer sample
    for s, d in zip(samples_source, samples_stacked_s):
        p300.pick_up_tip()
        p300.aspirate(vol_sample, s)
        slow_withdraw(s, p300)
        p300.dispense(vol_sample, d.bottom(2))
        slow_withdraw(d, p300)
        p300.drop_tip()

    ctx.pause('RESUME WHEN READY')

    for _ in range(2):
        m300.pick_up_tip()
        for d in samples_stacked_m:
            m300.aspirate(vol_air_gap, meoh.top())  # pre air gap
            m300.aspirate(vol_meoh, meoh)
            slow_withdraw(meoh, m300)
            m300.aspirate(vol_air_gap, meoh.top())
            m300.dispense(m300.current_volume, d.top(-1))
        m300.drop_tip()

        ctx.pause('RESUME WHEN READY')

    m300.pick_up_tip()
    for d in samples_stacked_m:
        m300.aspirate(vol_mq, mq)
        slow_withdraw(mq, m300)
        m300.dispense(m300.current_volume, d.top(-1))
    m300.drop_tip()

    ctx.pause('RESUME WHEN READY')

    for tip, s, d in zip(
            m300.tip_racks[1].rows()[0][:num_cols],
            samples_collection_m,
            samples_final_m):
        m300.pick_up_tip(tip)
        m300.aspirate(vol_sample_redissolved, s)
        slow_withdraw(s, m300)
        m300.dispense(vol_sample, d)
        slow_withdraw(d, m300)
        m300.drop_tip()
