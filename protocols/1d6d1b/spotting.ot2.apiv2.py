metadata = {
    'protocolName': 'Slide Array Spotting',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.9'
}


def run(ctx):

    [num_samples, m300_mount] = get_values(  # noqa: F821
        'num_samples', 'm300_mount')

    sample_plates = [
        ctx.load_labware('eppendorf_96_wellplate_350ul', slot,
                         'sample plate ' + str(i+1))
        for i, slot in enumerate(['1', '3', '4', '6'])]
    slides = ctx.load_labware('custom slide', '2', 'slides')
    pin_wash_res = ctx.load_labware('axygen_4_reservoir_73000ul', '7',
                                    'pin wash reservoir')
    blot_res = ctx.load_labware('axygen_4_reservoir_73000ul', '8',
                                'blot reservoir')
    tiprack300 = ctx.load_labware('opentrons_96_tiprack_300ul', '10')
    wash_res = ctx.load_labware('axygen_4_reservoir_73000ul', '11',
                                'wash reservoir')

    m300 = ctx.load_instrument('p300_multi_gen2', m300_mount,
                               tip_racks=tiprack300)

    # wash and blot

    def wash_blot():
        for wash, blot in zip()
