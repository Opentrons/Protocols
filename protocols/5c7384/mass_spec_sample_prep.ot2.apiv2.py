metadata = {
    'protocolName': 'Mass Spec Sample Prep',
    'author': 'Nick <ndiehl@opentrons.com',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.9'
}


def run(ctx):

    num_samples, p20_mount, p300_mount, plate_def = get_values(  # noqa: F821
        'num_samples', 'p20_mount', 'p300_mount', 'plate_def')

    waste = ctx.load_labware('nest_1_reservoir_195ml', '1',
                             'waste container (load empty)').wells()[0].top()
    tips20 = [
        ctx.load_labware('opentrons_96_tiprack_20ul', slot)
        for slot in ['6']]
    tips300 = [
        ctx.load_labware('opentrons_96_tiprack_300ul', slot)
        for slot in ['9']]
    magdeck = ctx.load_module('magnetic module gen2', '4')
    mag_plate = magdeck.load_labware(plate_def)
    mag_samples = mag_plate.wells()[:num_samples]
    reagent_plate = ctx.load_labware(plate_def, '5', 'reagent plate')
    etoh = ctx.load_labware(
        plate_def, '2', 'ethanol plate').wells()[:num_samples]
    acetonitrile = ctx.load_labware(
        plate_def, '3', 'acetonitrile plate').wells()[:num_samples]
    tc = ctx.load_module('thermocycler')
    sample_plate = tc.load_labware(plate_def, 'sample plate')
    samples = sample_plate.wells()[:num_samples]

    dtt = reagent_plate.columns()[0]
    caa = reagent_plate.columns()[1]
    mag_bead_stock = reagent_plate.columns()[2]
    abc = reagent_plate.columns()[3:5]
    trypsin = reagent_plate.columns()[5]

    tc.set_block_temperature(60)

    p20 = ctx.load_instrument('p20_single_gen2', p20_mount, tip_racks=[])
    p300 = ctx.load_instrument('p300_single_gen2', p300_mount, tip_racks=[])

    tip_log = {}
    tip_log['tips'] = {
        p20: [tip for rack in tips20 for tip in rack.wells()],
        p300: [tip for rack in tips300 for tip in rack.wells()]}
    tip_log['max'] = {
        p20: len(tip_log['tips'][p20]),
        p300: len(tip_log['tips'][p300])}
    tip_log['count'] = {p20: 0, p300: 0}

    def _pick_up(pip, loc=None):
        if tip_log['count'][pip] == tip_log['max'][pip] and not loc:
            ctx.pause('Replace ' + str(pip.max_volume) + 'µl tipracks before \
resuming.')
            pip.reset_tipracks()
            tip_log['count'][pip] = 0
        if loc:
            pip.pick_up_tip(loc)
        else:
            pip.pick_up_tip(tip_log['tips'][pip][tip_log['count'][pip]])
            tip_log['count'][pip] += 1

    """ Reduction and Alkylation """
    for i, s in enumerate(samples):
        _pick_up(p20)
        p20.transfer(5, dtt[i % 8], s, mix_after=(2, 5), new_tip='never')
        p20.drop_tip()

    ctx.delay(minutes=30, msg='Incubating 30 minutes at 60C for reduction.')

    for i, s in enumerate(samples):
        _pick_up(p20)
        p20.transfer(5, caa[i % 8], s, mix_after=(2, 5), new_tip='never')
        p20.drop_tip()

    tc.set_block_temperature(25)
    ctx.delay(minutes=30, msg='Incubating 30 minutes at RT (25C) for \
alkylation.')

    """ Protein Binding """
    for i, s in enumerate(samples):
        _pick_up(p20)
        p20.transfer(5, mag_bead_stock[i % 8], s, mix_after=(2, 5),
                     new_tip='never')
        p20.drop_tip()

    for i, (s, a) in enumerate(zip(samples, acetonitrile)):
        _pick_up(p20)
        p20.transfer(15, a, s, mix_after=(2, 20),
                     new_tip='never')
        p20.drop_tip(tips20[0].wells()[i])

    ctx.pause('Please move plate from thermocycler to magnetic module. Resume \
when the plate has been moved.')

    magdeck.engage()
    ctx.delay(minutes=5, msg='Incubating on magnet for 5 minutes.')

    for i, m in enumerate(mag_samples):
        _pick_up(p20, tips20[0].wells()[i])
        p20.transfer(43, m.bottom(1), waste, new_tip='never')
        p20.drop_tip()

    """ Ethanol Wash """
    for wash in range(2):
        magdeck.disengage()
        for i, (m, e) in enumerate(zip(mag_samples, etoh)):
            if wash == 0:
                _pick_up(p300)
            else:
                _pick_up(p300, tips300[0].wells()[i])
            p300.transfer(200, e, m, mix_after=(10, 50), new_tip='never')
            p300.drop_tip(tips300[0].wells()[i])

        magdeck.engage()
        ctx.delay(minutes=5, msg='Incubating on magnet for 5 minutes.')

        for i, m in enumerate(mag_samples):
            _pick_up(p300, tips300[0].wells()[i])
            p300.transfer(230, m.bottom(1), waste, new_tip='never')
            # if wash == 1:
            #     p300.drop_tip()
            # else:
            p300.drop_tip(tips300[0].wells()[i])

        ctx.pause('Please replace the ethanol plate (slot 6) with a fresh \
plate of ethanol before resuming.')

    """ Acetonitrile Wash """
    magdeck.disengage()
    for i, (m, a) in enumerate(zip(mag_samples, acetonitrile)):
        _pick_up(p300, tips300[0].wells()[i])
        p300.transfer(171.5, a, m, mix_after=(10, 50), new_tip='never')
        p300.drop_tip(tips300[0].wells()[i])

    magdeck.engage()
    ctx.delay(minutes=5, msg='Incubating on magnet for 5 minutes.')

    for i, m in enumerate(mag_samples):
        _pick_up(p300, tips300[0].wells()[i])
        p300.transfer(230, m.bottom(1), waste, new_tip='never')
        p300.drop_tip()

    """ On-Bead Digestion """
    for i, s in enumerate(samples):
        _pick_up(p300)
        p300.transfer(35, abc[i//48][(i % 48) % 8], s, new_tip='never')
        p300.drop_tip()

    for i, s in enumerate(samples):
        _pick_up(p20)
        p20.transfer(5, trypsin[i % 8], s, mix_after=(2, 5), new_tip='never')
        p20.drop_tip()

    tc.set_block_temperature(37)
    ctx.comment('Protocol complete. Please shake the plate from the magnetic \
module to resuspend the beads, and replace on the thermocycler now set at \
37C.')
