metadata = {
    'protocolName': 'Dispensing Diluted Phage to Agar Plates',
    'author': 'Rami Farawi <rami.farawi@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.11'
}


def run(ctx):

    [num_plates, num_col, num_row, p20_mount] = get_values(  # noqa: F821
        "num_plates", "num_col", "num_row", "p20_mount")

    num_col = int(num_col)
    num_row = int(num_row)
    num_plates = int(num_plates)

    # load labware
    agar1 = ctx.load_labware('127x85_agar_plate1', '2')
    agar2 = ctx.load_labware('127x85_agar_plate2', '3')
    agar3 = ctx.load_labware('127x85_agar_plate3', '4')
    agar4 = ctx.load_labware('127x85_agar_plate4', '5')
    agar5 = ctx.load_labware('127x85_agar_plate5', '6')
    dilution_plate = ctx.load_labware('corning_96_wellplate_360ul_flat', '1')
    tiprack = ctx.load_labware('opentrons_96_filtertiprack_20ul', '10')

    # load instrument
    m20 = ctx.load_instrument('p20_multi_gen2', p20_mount, tip_racks=[tiprack])

    # multi as single channel
    num_chan = num_row
    tips_ordered = [
                    tip
                    for row in tiprack.rows()[
                     len(tiprack.rows())-num_chan::-1*num_chan]
                    for tip in row]

    tip_count = 0

    def pick_up():
        nonlocal tip_count
        m20.pick_up_tip(tips_ordered[tip_count])
        tip_count += 1

    # PROTOCOL
    plates = [agar1, agar2, agar3, agar4, agar5][:num_plates]
    airgap = 1
    for col_ctr in range(num_col):
        pick_up()
        for _ in range(num_plates):
            m20.aspirate(2.5, dilution_plate.rows()[0][col_ctr])
            m20.touch_tip()
            m20.air_gap(airgap)
        for plate in plates:
            m20.dispense(2.5+airgap, plate.rows()[0][col_ctr], rate=0.5)
        m20.drop_tip()
        ctx.comment('\n\n\n\n')
