metadata = {
    'protocolName': 'Mass Spec Sample Prep',
    'author': 'Nick <ndiehl@opentrons.com',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.9'
}


def run(ctx):

    num_samples, p20_mount, p300_mount = get_values(  # noqa: F821
        'num_samples', 'p20_mount', 'p300_mount')

    tc = ctx.load_module('thermocycler')
    tc_plate = tc.load_labware('nest_96_wellplate_100ul_pcr_full_skirt')
    tc.set_lid_temperature(105)
    tc.set_block_temperature(95)

    p20 = ctx.load_instrument('p20_single_gen2', p20_mount, tip_racks=[])
    p300 = ctx.load_instrument('p20_single_gen2', p20_mount, tip_racks=[])
