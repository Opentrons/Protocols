metadata = {
    'protocolName': 'TMTpro 18-plex Mass Spec Sample Prep',
    'author': 'Nick Diehl <ndiehl@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.11'
}


def run(ctx):

    [num_tmt, p300_mount] = get_values(  # noqa: F821
        'num_tmt', 'p300_mount')

    if not 1 <= num_tmt <= 18:
        raise Exception(f'Invalid number of reagents ({num_tmt}). Must be \
1-18.')

    plate = ctx.load_labware('nest_96_wellplate_100ul_pcr_full_skirt', '2',
                             'plate')
    rack = ctx.load_labware(
        'opentrons_24_aluminumblock_nest_2ml_screwcap', '1', 'vial rack')
    tiprack = [ctx.load_labware('opentrons_96_tiprack_300ul', '4')]

    p300 = ctx.load_instrument('p300_single_gen2', p300_mount,
                               tip_racks=tiprack)

    tmt = [well for row in rack.rows()[1:] for well in row][:num_tmt]

    dest_sets = [
        [well for row in plate.rows()[i*2:(i+1)*2] for well in row[:9]]
        for i in range(4)] + [
        [well for col in plate.columns()[9:] for well in col][:18]]

    # transfer each tmt
    for i, t in enumerate(tmt):
        p300.pick_up_tip()
        for set in dest_sets:
            p300.transfer(20, t, set[i], new_tip='never')
        p300.drop_tip()
