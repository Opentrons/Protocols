from opentrons import types
from datetime import datetime, timedelta
from opentrons import protocol_api
import threading
from time import sleep

metadata = {
    'protocolName': 'Mag-Bind® Environmental DNA 96 Kit',
    'author': 'Sakib <sakib.hossain@opentrons.com>',
    'description': 'Custom Protocol Request',
    'apiLevel': '2.9'
}

def get_values(*names):
    import json
    _all_values = json.loads("""{"debug":"True","m300_mount":"left", "tip_type":"filter"}""")
    return [_all_values[n] for n in names]

def run(ctx):

    [debug, m300_mount, tip_type] = get_values(  # noqa: F821
        "debug", "m300_mount", "tip_type")

    tiprack_type = {
        'standard': 'opentrons_96_tiprack_300ul',
        'filter': 'opentrons_96_filtertiprack_200ul'
        }

    # Load Labware/Modules
    temp_mod = ctx.load_module('temperature module gen2', 3)
    mag_mod = ctx.load_module('magnetic module gen2', 1)
    mag_plate = mag_mod.load_labware('nest_96_wellplate_2ml_deep')
    tipracks = [ctx.load_labware(tiprack_type[tip_type], slot) for slot in range(7,11)]
    tip_isolator = ctx.load_labware('opentrons_96_filtertiprack_200ul', 11, 'Tip Isolator')
    res1 = ctx.load_labware('nest_12_reservoir_15ml', 4)
    res2 = ctx.load_labware('nest_12_reservoir_15ml', 5)

    # Load Pipettes
    m300 = ctx.load_instrument('p300_multi_gen2', m300_mount, tip_racks=tipracks)

    # Reagents
    mm2 = [well for well in res1.wells()[:2] for i in range(6)]

    # Helper Functions
    def debug_mode(msg, debug_setting=debug):
        if debug_setting == "True":
            ctx.pause(msg)

    def supernatant_removal(vol, src, dest, side):
        m300.flow_rate.aspirate = 20
        asp_ctr = 0
        while vol > 180:
            m300.aspirate(
                180, src.bottom().move(types.Point(x=side, y=0, z=0.5)))
            m300.dispense(180, dest)
            m300.aspirate(10, dest)
            vol -= 180
            asp_ctr += 1
        m300.aspirate(
            vol, src.bottom().move(types.Point(x=side, y=0, z=0.5)))
        dvol = 10*asp_ctr + vol
        m300.dispense(dvol, dest)
        m300.flow_rate.aspirate = 50

    def reset_flow_rates():
        m300.flow_rate.aspirate = 94
        m300.flow_rate.dispense = 94

    def pick_up(pip):
        """Function that can be used instead of .pick_up_tip() that will pause
        robot when robot runs out of tips, prompting user to replace tips
        before resuming"""
        try:
            pip.pick_up_tip()
        except protocol_api.labware.OutOfTipsError:
            pip.home()
            ctx.pause("Replace the tips")
            pip.reset_tipracks()
            pip.pick_up_tip()


    # Wells
    mag_plate_wells = mag_plate.rows()[0]

    # Protocol Steps

    # Step 14
    # Transfer Master Mix 2 (XP1 Buffer + Mag-Bind® Particles RQ) to Mag Plate
    debug_mode(msg="Debug: Transfer Master Mix 2 to Mag Plate")
    mix_count = 0
    
    m300.transfer(150, mm2, mag_plate_wells, mix_after=(10, 100), new_tip='always')



    # # Step 15
    # # Incubate at Room Temp for 10 Minutes while mixing
    # now = datetime.now()
    # # now_plus_10 = now + timedelta(minutes = 10)
    # now_plus_10 = now + timedelta(seconds = 10)
    # # Determine how many mixes can be done per column
    # while datetime.now() < now_plus_10:
    #     for col in mag_plate_wells:
    #         pick_up(m300)
    #         m300.mix(3, 100, col)
    #         m300.return_tip()







    # print(ctx.loaded_labwares)
