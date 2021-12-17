import sys
import os
dir = 'protocols/0117ed/supplements/QOT_python_module'
if os.path.isdir(dir):
    sys.path.append(dir)
from QOT import QIDevice

metadata = {
    'protocolName': 'Protein Purification and Assay Setup',
    'author': 'Nick <ndiehl@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.11'
}


def run(ctx):
    [serial_number, setup_number,
     num_expression_blocks] = get_values(  # noqa: F821
     'serial_number', 'setup_number', 'num_expression_blocks')

    # load labware
    device = QIDevice(serial_number=serial_number, deck_position=1,
                      adapter_set_up=setup_number, protocol=ctx)
    cell_plate = device.load_labware('corning_96_wellplate_360ul_flat',
                                     'cell plate')
    tipracks20 = [ctx.load_labware('opentrons_96_filtertiprack_20ul', '7')]
    tipracks200 = [ctx.load_labware('opentrons_96_filtertiprack_200ul', '2')]
    ethanol = ctx.load_labware('agilent_1_reservoir_290ml', '3',
                               'ethanol').wells()[0]
    assay_plate_1 = ctx.load_labware('protino_96_wellplate_1200ul', '4',
                                     'assay plate 1')
    assay_plate_2 = ctx.load_labware('protino_96_wellplate_1200ul', '5',
                                     'assay plate 2')
    wash_buffer = ctx.load_labware('agilent_1_reservoir_290ml', '6',
                                   'wash buffer 1').wells()[0]
    media = ctx.load_labware('agilent_1_reservoir_290ml', '8',
                             'media').wells()[0]
    expression_block_2 = ctx.load_labware('kingfisher_96_wellplate_2200ul',
                                          '9', 'expression block 2')
    protino_plate = ctx.load_labware('protino_96_wellplate_1200ul', '10',
                                     'protino plate')
    expression_block_1 = ctx.load_labware('kingfisher_96_wellplate_2200ul',
                                          '11', 'expression block 1')

    # pipettes
    m300 = ctx.load_instrument('p300_multi_gen2', 'left',
                               tip_racks=tipracks200)
    m20 = ctx.load_instrument('p20_multi_gen2', 'right', tip_racks=tipracks20)

    def pick_up(pip):
        try:

    # transfer dPBS wash to protino plate
    m300.pick_up_tip()
    for s in protino_plate.rows()[0]:
        m300.transfer(400, )
