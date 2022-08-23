import math
from opentrons.types import Point

metadata = {
    'title': 'NGS Library Prep',
    'author': 'Nick Diehl <ndiehl@opentrons.com',
    'apiLevel': '2.11'
}


def run(ctx):

    [num_samples, num_subsamples, pipette_p20, pipette_p300, mount_p20,
     mount_p300] = get_values(  # noqa: F821
        'num_samples', 'num_subsamples', 'pipette_p20', 'pipette_p300',
        'mount_p20', 'mount_p300')

    if num_samples * num_subsamples * 2 > 96:
        raise Exception(f'Invalid number of samples ({num_samples}) and \
subsamples ({num_subsamples}). Exceeds plate capacity.')

    # labware
    sample_plate = ctx.load_labware('agilent_96_wellplate_200ul', '1',
                                    'sample plate')
    dilution_plate = ctx.load_labware('agilent_96_wellplate_200ul', '2',
                                      'dilution plate')
    pcr1_plate = ctx.load_labware('agilent_96_wellplate_200ul', '3',
                                  'PCR 1 plate')
    tipracks20 = [ctx.load_labware('opentrons_96_filtertiprack_20ul', '4')]
    tipracks200 = [ctx.load_labware('opentrons_96_filtertiprack_200ul', '5')]
    pcr2_plate = ctx.load_labware('agilent_96_wellplate_200ul', '6',
                                  'PCR 2 plate')
    tuberack = ctx.load_labware(
        'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', '7',
        'tuberack 1')
    tuberack2 = ctx.load_labware(
        'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', '8',
        'tuberack 2')

    # pipettes
    p20 = ctx.load_instrument(pipette_p20, mount_p20, tip_racks=tipracks20)
    p300 = ctx.load_instrument(pipette_p300, mount_p300, tip_racks=tipracks200)

    # reagents
    num_cols = math.ceil(num_samples/8)
    samples_single = sample_plate.wells()[:num_samples]
    samples_multi = sample_plate.rows()[0][0]  # max 8 samples
    dilution_samples_single = [
        well for row in dilution_plate.rows()[:num_samples]
        for well in row[:num_subsamples]]
    dilution_samples_multi = dilution_plate.rows()[:num_subsamples]
    pcr1_sample_sets_single = [
        row[i*2:(i+1*2)]
        for row in pcr1_plate.rows()[:num_samples]
        for i in range(num_subsamples)]
    pcr1_sample_sets_multi = [
        pcr1_plate.rows()[0][i*2:(i+1)*2]
        for i in range(num_subsamples)]
    water, mm1, reverse_primer1, mm2 = tuberack2.columns()[0][:4]

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

    """ DILUTION """
    rows_per_sample = 2 if num_subsamples > 6 else 1
    if p20.type == 'multi' and rows_per_sample == 1:  # only if samples in col
        sources, num_pickups = samples_multi, num_samples
        dest_sets = [dilution_plate.rows()[:num_subsamples]]
    else:
        sources, num_pickups = samples_single, 1
        sets = []
        for i in range(num_samples):
            rows_flat = [
                well for row in dilution_plate.rows()[
                    i*rows_per_sample:(i+1)*rows_per_sample]
                for well in row]
            sets.append(rows_flat)
        dest_sets = [set[:num_subsamples] for set in sets]

    # pre-add water
    sets = []
    for i in range(num_samples):
        rows_flat = [
            well for row in dilution_plate.rows()[
                i*rows_per_sample:(i+1)*rows_per_sample]
            for well in row]
        sets.append(rows_flat)
    dests_water_all = [
        well for set in sets
        for well in set[:num_subsamples]]
    vol_water = 9
    pick_up(p20, 1)
    for d in dests_water_all:
        p20.aspirate(vol_water, water)
        p20.dispense(vol_water, d.bottom(2))
        # touch at half radius
        p20.move_to(d.bottom().move(Point(x=d.diameter/4, z=2)))
    p20.drop_tip()

    # add samples to dilute
    vol_sample = 1
    for s, dest_set in zip(sources, dest_sets):
        for d in dest_set:
            pick_up(p20, num_pickups)
            p20.aspirate(vol_sample, s)
            p20.dispense(vol_sample, d.bottom(2))
            p20.mix(5, 8, d.bottom(2))
            # touch at half radius
            p20.move_to(d.bottom().move(Point(x=d.diameter/4, z=2)))
            p20.drop_tip()

    """ PCR1 PREP """
    # prepare PCR1 mastermixes
    num_samples_mm_creation = num_samples*2+2+1  # accounts for overage
    pcr1_map = [
        {
            'forward-primer-tube': primer_well,
            'creation-tube': creation_well,
            'volume': 0.1*num_samples_mm_creation
        }
        for creation_well, primer_well in zip(
            tuberack.wells()[:num_subsamples],
            # use max 5 primers. loop back around for subsamples 6-8
            [tuberack.wells()[8+(ind % 5)] for ind in range(num_subsamples)])
    ]

    # add all constant reagents to each mix tube
    vol_pcr_mm = 10*num_samples_mm_creation
    vol_reverse_primer_mm = 0.1*num_samples_mm_creation
    vol_water_mm = 8.8*num_samples_mm_creation
    for reagent, vol in zip(
            [mm1, reverse_primer1, water],
            [vol_pcr_mm, vol_reverse_primer_mm, vol_water_mm]):
        pip = p300 if vol > 20 else p20
        tip_capacity = pip.tip_racks[0].wells()[0].max_volume
        num_transfers = math.ceil(vol/tip_capacity)
        vol_per_transfer = vol/num_transfers
        pick_up(pip, 1)
        for item in pcr1_map:
            mix_dest = item['creation-tube']
            for _ in range(num_transfers):
                pip.aspirate(vol_per_transfer, reagent)
                pip.dispense(vol_per_transfer, mix_dest.bottom(5))
        pip.drop_tip()

    # add unique forward primers to mix and homogenize
    vol_forward_primer_mm = 0.1*num_samples_mm_creation
    pip = p300 if vol_forward_primer_mm > 20 else p20
    tip_capacity = pip.tip_racks[0].wells()[0].max_volume
    num_transfers = math.ceil(vol_forward_primer_mm/tip_capacity)
    vol_per_transfer = vol_forward_primer_mm/num_transfers
    for item in pcr1_map:
        pick_up(pip, 1)
        primer = item['forward-primer-tube']
        mix_dest = item['creation-tube']
        for _ in range(num_transfers):
            pip.aspirate(vol_per_transfer, primer)
            pip.dispense(vol_per_transfer, mix_dest.bottom(5))
        pip.mix(10, 20, mix_dest.bottom(5))
        pip.drop_tip()

    # pre-transfer mix to wellplate
    vol_mm_total = 19
    pcr1_mix_sources = [item['creation-tube'] for item in pcr1_map]
    pcr1_mix_dest_sets = [
        [well for col in pcr1_plate.columns()[i*2:(i+1)*2]
         for well in col[:num_samples]]
        for i in range(num_subsamples)
    ]
    for source, dest_set in zip(pcr1_mix_sources, pcr1_mix_dest_sets):
        pick_up(p20, 1)
        for d in dest_set:
            p20.aspirate(vol_mm_total, source)
            p20.dispense(vol_mm_total, d.bottom(2))
            p20.move_to(d.bottom().move(Point(x=d.diameter/4, z=2)))
        p20.drop_tip()

    # add DNA template to mix
    if p20.type == 'multi':
        [sources, destination_sets, num_pickups] = [
            dilution_samples_multi, pcr1_sample_sets_multi, num_samples]
    else:
        [sources, destination_sets, num_pickups] = [
            dilution_samples_single, pcr1_sample_sets_single, 1]
    vol_template = 1
    for source, dest_set in zip(sources, destination_sets):
        for d in dest_set:
            pick_up(p20, num_pickups)
            p20.aspirate(vol_template, source)
            p20.dispense(vol_template, d.bottom(2))
            p20.mix(10, 10, d.bottom(2))
            p20.move_to(d.bottom().move(Point(x=d.diameter/4, z=2)))
            p20.drop_tip()

    ctx.pause(F'RUN PCR PROFILE 1 ON PLATE IN SLOT {pcr1_plate.parent} \
NORMALIZE AND REPLACE PLATE WHEN FINISHED AND CHANGE THE TUBERACK ACCORDING \
TO REAGENT MAP 2.')

    if num_samples < 6:
        num_replicates = 4
    elif 6 <= num_samples <= 7:
        num_replicates = 3
    else:
        num_replicates = 2

    num_samples_mm_creation = num_replicates + 2

    pcr2_map = [
        {
            'forward-primer-tube': forward_primer_well,
            'reverse-primer-tube': reverse_primer_well,
            'creation-tube': creation_well,
            'volume': 0.1*num_samples_mm_creation
        }
        for creation_well, forward_primer_well, reverse_primer_well in zip(
            tuberack.wells()[:num_samples], tuberack.wells()[8:num_samples],
            tuberack.wells()[16:num_samples])
    ]

    """ add all constant reagents to each mix tube """
    vol_pcr_mm = 10*num_samples_mm_creation
    vol_water_mm = 4.8*num_samples_mm_creation
    for reagent, vol in zip(
            [mm2, water], [vol_pcr_mm, vol_water_mm]):
        pip = p300 if vol > 20 else p20
        tip_capacity = pip.tip_racks[0].wells()[0].max_volume
        num_transfers = vol/tip_capacity
        vol_per_transfer = vol/num_transfers
        pick_up(pip, 1)
        for item in pcr2_map:
            mix_dest = item['creation-tube']
            for _ in range(num_transfers):
                pip.aspirate(vol_per_transfer, reagent)
                pip.dispense(mix_dest.bottom(5))
        pip.drop_tip()

    # add unique forward/reverse primers to mix and homogenize
    vol_primer_mm = 0.1*num_samples_mm_creation
    for item in pcr2_map:
        for i, primer_type in enumerate(
                ['forward-primer-tube', 'reverse-primer-tube']):
            primer = item[primer_type]
            pip = p300 if vol_primer_mm > 20 else p20
            tip_capacity = pip.tip_racks[0].wells()[0].max_volume
            num_transfers = vol_primer_mm/tip_capacity
            vol_per_transfer = vol_forward_primer_mm/num_transfers
            pick_up(pip, 1)
            mix_dest = item['creation-tube']
            for _ in range(num_transfers):
                pip.aspirate(vol_per_transfer, primer)
                pip.dispense(mix_dest.bottom(5))
            if i == 1:
                pip.mix(10, 20, mix_dest.bottom(5))
            pip.drop_tip()

    # plate PCR mixes
    pcr2_mix_sources = [item['creation-tube'] for item in pcr2_map]
    pcr2_mix_dest_sets = [
        row[:num_replicates]
        for row in pcr2_plate.rows()[:num_samples]]
    vol_pcr2_mix = 15
    for source, dest_set in zip(pcr2_mix_sources, pcr2_mix_dest_sets):
        pick_up(p20, 1)
        for d in dest_set:
            p20.aspirate(vol_pcr2_mix, source)
            p20.dispense(vol_pcr2_mix, d.bottom(2))
            p20.move_to(d.bottom().move(Point(x=d.diameter/4, z=2)))
        p20.drop_tip()

    """ POOLING """
    if p20.type == 'multi':
        pool_source_sets = [pcr1_plate.rows()[:num_subsamples*2]]
        pool_dests = pcr1_plate.rows()[0][11:]
        pool_replicate_sets = [pcr2_plate.rows()[:num_replicates]]
        num_pickups = num_samples
    else:
        pool_source_sets = [
            row[:num_subsamples*2]
            for row in pcr1_plate.rows()[:num_samples]]
        pool_dests = pcr1_plate.columns()[-1][:num_samples]
        pool_replicate_sets = [
            row[num_replicates]
            for row in pcr2_plate.rows()[:num_samples]]
        num_pickups = 1

    # pool and distribute replicates
    vol_sample_for_pooling = 10
    for source_set, pool, replicate_set in zip(
            pool_source_sets, pool_dests, pool_replicate_sets):
        for i, s in enumerate(source_set):
            pick_up(p20, num_pickups)
            p20.aspirate(vol_sample_for_pooling, s)
            p20.dispense(vol_sample_for_pooling, pool.bottom(2))
            p20.move_to(pool.bottom().move(Point(x=pool.diameter/4, z=2)))
            if i < len(source_set) - 1:
                p20.drop_tip()
            if (i == len(source_set) - 1) and (len(source_set) > 2):
                p20.mix(10, 10, pool.bottom(2))
                p20.move_to(pool.bottom().move(Point(x=pool.diameter/4, z=2)))

        for r in pool_replicate_sets:
            p20.aspirate(5, pool)
            p20.dispense(5, r.bottom(2))
            p20.move_to(pool.bottom().move(Point(x=pool.diameter/4, z=2)))
        p20.drop_tip()
