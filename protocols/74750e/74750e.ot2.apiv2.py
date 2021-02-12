metadata = {'apiLevel': '2.7'}


def run(ctx):

    # labware setup
    tiprack = ctx.load_labware('opentrons_96_tiprack_300ul', '1')
    plates = [ctx.load_labware('corning_96_wellplate_360ul_flat', slot)
              for slot in ['2', '3', '4', '5']]

    # instrument setup
    p300 = ctx.load_instrument('p300_multi_gen2', 'left', tip_racks=[tiprack])

    # commands
    num_dilutions = 6
    glob_num_dilutions = num_dilutions*len(plates)

    source = [s for plate in plates for s in
              zip(plate.rows()[0][:num_dilutions],
                  plate.rows()[0][1:num_dilutions+1])]

    if not p300.has_tip:
        p300.pick_up_tip()

    for col in range(0, glob_num_dilutions):
        if col % num_dilutions == 0 and col != 0:
            p300.mix(12, 100, source[col-1][1])
            p300.aspirate(20, source[col-1][1])
            p300.drop_tip()
            p300.pick_up_tip()
        p300.transfer(20, source[col][0], source[col][1],
                      mix_before=(12, 100), new_tip='never')

    p300.mix(12, 100, source[col][1])
    p300.aspirate(20, source[col][1])
    p300.drop_tip()
