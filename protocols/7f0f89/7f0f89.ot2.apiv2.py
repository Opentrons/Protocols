def get_values(*names):
    import json
    _all_values = json.loads("""{"num_samp": 1, "height_above_cartridge":2,"disp_vol":80, "asp_delay_time": 2,"disp_delay_time":2,"asp_rate":20,"disp_rate":20,"p300_mount":"right"}""")
    return [_all_values[n] for n in names]

import math

metadata = {
    'protocolName': 'Adding Developer Solution to 216 Well Cartridge Plate',
    'author': 'Rami Farawi <rami.farawi@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.9'
}


def run(ctx):

    [num_samp, height_above_cartridge, disp_vol, asp_rate, disp_rate,
     asp_delay_time, disp_delay_time, p300_mount] = get_values(  # noqa: F821
        "num_samp", "height_above_cartridge", "disp_vol", "asp_rate",
        "disp_rate", "asp_delay_time", "disp_delay_time", "p300_mount")

    if not 1 <= num_samp <= 216:
        raise Exception("Enter a sample number between 1 and 216")
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
    chunks = [plate.wells()[i:i+3] for i in range(
              0, len(plate.wells()), 3)][:math.ceil(num_samp/3)]
    if num_samp % 3 == 1:
        chunks[-1].pop()
        chunks[-1].pop()
    elif num_samp % 3 == 2:
        chunks[-1].pop()

    p300.pick_up_tip()
    for chunk in chunks:
        p300.aspirate(disp_vol*3+20, reservoir.wells()[0])  # aspirate extra
        ctx.delay(seconds=asp_delay_time)
        for well in chunk:
            p300.dispense(disp_vol, well.top(height_above_cartridge))
            ctx.delay(seconds=disp_delay_time)
        p300.dispense(20, reservoir.wells()[0])
    p300.blow_out(reservoir.wells()[0])
    p300.drop_tip()
