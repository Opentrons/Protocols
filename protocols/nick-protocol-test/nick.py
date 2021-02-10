metadata = {'apiLevel': '2.9'}


def run(ctx):

    tempdeck = ctx.load_module('temperature module gen2', '1')
    tempdeck.set_temperature(4)
    plate = tempdeck.load_labware('nest_96_wellplate_100ul_pcr_full_skirt')
    tiprack300 = ctx.load_labware('opentrons_96_tiprack_300ul', '2')

    p300 = ctx.load_instrument(
        'p300_single_gen2', 'right', tip_racks=[tiprack300])

    for i in range(len(plate.columns())//2):
        col_source = plate.columns()[i*2]
        col_dest = plate.columns()[i*2+1]
        for source, dest in zip(col_source, col_dest):
            p300.transfer(100, source, dest)
