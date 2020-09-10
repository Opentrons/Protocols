# metadata
metadata = {
    'protocolName': 'Pooling',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.4'
}


def run(ctx):

    [sample_vol, num_pool_sources, num_pools, p1000_mount, asp_speed,
     dispense_speed, mix_reps, mix_vol,
     tip_strategy] = get_values(  # noqa: F821
        'sample_vol', 'num_pool_sources', 'num_pools', 'p1000_mount',
        'asp_speed', 'dispense_speed', 'mix_reps', 'mix_vol', 'tip_strategy')

    # labware
    primary_racks = [
        ctx.load_labware('alpaquaprimaryv3_24_tuberack_2000ul', slot,
                         'primary rack ' + str(i+1))
        for i, slot in enumerate(['4', '7', '10', '5', '8', '11'])]
    secondary_racks = [
        ctx.load_labware('alpaquasecondaryv3_24_tuberack_750ul', slot,
                         'secondary rack ' + str(i+1))
        for i, slot in enumerate(['2', '3'])]
    tipracks1000 = [
        ctx.load_labware('opentrons_96_tiprack_1000ul', slot)
        for slot in ['1', '9']]

    sources_reordered = [
        row[i*3:i*3+num_pool_sources]
        for rack in primary_racks
        for row in rack.rows()
        for i in range(2)][:num_pools]
    dests = [
        well for rack in secondary_racks for well in rack.wells()][:num_pools]

    # pipette
    p1000 = ctx.load_instrument(
        'p1000_single_gen2', p1000_mount, tip_racks=tipracks1000)
    p1000.flow_rate.aspirate = asp_speed
    p1000.flow_rate.dispense = dispense_speed

    for source_set, dest in zip(sources_reordered, dests):
        if tip_strategy == 'once':
            p1000.pick_up_tip()
        for i, source in enumerate(source_set):
            if tip_strategy == 'always':
                p1000.pick_up_tip()
            p1000.mix(mix_reps, mix_vol, dest)
            p1000.transfer(sample_vol, source, dest, air_gap=20,
                           new_tip='never')
            if tip_strategy == 'always':
                p1000.drop_tip()
        if tip_strategy == 'once':
            p1000.drop_tip()
