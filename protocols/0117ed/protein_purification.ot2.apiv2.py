# flake8: noqa
import sys
import os

metadata = {
    'protocolName': 'Protein Purification and Assay Setup',
    'author': 'Nick <ndiehl@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.11'
}


def run(ctx):
    [num_expression_blocks] = get_values(  # noqa: F821
     'num_expression_blocks')

    # load labware
    if not ctx.is_simulating():
        my_bioshake = bioshake.BioshakeDriver()
    bioshake_plate = ctx.load_labware('corning_96_wellplate_360ul_flat', '1')
    tipracks200 = [ctx.load_labware('opentrons_96_filtertiprack_200ul', '2')]
    cell_plate = device.load_labware('corning_96_wellplate_360ul_flat',
                                     'cell plate')
    tipracks20 = [ctx.load_labware('opentrons_96_filtertiprack_20ul', '7')]
    elution_buffer = ctx.load_labware('agilent_1_reservoir_290ml', '3',
                                      'elution buffer').wells()[0]
    assay_plate_1 = ctx.load_labware('corning_96_wellplate_360ul_flat', '4',
                                     'assay plate 1')
    assay_plate_2 = ctx.load_labware('corning_96_wellplate_360ul_flat', '5',
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

    # reagents and samples
    samples_protino = protino_plate.rows()[0]
    samples_expression_1 = expression_block_1.rows()[0]
    samples_expression_2 = expression_block_2.rows()[0]
    samples_bioshake = bioshake_plate.rows()[0]

    def replace_tipracks(pip):
        vol = pip.tip_racks[0].wells()[0].max_volume
        pip.reset_tipracks
        ctx.pause('')

    def wash(vol, source, drop=True):
        m300.pick_up_tip()
        for s in protino_plate.rows()[0]:
            m300.transfer(vol, source, s.top())
        if drop:
            m300.drop_tip()
        ctx.pause('Vacuum Protino plate to remove buffer from resin and \
replace Protino plate onto the MN shaker frame.')

    # transfer dPBS wash to protino plate
    wash(400, wash_buffer, drop=False)
    m300.move_to(samples_protino[0].top(5))

    # pipette from expression blocks to protino plate
    m300.flow_rate.aspirate /= 5
    for source_set in [samples_expression_1, samples_expression_2]
        for s, d in zip(source_set, samples_protino):
            if not m300.has_tip:
                m300.pick_up_tip()
            m300.transfer(1000, s, d, new_tip='never')
            m300.drop_tip()
        m300.reset_tipracks()
        ctx.pause('Vacuum Protino plate to remove buffer from resin and replace \
    Protino plate onto the MN shaker frame. Replace 200ul filter tiprack.')
    m300.flow_rate.aspirate *= 5

    # transfer wash buffer to protino plate
    wash(400, wash_buffer)

    # transfer wash buffer to protino plate
    wash(300, elution_buffer)

    ctx.pause('Shake plate at 900rpm for 1 minute on benchtop plate shaker, \
and elute sample into a 0.5ml 96 well block by centrifugation at 500xg for 5 minutes')
