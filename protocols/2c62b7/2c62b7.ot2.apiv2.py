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
    _all_values = json.loads("""{"m300_mount":"left", "tip_type":"filter"}""")
    return [_all_values[n] for n in names]

# Definitions for deck light flashing
class CancellationToken:
    def __init__(self):
        self.is_continued = False

    def set_true(self):
        self.is_continued = True

    def set_false(self):
        self.is_continued = False

def turn_on_blinking_notification(hardware, pause):
    while pause.is_continued:
        hardware.set_lights(rails=True)
        sleep(1)
        hardware.set_lights(rails=False)
        sleep(1)

def create_thread(ctx, cancel_token):
    t1 = threading.Thread(target=turn_on_blinking_notification,
                          args=(ctx._hw_manager.hardware, cancel_token))
    t1.start()
    return t1

def run(ctx):

    [m300_mount, tip_type] = get_values(  # noqa: F821
        "m300_mount", "tip_type")

    tiprack_type = {
        'standard': 'opentrons_96_tiprack_300ul',
        'filter': 'opentrons_96_filtertiprack_200ul'
        }

    # Load Labware/Modules
    temp_mod = ctx.load_module('temperature module gen2', 3)
    ez_disruptor_plate = temp_mod.load_labware('nest_96_wellplate_2ml_deep') # Replace API name with E-Z 96 Disruptor Plate C Plus
    mag_mod = ctx.load_module('magnetic module gen2', 1)
    mag_plate = mag_mod.load_labware('nest_96_wellplate_2ml_deep')
    microtubes_96_well_racked = ctx.load_labware('corning_96_wellplate_360ul_flat', 2)
    tipracks = [ctx.load_labware(tiprack_type[tip_type], slot) for slot in range(7,11)]
    res1 = ctx.load_labware('nest_12_reservoir_15ml', 4)
    res2 = ctx.load_labware('nest_12_reservoir_15ml', 5)
    res3 = ctx.load_labware('nest_12_reservoir_15ml', 6)

    # Load Pipettes
    m300 = ctx.load_instrument('p300_multi_gen2', m300_mount, tip_racks=tipracks)

    # Reagents
    mm1 = [well for well in res1.wells()[:4] for i in range(3)]
    lysozyme = res1.wells()[5]
    ds_buffer = res1.wells()[7]
    p2_buffer = res1.wells()[9]
    chtr = res1.wells()[11]
    mm2 = [well for well in res2.wells()[:2] for i in range(6)]

    # Helper Functions
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
    ez_disruptor_plate_wells = ez_disruptor_plate.rows()[0]
    microtubes_96_well_racked_wells = microtubes_96_well_racked.rows()[0]
    mag_plate_wells = mag_plate.rows()[0]

    # Protocol Steps

    # Initial Steps 1-2
    ctx.pause('''Centrifuge E-Z 96 Disruptor Plate C Plus to remove ceramic beads. Then, add samples to the plate.''')

    # Add Master Mix 1 + Lysozyme + Incubate at 37C for 20 minutes (Step 3)
    m300.transfer(527, mm1, ez_disruptor_plate_wells, new_tip='once') # Change Tips?
    m300.transfer(20, lysozyme, ez_disruptor_plate_wells, new_tip='once') # Change Tips?
    temp_mod.set_temperature(37) # Does plate need to on an aluminum adapter?
    if temp_mod.status == 'holding at target':
        ctx.delay(minutes=20, msg='Incubating at 37C for 20 minutes')
    temp_mod.deactivate()

    # Pause (Steps 4-5)
    ctx.pause('''1. Seal plate with the caps. Vortex for 3-5 minutes.
                 2. Centrifuge at 500g for 10 seconds
                 3. Remove and Discard Caps from E-Z 96 Plate''')

    # Add 53uL DS Buffer (Steps 6-7)
    m300.transfer(20, ds_buffer, ez_disruptor_plate_wells, new_tip='once') # Change Tips?
    ctx.pause('''1. Seal plate with new caps for racked microtubes.
                 2. Vortex to mix thoroughly.''')

    # Incubate EZ 96 Plate on Temp Mod at 70C for 10 minutes (Step 8)
    for temp, delay in zip([70, 95], [10, 2]):
        temp_mod.set_temperature(temp)
        if temp_mod.status == 'holding at target':
            if temp == 70:
                ctx.delay(minutes=delay, msg='Incubating at 70C for 10 minutes. Briefly vortex the plate once during incubation.')
            else:
                ctx.delay(minutes=delay, msg='Performing second incubation at 95°C for 2 minutes.')

    # Centrifuge (Step 9)
    ctx.pause('Centrifuge at >2000g for 10 minutes at room temp.')

    # Transfer 200 uL of supernatant to 96-well racked microtubes (Step 10)
    ctx.comment(f'Transferring 200uL of supernatant to {microtubes_96_well_racked}')
    for source, dest in zip(ez_disruptor_plate_wells,
    microtubes_96_well_racked_wells):
        m300.pick_up_tip()
        supernatant_removal(200, source, dest, -1)
        m300.drop_tip()

    # Transfer P2 Buffer and cHTR Reagent (Step 11)
    ctx.pause('Add Prechilled P2 Buffer into reservoir')
    m300.transfer(67, p2_buffer, microtubes_96_well_racked_wells, new_tip='once')
    # cHTR is viscous
    m300.flow_rate.aspirate = 30
    m300.flow_rate.dispense = 30
    m300.transfer(100, chtr, microtubes_96_well_racked_wells, new_tip='once')
    # Reset Flow Rates
    reset_flow_rates()

    # Centrifuge (Step 12)
    ctx.pause('Centrifuge >2000g for 5 minutes')

    # Transfer supernatant to mag plate (Step 13)
    ctx.comment(f'Transferring 200uL of supernatant to {mag_plate}')
    for source, dest in zip(microtubes_96_well_racked_wells, mag_plate_wells):
        m300.pick_up_tip()
        supernatant_removal(200, source, dest, -1)
        m300.drop_tip()

    # Transfer Master Mix 2 to Mag Plate
    m300.transfer(150, mm2, mag_plate_wells, mix_after=(10, 100), new_tip='always')

    # Incubate at Room Temp for 10 Minutes while mixing
    now = datetime.now()
    # now_plus_10 = now + timedelta(minutes = 10)
    now_plus_10 = now + timedelta(seconds = 10)
    # Determine how many mixes can be done per column
    while datetime.now() < now_plus_10:
        for col in mag_plate_wells:
            pick_up(m300)
            m300.mix(3, 100, col)
            m300.return_tip()







    # print(ctx.loaded_labwares)
