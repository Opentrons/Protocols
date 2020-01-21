from opentrons import types

# metadata
metadata = {
    'protocolName': 'Magbead-Based Peptide Enrichment',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.0'
}


def run(ctx):

    # retrieve custom parameters
    [p300_single_mount, number_of_samples] = get_values(  # noqa: F821
            'p300_single_mount', 'number_of_samples')
    # [p300_single_mount, number_of_samples] = ['right', 96]

    # check
    if number_of_samples > 96 or number_of_samples < 1:
        raise Exception('Invalid sample number (must be 1-96).')

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
    tips300 = [
        ctx.load_labware('opentrons_96_tiprack_300ul', str(slot))
        for slot in range(5, 11)
    ]

    # pipettes
    p300 = ctx.load_instrument(
        'p300_single_gen2', p300_single_mount, tip_racks=tips300)
    p300.flow_rate.aspirate = 150
    p300.flow_rate.dispense = 300

    # samples and reagents
    magsamples = [
        well for row in magplate.rows() for well in row][:number_of_samples]
    elutionsamples = [
        well
        for row in elutionplate.rows() for well in row][:number_of_samples]
    mgcbb = res12.wells()[:2]
    etoh = res12.wells()[3:9]
    mgceb = res12.wells()[10]

    # add MGC binding buffer
    for i, m in enumerate(magsamples):
        mgcbb_chan = mgcbb[i//48]
        p300.transfer(200, mgcbb_chan, m.bottom(5), mix_after=(5, 150))

    ctx.delay(minutes=5, msg='Incubating off magnet for 5 minutes')
    magdeck.engage()
    ctx.delay(minutes=5, msg='Incubating on magnet for 5 minutes')

    # remove supernatant
    for m in magsamples:
        p300.transfer(400, m, waste, air_gap=30)

    # etoh washes
    for wash in range(2):
        p300.pick_up_tip()
        for i, m in enumerate(magsamples):
            etoh_chan = etoh[wash*3:wash*3+3][i//32]
            p300.transfer(400, etoh_chan, m.top(), air_gap=30, new_tip='never')

        ctx.delay(seconds=30, msg='Incubating on magnet for 30 seconds.')

        # remove supernatant
        for m in magsamples:
            if not p300.hw_pipette['has_tip']:
                p300.pick_up_tip()
            p300.transfer(400, m, waste, air_gap=30, new_tip='never')
            p300.drop_tip()

    ctx.delay(minutes=15, msg='Incubating off magnet for 15 minutes')
    magdeck.disengage()

    # resuspend in elution buffer
    # establish offset location for resuspension
    x, y, z = [magsamples[0]._width*0.95/2, 0, 2]
    for i, m in enumerate(magsamples):
        sign = 1 if i//8 % 2 == 0 else -1
        disploc = m.bottom().move(types.Point(x*sign, y, z))
        p300.pick_up_tip()
        p300.aspirate(50, mgceb)
        p300.move_to(m.center())
        p300.dispense(50, disploc)
        p300.mix(5, 40, m.bottom(1))
        p300.drop_tip()

    ctx.delay(minutes=1, msg='Incubating off magnet for 5 minutes')
    magdeck.engage()
    ctx.delay(minutes=1, msg='Incubating on magnet for 5 minutes')

    # transfer eluent to new plate
    for m, e in zip(magsamples, elutionsamples):
        p300.transfer(50, m.bottom(1), e.bottom(3))

    magdeck.disengage()
