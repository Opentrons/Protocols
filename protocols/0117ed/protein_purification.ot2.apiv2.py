import sys
sys.path.append('protocols/0117ed/supplements/QOT_python_module')
from QOT import QIDevice

metadata = {
    'protocolName': 'Protein Purification and Assay Setup',
    'author': 'Nick <ndiehl@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.11'
}


def run(ctx):
    # [num_expression_blocks] = get_values(  # noqa: F821
    #  'num_expression_blocks')

    # load labware
    filtertipracks20 = [ctx.load_labware('opentrons_96_filtertiprack_20ul', '1')]
    filtertipracks200 = [ctx.load_labware('opentrons_96_filtertiprack_200ul', '2')]
    ethanol = ctx.load_labware('agilent_1_reservoir_290ml', '3',
                               'ethanol').wells()[0]
    assay_plate_1 = ctx.load_labware('protino_96_wellplate_1200ul', '4',
                                     'assay plate 1')
    assay_plate_2 = ctx.load_labware('protino_96_wellplate_1200ul', '5',
                                     'assay plate 2')
    wash_buffer = ctx.load_labware('agilent_1_reservoir_290ml', '6',
                                   'wash buffer 1').wells()[0]
    device = QIDevice(serial_number='6258', deck_position=7, adapter_set_up=1,
                      protocol=ctx)
    cell_plate = device.load_labware('corning_96_wellplate_360ul_flat', 'cell plate')
    media = ctx.load_labware('agilent_1_reservoir_290ml', '8',
                             'media').wells()[0]
    expression_block_2 = ctx.load_labware('kingfisher_96_wellplate_2200ul',
                                          '9', 'expression block 2')
    protino_plate = ctx.load_labware('protino_96_wellplate_1200ul', '10',
                                     'protino plate')
    expression_block_1 = ctx.load_labware('kingfisher_96_wellplate_2200ul',
                                          '11', 'expression block 1')
