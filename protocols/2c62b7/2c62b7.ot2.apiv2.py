from opentrons import types
from datetime import datetime, timedelta
from opentrons import protocol_api
import threading
from time import sleep
import math

metadata = {
    'protocolName': 'Mag-Bind® Environmental DNA 96 Kit',
    'author': 'Sakib <sakib.hossain@opentrons.com>',
    'description': 'Custom Protocol Request',
    'apiLevel': '2.9'
}

def get_values(*names):
    import json
    _all_values = json.loads("""{"debug":"True","samples":96,"m300_mount":"left","tip_type":"standard", "mm2_vol":300,"settling_time":5}""")
    return [_all_values[n] for n in names]

def run(ctx):

    [debug, samples, m300_mount, tip_type, mm2_vol, settling_time] = get_values(  # noqa: F821
        "debug", "samples", "m300_mount", "tip_type", "mm2_vol", "settling_time")

    samples = 96
    cols = math.ceil(samples/8)

    tiprack_type = {
        'standard': 'opentrons_96_tiprack_300ul',
        'filter': 'opentrons_96_filtertiprack_200ul'
        }

    # Load Labware/Modules
    temp_mod = ctx.load_module('temperature module gen2', 3)
    mag_mod = ctx.load_module('magnetic module gen2', 1)
    mag_plate = mag_mod.load_labware('nest_96_wellplate_2ml_deep')
    tipracks = [ctx.load_labware(tiprack_type[tip_type], slot) for slot in range(7,11)]
    tip_isolator = ctx.load_labware(tiprack_type[tip_type], 11, 'Tip Isolator')
    res1 = ctx.load_labware('nest_12_reservoir_15ml', 4)
    res2 = ctx.load_labware('nest_12_reservoir_15ml', 5)
    trash = ctx.loaded_labwares[12]['A1']

    # Load Pipettes
    m300 = ctx.load_instrument('p300_multi_gen2', m300_mount, tip_racks=tipracks)
    max_tip_volume = tipracks[0]['A1'].geometry.max_volume

    # Reagents
    # Splitting A1 and A2 for 6 columns of sample each, 12 columns total
    mm2 = [well for well in res1.wells()[:2] for i in range(6)]
    vhb = [well for well in res1.wells()[2:6] for i in range(3)]

    # Helper Functions
    def debug_mode(msg, debug_setting=debug):
        if debug_setting == "True":
            ctx.pause(msg)

    def supernatant_removal(vol, src, dest, side=-1):
        m300.flow_rate.aspirate = 20
        while vol >= max_tip_volume:
            m300.aspirate(
                max_tip_volume, src.bottom().move(types.Point(x=side, y=0, z=0.5)))
            m300.dispense(max_tip_volume, dest)
            vol -= max_tip_volume
        m300.flow_rate.aspirate = 50

    def reset_flow_rates():
        m300.flow_rate.aspirate = 94
        m300.flow_rate.dispense = 94

    def pick_up(pip, loc=None):
        """Function that can be used instead of .pick_up_tip() that will pause
        robot when robot runs out of tips, prompting user to replace tips
        before resuming"""
        try:
            if loc:
                pip.pick_up_tip(loc)
            else:
                pip.pick_up_tip()
        except protocol_api.labware.OutOfTipsError:
            pip.home()
            ctx.pause("Replace the tips")
            pip.reset_tipracks()
            pip.pick_up_tip()

    def tip_mix(well, vol, reps, park_tip=False, tip_loc=None, tip_map=None, asp_speed=94, disp_speed=94):

        if not m300.has_tip:
            if tip_loc:
                pick_up(m300, tip_loc)
            else:
                pick_up(m300)
        ctx.comment('Mixing from the middle')
        m300.mix(reps, vol, well.center())
        ctx.comment('Mixing from the bottom')
        m300.mix(reps, vol, well.bottom())
        ctx.comment('Mixing from the middle')
        m300.mix(reps, vol, well.center())

        if not park_tip:
            m300.drop_tip()
        elif park_tip:
            m300.drop_tip(tip_isolator.columns()[mag_plate_wells[well]][0])

    def bind_and_remove(vol, src, dest=trash, use_park_tip=True):
        if mag_mod.status != 'engaged':
            mag_mod.engage()
        ctx.delay(minutes=settling_time, msg=f'''Incubating on MagDeck for {settling_time} minutes.''')

        if use_park_tip:
            pick_up(m300, tip_isolator.columns()[mag_plate_wells[src]][0])
        elif not use_park_tip:
            pick_up(m300)
        supernatant_removal(vol, src, dest, side=-1)
        m300.drop_tip()

    def wash(vol, src, dest):
        m300.flow_rate.dispense = 200
        pick_up(m300)
        m300.transfer(vol, src, dest, new_tip='never')
        m300.drop_tip()
        m300.flow_rate.dispense = 94


    # Wells
    # mag_plate_wells = mag_plate.rows()[0]
    mag_plate_wells = {well:column for well, column in zip(mag_plate.rows()[0][:cols], range(cols))}

    # Protocol Steps

    # Step 14
    # Transfer Master Mix 2 (XP1 Buffer + Mag-Bind® Particles RQ) to Mag Plate
    debug_mode(msg="Debug: Transfer Master Mix 2 to Mag Plate (Step 14)")
    transfer_count = 0
    for mm, dest in zip(mm2, mag_plate_wells):
        if transfer_count == 3:
            transfer_count = 0
        if transfer_count == 0:
            pick_up(m300)
            m300.mix(10, 300, mm.center())
            if cols > 6:
                m300.mix(10, 300, mm2[6].center())
            m300.drop_tip()
        pick_up(m300)
        m300.aspirate(mm2_vol, mm)
        m300.dispense(mm2_vol, dest)
        m300.drop_tip()
        transfer_count += 1

    # Step 15
    # Incubate at Room Temp for 10 Minutes while mixing
    debug_mode(msg="Debug: Incubate at Room Temperature while Mixing (Step 15)")
    for well in mag_plate_wells:
        tip_mix(well, mm2_vol/2, 10, park_tip=True, tip_map=mag_plate_wells, asp_speed=94, disp_speed=94)

    for well in mag_plate_wells:
        tip_mix(well, mm2_vol/2, 5, park_tip=True, tip_loc=tip_isolator.columns()[mag_plate_wells[well]][0], tip_map=mag_plate_wells, asp_speed=94, disp_speed=94)

    # Steps 16-18
    debug_mode(msg=f"Debug: Engage Magnet for {settling_time} minutes and then remove supernatant (Steps 16-18)")
    for well in mag_plate_wells:
        bind_and_remove(600, well, use_park_tip=True)
    if mag_mod.status == 'engaged':
        mag_mod.disengage()

    # Steps 19-20
    for src, dest in zip(vhb, mag_plate_wells):
        wash(500, src, dest)