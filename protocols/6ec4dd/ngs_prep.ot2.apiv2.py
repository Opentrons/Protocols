metadata = {
    'protocolName': 'NGS Library Prep',
    'author': 'Nick <protocols@opentrons.com>',
    'apiLevel': '2.10'
}


def run(ctx):

    num_samples, m20_mount = get_values(  # noqa: F821
        'num_samples', 'm20_mount')

    # labware and modules
    magdeck = ctx.load_module('magnetic module gen2', '1')
    mag_plate = magdeck.load_labware('nest_96_wellplate_100ul_pcr_full_skirt')
    

    m20 = ctx.load_instrument('p20_multi_gen2', m20_mount, tip_racks=[])
