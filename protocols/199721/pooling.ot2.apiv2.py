# metadata
metadata = {
    'protocolName': 'Pooling',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.4'
}


def run(ctx):

    sample_vol, num_pools, p300_mount, tip_strategy = get_values(  # noqa: F821
        'sample_vol', 'num_pools', 'p300_mount', 'tip_strategy')

    # labware
    primary_racks_sets = [
        [ctx.load_labware(
            'alpaquaprimaryv3_24_tuberack_2000ul', slot,
            'primary rack ' + str(i+1))
         for i, slot in enumerate(set)]
        for set in [['4', '7', '10'], ['5', '8', '11']]]
    secondary_racks = [ctx.load_labware(
            'alpaquasecondaryv3_24_tuberack_750ul', slot,
            'secondary rack ' + str(i+1))
        for i, slot in enumerate(['2', '3'])]
    tipracks300 = [ctx.load_labware('opentrons_96_tiprack_300ul', slot)
                   for slot in ['1', '9']]

    # pipette
    p300 = ctx.load_instrument(
        'p300_single_gen2', p300_mount, tip_racks=tipracks300)

    for primary_racks, secondary_rack in zip(primary_racks_sets,
                                             secondary_racks):
        sources_reordered = [
            row[i*3:i*3+num_pools]
            for rack in primary_racks
            for row in rack.rows()
            for i in range(2)]
        dests = secondary_rack.wells()

        for source_set, dest in zip(sources_reordered, dests):
            if tip_strategy == 'once':
                p300.pick_up_tip()
            for source in source_set:
                if tip_strategy == 'always':
                    p300.pick_up_tip()
                p300.transfer(sample_vol, source, dest, air_gap=20,
                              new_tip='never')
                if tip_strategy == 'always':
                    p300.drop_tip()
            if tip_strategy == 'once':
                p300.drop_tip()
