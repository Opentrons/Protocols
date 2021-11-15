metadata = {
    'protocolName': 'LCMS Urine Extraction',
    'author': 'Rami Farawi <rami.farawi@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.11'
 }


def run(ctx):

    [num_samp, p300_mount, p1000_mount] = get_values(  # noqa: F821
        "num_samp", "p300_mount", "p1000_mount")

    if not 1 <= num_samp <= 96:
        raise Exception("Enter a sample number between 1-96")

    # labware
    urine_tube_rack = [ctx.load_labware(
                        'opentrons_15_tuberack_nest_15ml_conical', slot)
                       for slot in ['1']]
    plate = ctx.load_labware('biorad_96_wellplate_200ul_pcr', '2')
    reservoir12 = ctx.load_labware(
                            'opentrons_15_tuberack_nest_15ml_conical', '3')
    reservoir = ctx.load_labware('agilent_1_reservoir_290ml', '9')
    tips1000 = [ctx.load_labware('opentrons_96_filtertiprack_1000ul', '4')]
    tips20 = [ctx.load_labware('opentrons_96_tiprack_300ul', '5')]

    # instrument
    p300 = ctx.load_instrument('p300_single_gen2', p300_mount,
                               tip_racks=tips20)
    p1000 = ctx.load_instrument('p1000_single_gen2', p1000_mount,
                                tip_racks=tips1000)

    def create_chunks(list, n):
        for i in range(0, len(list), n):
            yield list[i:i+n]

    # reagents
    methanol = reservoir.wells()[0]
    buffer = reservoir12.wells()[:3]
    negative_urine = urine_tube_rack[0].wells()[1:8]
    spike = urine_tube_rack[0].rows()[-1][0]
    enzyme = urine_tube_rack[0].rows()[-1][1]
    water = urine_tube_rack[0].rows()[-1][2]

    # add enzyme to all wells
    p300.pick_up_tip()
    p300.distribute(60, enzyme,
                    [well for well in plate.wells()[:num_samp]],
                    new_tip='never')
    p300.drop_tip()

    # add buffer to all wells
    p1000.pick_up_tip()
    for source, chunk in zip(buffer*num_samp,
                             create_chunks(plate.wells()[:num_samp], 2)):
        p1000.aspirate(660, source)
        for well in chunk:
            p1000.dispense(340, well)
    p1000.drop_tip()

    # add negative urine (blank)
    p300.pick_up_tip()
    p300.aspirate(300, urine_tube_rack[0].wells()[0])
    p300.dispense(300, plate.wells()[0])
    p300.drop_tip()

    # add negative urine (cals)
    for tube, well in zip(negative_urine, plate.wells()[1:]):
        p300.pick_up_tip()
        p300.aspirate(270, tube)
        p300.dispense(270, well)
        p300.drop_tip()

    # add spike
    p300.pick_up_tip()
    p300.distribute(20, spike,
                    [well.top() for well in plate.wells()[:num_samp]],
                    new_tip='never')
    p300.drop_tip()

    # add water
    p300.pick_up_tip()
    p300.distribute(30, water,
                    [well.top() for well in plate.wells()[:num_samp]],
                    new_tip='never')
    p300.drop_tip()

    ctx.delay(minutes=30)

    # add methanol
    p300.pick_up_tip()
    p300.distribute(700, methanol,
                    [well.top() for well in plate.wells()[:num_samp]],
                    new_tip='never')
    p300.drop_tip()
