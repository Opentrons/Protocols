from opentrons import types
import math

# metadata
metadata = {
    'protocolName': 'Magbead-Based Peptide Enrichment',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.0'
}


def run(ctx):

    # retrieve custom parameters
    [p50_multi_mount, p300_multi_mount,
        number_of_samples] = get_values(  # noqa: F821
            'p50_multi_mount', 'p300_multi_mount', 'number_of_samples'
        )

    # check
    if p50_multi_mount == p300_multi_mount:
        raise Exception('Pipette mounts cannot match.')
    if number_of_samples > 96 or number_of_samples < 1:
        raise Exception('Invalid sample number (must be 1-96).')

    num_cols = math.ceil(number_of_samples/8)

    # load labware
    magdeck = ctx.load_module('magdeck', '1')

    if magdeck.status == 'engaged':
        magdeck.disengage()
    magplate = magdeck.load_labware('usascientific_96_wellplate_2.4ml_deep')
    waste = ctx.load_labware(
        'nest_1_reservoir_195ml', '2', 'waste reservoir').wells()[0].top()
    res12 = ctx.load_labware(
        'nest_12_reservoir_15ml', '3', 'reagent reservoir')
    elutionplate = ctx.load_labware(
        'thermoscientific_96_wellplate_300ul', '4', 'elution plate')
    tips50 = [
        ctx.load_labware('opentrons_96_tiprack_300ul', slot)
        for slot in ['5', '6']
    ]
    tips300 = [
        ctx.load_labware('opentrons_96_tiprack_300ul', slot)
        for slot in ['7', '8', '9', '10']
    ]

    # pipettes
    m50 = ctx.load_instrument(
        'p50_multi', p50_multi_mount, tip_racks=tips50)
    m300 = ctx.load_instrument(
        'p300_multi', p300_multi_mount, tip_racks=tips300)

    # samples and reagents
    magsamples = magplate.rows()[0][:num_cols]
    elutionsamples = elutionplate.rows()[0][:num_cols]
    mgcbb = res12.wells()[:2]
    etoh = res12.wells()[3:9]
    mgceb = res12.wells()[10]

    # add MGC binding buffer
    for i, m in enumerate(magsamples):
        mgcbb_chan = mgcbb[i//6]
        m300.transfer(200, mgcbb_chan, m.bottom(5), mix_after=(15, 150))

    ctx.delay(minutes=5, msg='Incubating off magnet for 5 minutes')
    magdeck.engage()
    ctx.delay(minutes=5, msg='Incubating on magnet for 5 minutes')

    # remove supernatant
    for m in magsamples:
        m300.transfer(400, m, waste, air_gap=30)

    # etoh washes
    for wash in range(2):
        m300.pick_up_tip()
        for i, m in enumerate(magsamples):
            etoh_chan = etoh[wash*3:wash*3+3][i//4]
            m300.transfer(400, etoh_chan, m.top(), air_gap=30, new_tip='never')

        ctx.delay(seconds=30, msg='Incubating on magnet for 30 seconds.')

        # remove supernatant
        for m in magsamples:
            if not m300.hw_pipette['has_tip']:
                m300.pick_up_tip()
            m300.transfer(400, m, waste, air_gap=30, new_tip='never')
            m300.drop_tip()

    ctx.delay(minutes=15, msg='Incubating off magnet for 15 minutes')
    magdeck.disengage()

    # resuspend in elution buffer
    # establish offset location for resuspension
    x, y, z = [magsamples[0]._width*0.95/2, 0, 2]
    for i, m in enumerate(magsamples):
        sign = 1 if i % 2 == 0 else -1
        disploc = m.bottom().move(types.Point(x*sign, y, z))
        m50.pick_up_tip()
        m50.transfer(50, mgceb, disploc, new_tip='never')
        m50.mix(15, 40, m.bottom(1))
        m50.drop_tip()

    ctx.delay(minutes=1, msg='Incubating off magnet for 5 minutes')
    magdeck.engage()
    ctx.delay(minutes=1, msg='Incubating on magnet for 5 minutes')

    # transfer eluent to new plate
    for m, e in zip(magsamples, elutionsamples):
        m50.transfer(50, m.bottom(1), e.bottom(3))

    magdeck.disengage()
