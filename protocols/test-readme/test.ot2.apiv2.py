metadata = {
    'protocolName': 'Test README.md',
    'author': 'Opentrons <protocols@opentrons.com>',
    'source': 'Protocol Library',
    'apiLevel': '2.9'
}


def run(ctx):

    # raise exceptions
    plate = ctx.load_labware('nest_96_wellplate_100ul_pcr_full_skirt', '1')
    tips = ctx.load_labware('opentrons_96_tiprack_20ul', '2')
    p20 = ctx.load_instrument('p20_single_gen2', 'right', tip_racks=[tips])

    p20.transfer(5, plate.wells()[0], plate.wells(1))
