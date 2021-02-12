metadata = {
    'protocolName': 'Slide Array Spotting',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.9'
}


def run(ctx):

    [] = get_values(  # noqa: F821
        )

    sample_plates = [
        ctx.load_labware('')]

    
