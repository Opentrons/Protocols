metadata = {
    'protocolName': 'Adding Developer Solution to 216 Well Cartridge Plate',
    'author': 'Rami Farawi <rami.farawi@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.9'
}


def run(ctx):

    [height_above_cartridge, disp_vol, asp_rate, disp_rate,
     asp_delay_time, disp_delay_time, p300_mount] = get_values(  # noqa: F821
        "height_above_cartridge", "disp_vol", "asp_rate", "disp_rate",
        "asp_delay_time", "disp_delay_time", "p300_mount")

    if not 0.1 <= height_above_cartridge <= 10:
        raise Exception("Enter a height between 1 and 10mm")
    if not 1 <= disp_vol <= 85:
        raise Exception("Enter a dispense volume between 1 and 85µL")

    # load labware
    plate = ctx.load_labware('generic_216_wellplate_85ul_flat', '1')
    reservoir = ctx.load_labware('nest_1_reservoir_195ml', '6')
    tiprack = ctx.load_labware('opentrons_96_tiprack_300ul', '9')

    # load instruments
    p300 = ctx.load_instrument('p300_single_gen2', p300_mount,
                               tip_racks=[tiprack])

    # protocol
    p300.flow_rate.dispense = asp_rate
    p300.flow_rate.dispense = disp_rate

    p300.pick_up_tip()
    for well in plate.wells():
        p300.aspirate(disp_vol, reservoir.wells()[0])
        ctx.delay(seconds=asp_delay_time)
        p300.dispense(disp_vol, well)
        p300.blow_out()
        ctx.delay(seconds=disp_delay_time)
    p300.drop_tip()
