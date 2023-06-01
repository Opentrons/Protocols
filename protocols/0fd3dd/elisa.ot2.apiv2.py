metadata = {
    'protocolName': 'ELISA',
    'author': 'Nick Diehl <ndiehl@opentrons.com>',
    'apiLevel': '2.13'
}


def run(ctx):

    # labware
    sample_plate = ctx.load_labware('thermo_96_wellplate_400ul', '1',
                                    'sample plate')
    elisa_plate = ctx.load_labware('thermo_96_wellplate_400ul', '2')
    res12 = ctx.load_labware('starlab_12_reservoir_22000ul', '4')
    res1 = ctx.load_labware('starlab_1_reservoir_240000ul', '5')
    waste = ctx.load_labware(
        'starlab_1_reservoir_240000ul', '3').wells()[0].top()
    tipracks300 = [
        ctx.load_labware('opentrons_96_tiprack_300ul', slot)
        for slot in ['6']]

    # pipettes
    p300 = ctx.load_labware('p300_single_gen2', 'left', tip_racks=tipracks300)
    m300 = ctx.load_labware('p300_multi_gen2', 'right', tip_racks=tipracks300)

    # liquids

    # protocol steps
    samples = []
    destination_sets = []

    ctx.pause(minutes=60, msg='Incubating for 1 hour')

    def remove_supernatant(volume):
        