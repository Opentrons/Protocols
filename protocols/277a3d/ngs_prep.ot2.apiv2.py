metadata = {
    'protocolName': 'Oxford Nanopore 16S Barcoding NGS Prep',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.9'
}


def run(ctx):

    num_samples = ctx.get_values(  # noqa: F821
        'num_samples')

    sample_plate = ctx.load_labware('thermofishermicroamp_96_wellplate_200ul',
                                    '1', 'sample plate')
    reservoir = ctx.load_labware('nest_12_reservoir_15ml', '4', 'reservoir')
    mag_rack = ctx.load_labware('permagen_24_tuberack_1500ul', '2',
                                'magnetic rack')
    barcode_rack = ctx.load_labware(
        'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', '5',
        'barcode rack')
    reagent_rack = ctx.load_labware(
        'opentrons_24_aluminumblock_nest_2ml_snapcap', 'reagent tubes')
