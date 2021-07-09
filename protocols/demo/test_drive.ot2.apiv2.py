import math

metadata = {
    'protocolName': 'OT-2 Demo',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.10'
}


def run(ctx):

    [left_pip, right_pip, source_lw, dest_lw, num_samples, sample_vol,
     using_magdeck, incubation_time_mins] = get_values(  # noqa: F821
        'left_pip', 'right_pip', 'source_lw', 'dest_lw', 'num_samples',
        'sample_vol', 'using_magdeck', 'incubation_time_mins')

    # load labware
    source_labware = ctx.load_labware(source_lw, '1')
    dest_labware = ctx.load_labware(dest_lw, '2')
    if using_magdeck:
        magdeck = ctx.load_module('magnetic module gen2', '7')

    # load instrument
    pip_l = ctx.load_instrument(left_pip, 'left')
    pip_r = ctx.load_instrument(right_pip, 'right')

    tipracks_l_type = f'opentrons_96_tiprack_{pip_l.max_volume}ul'
    tipracks_r_type = f'opentrons_96_tiprack_{pip_r.max_volume}ul'
    tipracks_l = [ctx.load_labware(tipracks_l_type, '4')]
    tipracks_r = [ctx.load_labware(tipracks_r_type, '5')]

    pip_l.tip_racks = tipracks_l
    pip_r.tip_racks = tipracks_r

    # protocol
    ctx.pause('''Welcome to the OT-2 Demo Protocol-
                    This is the `Pause` function.
                    Pauses can be put at any point during a protocol
                    to replace plates, reagents, spin down plates,
                    or for any other instance where human intervention
                    is needed. Protocols continue after a `Pause` when
                    the `Resume` button is selected. Select `Resume`
                    to see more OT-2 features.''')

    if 'tuberack' in source_lw:
        pip = pip_l
        sources = source_labware.wells()[:math.ceil(num_samples/4)]
        destinations = dest_labware.wells()[:num_samples]

        for i, d in enumerate(destinations):
            pip.transfer(sample_vol, sources[i//4], d)

    else:
        pip = pip_r
        sources = source_labware.wells()[:math.ceil(num_samples/8)]
        destinations = dest_labware.rows()[0][:math.ceil(num_samples/8)]

        for s, d in zip(sources, destinations):
            pip.transfer(sample_vol, s, d)

    ctx.comment('Engaging magnetic module...')
    if using_magdeck:
        magdeck.engage(height=18)
        ctx.delay(minutes=incubation_time_mins,
                  msg=f'Incubating for {incubation_time_mins} minutes')
        ctx.comment('Protocol complete. Move labware to magnetic module for \
bead separation.')
    else:
        ctx.comment('Protocol complete. Please remove your plate for further \
processing')
