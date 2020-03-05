import math

# metadata
metadata = {
    'protocolName': 'Copy Number Variant (CNV) Plating',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.0'
}


def run(ctx):

    p10_multi_mount, num_samples, num_reps = get_values(  # noqa: F821
        'p10_multi_mount', 'num_samples', 'num_reps')

    # load labware
    mm_plate = ctx.load_labware(
        'microampoptical_384_wellplate_30ul', '1', 'mastermix plate')
    plate384 = ctx.load_labware(
        'microampoptical_384_wellplate_30ul', '2', '384-well plate')
    dilution_plate = ctx.load_labware(
        'usascientific_96_wellplate_100ul', '3', 'CNV dilution plate')
    tipracks = [
        ctx.load_labware('opentrons_96_tiprack_10ul', str(slot))
        for slot in range(4, 7)
    ]

    # load pipette
    m10 = ctx.load_instrument('p10_multi', p10_multi_mount, tip_racks=tipracks)

    # transfer mastermix to all 384 wells
    num_cols = math.ceil(num_samples/8)
    mm_sources = mm_plate.rows()[0][:num_reps]
    mm_dest_sets = [
        [
            [well
             for set in [row[i*2:i*2+2] for row in plate384.rows()[:2]]
             for well in set[:num_reps]][n]
            for i in range(12)
        ][:num_cols]
        for n in range(num_reps)
    ]
    for s, d_set in zip(mm_sources, mm_dest_sets):
        m10.pick_up_tip()
        for d in d_set:
            m10.air_gap(2)
            m10.aspirate(8, s)
            m10.dispense(10, d)
            m10.blow_out(d.bottom(3))
        m10.drop_tip()

    # setup DNA sources and destinations
    dna_source_sets = dilution_plate.rows()[0]
    dna_dest_sets = [
        [well
         for set in [row[i*2:i*2+2] for row in plate384.rows()[:2]]
         for well in set[:num_reps]]
        for i in range(12)
    ][:num_cols]

    # transfer DNA in triplicate
    for s, d_set in zip(dna_source_sets, dna_dest_sets):
        for d in d_set:
            m10.pick_up_tip()
            m10.air_gap(3)
            m10.aspirate(2, s)
            m10.air_gap(2)
            m10.dispense(2, d.top(-2))
            m10.aspirate(5)
            m10.dispense(7, d)
            m10.dispense(3, d.bottom(3))
            m10.blow_out(d.bottom(3))
            m10.drop_tip()
