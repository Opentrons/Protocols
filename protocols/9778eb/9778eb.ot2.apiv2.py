"""OPENTRONS."""
from opentrons.types import Point
import json
import os
import math
import threading
from time import sleep
from opentrons import types


metadata = {
    'protocolName': 'Mag-Bind® Blood & Tissue DNA HDQ 96 Kit',
    'author': 'Opentrons <protocols@opentrons.com>',
    'apiLevel': '2.11'
}


"""
Here is where you can modify the magnetic module engage height:
"""
TEST_MODE = True


# Definitions for deck light flashing
class CancellationToken:
    """FLASH SETUP."""

    def __init__(self):
        """FLASH SETUP."""
        self.is_continued = False

    def set_true(self):
        """FLASH SETUP."""
        self.is_continued = True

    def set_false(self):
        """FLASH SETUP."""
        self.is_continued = False


def turn_on_blinking_notification(hardware, pause):
    """FLASH SETUP."""
    while pause.is_continued:
        hardware.set_lights(rails=True)
        sleep(1)
        hardware.set_lights(rails=False)
        sleep(1)


def create_thread(ctx, cancel_token):
    """FLASH SETUP."""
    t1 = threading.Thread(target=turn_on_blinking_notification,
                          args=(ctx._hw_manager.hardware, cancel_token))
    t1.start()
    return t1


# Start protocol
def run(ctx):
    """PROTOCOL."""
    # Setup for flashing lights notification to empty trash
    cancellationToken = CancellationToken()

    # [num_samples, deepwell_type, res_type, starting_vol, binding_buffer_vol,
    #  wash1_vol, wash2_vol, wash3_vol, elution_vol, mix_reps, settling_time,
    #  park_tips, tip_track, flash, p300_mount] = get_values(  # noqa: F821
    #     'num_samples', 'deepwell_type', 'res_type', 'starting_vol',
    #     'binding_buffer_vol', 'wash1_vol', 'wash2_vol', 'wash3_vol',
    #     'elution_vol', 'mix_reps', 'settling_time', 'park_tips', 'tip_track',
    #     'flash', 'p300_mount')

    num_samples = 8
    deepwell_type = 'nest_96_wellplate_2ml_deep'
    res_type = 'nest_12_reservoir_15ml'
    starting_vol = 400
    binding_buffer_vol = 370
    wash1_vol = 600
    wash2_vol = 500
    wash3_vol = 500
    elution_vol = 50
    mix_reps = 15
    settling_time = 7
    park_tips = False
    tip_track = False
    flash = True
    p300_mount = 'left'

    sample_vol = 560
    bead_delay_time = 7
    supernatant_headspeed_modulator = 10
    num_trans_super_1 = math.ceil((sample_vol+420)/180)
    num_trans_super_2 = math.ceil(wash1_vol/150)

    """
    Here is where you can change the locations of your labware and modules
    (note that this is the recommended configuration)
    """
    magdeck = ctx.load_module('magnetic module gen2', '7')
    magdeck.disengage()
    magplate = magdeck.load_labware('nest_96_wellplate_2ml_deep',
                                    'deepwell plate')
#    tempdeck = ctx.load_module('Temperature Module Gen2', '1')
#   elutionplate will be random plate from Sanofi on Al block
    elutionplate = ctx.load_labware(
                'opentrons_96_aluminumblock_nest_wellplate_100ul',
                '3')
    waste = ctx.load_labware('nest_1_reservoir_195ml', '4',
                             'Liquid Waste').wells()[0].top()
    res2 = ctx.load_labware(res_type, '2', 'reagent reservoir 2')
    res1 = ctx.load_labware(res_type, '5', 'reagent reservoir 1')
    num_cols = math.ceil(num_samples/8)
    tips300 = [ctx.load_labware('opentrons_96_filtertiprack_200ul', slot,
                                '200µl filtertiprack')
               for slot in ['1', '6', '9', '8', '10', '11']]

    parking_spots = [column for column in tips300[0].rows()[0][:num_cols]]

    # load P300M pipette
    m300 = ctx.load_instrument(
        'p300_multi_gen2', p300_mount, tip_racks=tips300)

    """
    Here is where you can define the locations of your reagents.
    """
    binding_buffer = res1.wells()[:4]
    elution_solution = res2.wells()[-1]
    # VHB, first time
    wash1 = res1.wells()[4:8]
    wash2 = res1.wells()[8:]  # VHB second time
    wash3 = res2.wells()[:4]  # SPM wash
    wash4 = res2.wells()[4:8]  # NFW wash

    mag_samples_m = magplate.rows()[0][:num_cols]
    elution_samples_m = elutionplate.rows()[0][:num_cols]

#    magdeck.disengage()  # just in case
#    tempdeck.set_temperature(4)

    m300.flow_rate.aspirate = 150
    m300.flow_rate.dispense = 300
    m300.flow_rate.blow_out = 300

    def bead_mixing(well, pip, mvol, reps=10):
        """bead_mixing."""
        """
        'bead_mixing' will mix liquid that contains beads. This will be done by
        aspirating from the middle of the well and dispensing from the bottom to
        mix the beads with the other liquids as much as possible. Aspiration &
        dispensing will also be reversed to ensure proper mixing.
        param well: The current well that the mixing will occur in.
        param pip: The pipet that is currently attached/ being used.
        param mvol: The volume that is transferred before the mixing steps.
        param reps: The number of mix repetitions that should occur. Note~
        During each mix rep, there are 2 cycles of aspirating from bottom,
        dispensing at the top and 2 cycles of aspirating from middle,
        dispensing at the bottom
        """
        vol = mvol * .9

        pip.move_to(well.center())
        pip.flow_rate.aspirate = 200
        pip.flow_rate.dispense = 300
        for _ in range(reps):
            pip.aspirate(vol, well.bottom(1))
            pip.dispense(vol, well.bottom(5))
        pip.flow_rate.aspirate = 150
        pip.flow_rate.aspirate = 300

    # Begin Protocol
    # pre-mix bead/binding buffer mix

    # add binding buffer/bead mix
    m300.flow_rate.dispense = 60
    for i, dest in enumerate(mag_samples_m):
        m300.pick_up_tip()
        if i % 4 == 0:
            bead_mixing(binding_buffer[i//4], m300, 150, reps=20)
        for _ in range(3):
            if _ == 0:
                m300.aspirate(40, binding_buffer[i//4].top())
            m300.aspirate(140, binding_buffer[i//4])
            m300.dispense(180, dest.top(-2))
            m300.aspirate(40, dest.top(-2))
            m300.move_to(dest.top(2))
        m300.drop_tip()
    m300.flow_rate.dispense = 96
    # Mix 30 seconds, move to next sample 30 seconds mix
    for dest in mag_samples_m:
        m300.pick_up_tip()
        bead_mixing(dest, m300, 200, reps=10)
        # for _ in range(8):
        #     m300.aspirate(200, dest)
        #     m300.dispense(200, dest.top(-5))
        m300.drop_tip(home_after=False)

    # Mag module engage
    magdeck.engage()
    if TEST_MODE:
        ctx.delay(seconds=bead_delay_time)
    else:
        ctx.delay(minutes=bead_delay_time)

    # discard supernatant
    ctx.max_speeds['Z'] = 400
    ctx.max_speeds['A'] = 400
    m300.flow_rate.aspirate /= 5
    for i, (source, park_loc) in enumerate(zip(mag_samples_m, parking_spots)):
        side = -1 if i % 2 == 0 else 1
        m300.pick_up_tip()
        m300.move_to(source.top())
        for _ in range(num_trans_super_1):
            ctx.max_speeds['Z'] /= supernatant_headspeed_modulator
            ctx.max_speeds['A'] /= supernatant_headspeed_modulator
            if _ == 0:
                m300.aspirate(10, source.top())
            m300.aspirate(
                180, source.bottom().move(types.Point(x=side,
                                                      y=0, z=0.2)))
            m300.move_to(source.top())
            m300.air_gap(10)
            ctx.max_speeds['Z'] *= supernatant_headspeed_modulator
            ctx.max_speeds['A'] *= supernatant_headspeed_modulator
            m300.dispense(m300.current_volume, waste)
            m300.aspirate(10, waste)  # waste defaults to waste.top()
        m300.drop_tip(park_loc)
    m300.flow_rate.aspirate *= 5
    magdeck.disengage()

    # Add 600uL VHB Buffer, mix well to resuspend beads
    for i, dest in enumerate(mag_samples_m):
        m300.pick_up_tip()
        for _ in range(4):
            if _ == 0:
                m300.aspirate(20, wash1[i//3])
            m300.aspirate(150, wash1[i//3])
            m300.dispense(m300.current_volume, dest.top(-2))
            m300.aspirate(20, dest.top())
        bead_mixing(dest, m300, 200, reps=5)
        m300.drop_tip()

    # engage mag module
    magdeck.engage()
    if TEST_MODE:
        ctx.delay(seconds=bead_delay_time)
    else:
        ctx.delay(minutes=bead_delay_time)

    # discard supernatant
    m300.flow_rate.aspirate /= 5
    for i, (source, park_loc) in enumerate(zip(mag_samples_m, parking_spots)):
        side = -1 if i % 2 == 0 else 1
        m300.pick_up_tip(park_loc)
        m300.move_to(source.top())
        for _ in range(num_trans_super_2):
            ctx.max_speeds['Z'] /= supernatant_headspeed_modulator
            ctx.max_speeds['A'] /= supernatant_headspeed_modulator
            if _ == 0:
                m300.aspirate(20, source.top())
            m300.aspirate(
                150, source.bottom().move(types.Point(x=side,
                                                      y=0, z=0.2)))
            m300.move_to(source.top())
            m300.air_gap(20)
            ctx.max_speeds['Z'] *= supernatant_headspeed_modulator
            ctx.max_speeds['A'] *= supernatant_headspeed_modulator
            m300.dispense(m300.current_volume, waste)
            m300.aspirate(20, waste)
        m300.drop_tip(park_loc)
    m300.flow_rate.aspirate *= 5
    magdeck.disengage()

    # Wash 2, same as above

    # Add 600uL VHB Buffer, mix well to resuspend beads
    for i, dest in enumerate(mag_samples_m):
        m300.pick_up_tip()
        for _ in range(4):
            if _ == 0:
                m300.aspirate(20, wash2[i//3])
            m300.aspirate(150, wash2[i//3])
            m300.dispense(m300.current_volume, dest.top(-2))
            m300.aspirate(20, dest.top())
        bead_mixing(dest, m300, 200, reps=10)
        m300.drop_tip()

    # engage mag module
    magdeck.engage()
    if TEST_MODE:
        ctx.delay(seconds=bead_delay_time)
    else:
        ctx.delay(minutes=bead_delay_time)

    # discard supernatant
    m300.flow_rate.aspirate /= 5
    for i, (source, park_loc) in enumerate(zip(mag_samples_m, parking_spots)):
        side = -1 if i % 2 == 0 else 1
        m300.pick_up_tip(park_loc)
        m300.move_to(source.top())
        for _ in range(num_trans_super_2):
            ctx.max_speeds['Z'] /= supernatant_headspeed_modulator
            ctx.max_speeds['A'] /= supernatant_headspeed_modulator
            if _ == 0:
                m300.aspirate(20, source.top())
            m300.aspirate(
                150, source.bottom().move(types.Point(x=side,
                                                      y=0, z=0.2)))
            m300.move_to(source.top())
            m300.air_gap(20)
            ctx.max_speeds['Z'] *= supernatant_headspeed_modulator
            ctx.max_speeds['A'] *= supernatant_headspeed_modulator
            m300.dispense(m300.current_volume, waste)
            m300.aspirate(20, waste)
    m300.flow_rate.aspirate *= 5
    m300.drop_tip(park_loc)
    magdeck.disengage()

    # SPM Buffer Wash
    for i, dest in enumerate(mag_samples_m):
        m300.pick_up_tip()
        for _ in range(4):
            if _ == 0:
                m300.aspirate(20, wash3[i//3].top())
            m300.aspirate(150, wash3[i//3])
            m300.dispense(m300.current_volume, dest.top(-2))
            m300.aspirate(20, dest.top())
        bead_mixing(dest, m300, 200, reps=5)
        m300.drop_tip()

    # engage mag module
    magdeck.engage()
    if TEST_MODE:
        ctx.delay(seconds=bead_delay_time)
    else:
        ctx.delay(minutes=bead_delay_time)

    # discard supernatant, N.B. Trash tips here
    m300.flow_rate.aspirate /= 5
    for i, (source, park_loc) in enumerate(zip(mag_samples_m, parking_spots)):
        side = -1 if i % 2 == 0 else 1
        m300.pick_up_tip(park_loc)
        m300.move_to(source.top())
        for _ in range(num_trans_super_2):
            ctx.max_speeds['Z'] /= supernatant_headspeed_modulator
            ctx.max_speeds['A'] /= supernatant_headspeed_modulator
            if _ == 0:
                m300.aspirate(20, source.top())
            m300.aspirate(
                150, source.bottom().move(types.Point(x=side,
                                                      y=0, z=0.2)))
            m300.move_to(source.top())
            m300.air_gap(20)
            ctx.max_speeds['Z'] *= supernatant_headspeed_modulator
            ctx.max_speeds['A'] *= supernatant_headspeed_modulator
            m300.dispense(m300.current_volume, waste)
            m300.aspirate(20, waste)
        m300.drop_tip()
    m300.flow_rate.aspirate *= 5

    # NFW wash to remove EtOH twice
    for i, dest in enumerate(mag_samples_m):
        side = -1 if i % 2 == 0 else 1
        m300.pick_up_tip()
        magdeck.engage()
        for _ in range(2):
            m300.aspirate(200, wash4[i//3])
            m300.dispense(200, dest.top(-2))
            m300.aspirate(20, dest.top())
            m300.dispense(20, wash4[i//3])
        ctx.delay(seconds=20)
        for _ in range(2):
            m300.aspirate(200, dest.bottom().move(types.Point(x=side,
                                                  y=0, z=0.2)))
            m300.dispense(200, waste)
            m300.aspirate(20, waste)
            m300.dispense(20, dest.top())
        magdeck.disengage()
        m300.aspirate(20, dest.top())
        m300.drop_tip()
        m300.pick_up_tip()
        m300.aspirate(50, elution_solution)
        m300.dispense(50, dest)
        m300.mix(4, 50, dest)
        m300.drop_tip()

    # N.B. previous approach to NFW wash
    """for _ in range(2):
        if not m300.has_tip:
            m300.pick_up_tip()
        for i, dest in enumerate(mag_samples_m):
            src = wash3[i//6] if _ == 0 else wash3[(i//6)+2]
            m300.aspirate(200, src)
            m300.dispense(200, dest.top(-2))
        m300.drop_tip()

        for i, (source, park_loc) in enumerate(zip(mag_samples_m, parking_spots)):
            side = -1 if i % 2 == 0 else 1
            if not m300.has_tip:
                m300.pick_up_tip(park_loc) if _ == 1 else m300.pick_up_tip()
            m300.move_to(source.top())
            ctx.max_speeds['Z'] /= supernatant_headspeed_modulator
            ctx.max_speeds['A'] /= supernatant_headspeed_modulator
            m300.aspirate(
                200, source.bottom().move(types.Point(x=side,
                                                      y=0, z=0.2)))
            m300.move_to(source.top())
            ctx.max_speeds['Z'] *= supernatant_headspeed_modulator
            ctx.max_speeds['A'] *= supernatant_headspeed_modulator
            m300.dispense(m300.current_volume, waste)
            m300.drop_tip(park_loc, home_after=False)

    magdeck.disengage()

    # Elution buffer addition
    for dest in mag_samples_m:
        m300.pick_up_tip()
        m300.aspirate(50, elution_solution)
        m300.dispense(50, dest)
        bead_mixing(dest, m300, 50, reps=10)
        m300.drop_tip()
    magdeck.engage()"""

    if TEST_MODE:
        ctx.delay(seconds=bead_delay_time)
    else:
        ctx.delay(minutes=bead_delay_time)

    # Transfer super to 96 well plate
    for i, (source, dest) in enumerate(zip(mag_samples_m, elution_samples_m)):
        side = -1 if i % 2 == 0 else 1
        m300.pick_up_tip()
        m300.move_to(source.top())
        ctx.max_speeds['Z'] /= supernatant_headspeed_modulator
        ctx.max_speeds['A'] /= supernatant_headspeed_modulator
        m300.aspirate(
            50, source.bottom().move(types.Point(x=side,
                                                 y=0, z=0.2)))
        m300.move_to(source.top())
        m300.aspirate(20, source.top())
        ctx.max_speeds['Z'] *= supernatant_headspeed_modulator
        ctx.max_speeds['A'] *= supernatant_headspeed_modulator
        m300.dispense(20, dest.top())
        m300.dispense(m300.current_volume, dest)
        m300.drop_tip()

#     folder_path = '/data/B'
#     tip_file_path = folder_path + '/tip_log.json'
#     tip_log = {'count': {}}
#     if tip_track and not ctx.is_simulating():
#         if os.path.isfile(tip_file_path):
#             with open(tip_file_path) as json_file:
#                 data = json.load(json_file)
#                 if 'tips300' in data:
#                     tip_log['count'][m300] = data['tips300']
#                 else:
#                     tip_log['count'][m300] = 0
#         else:
#             tip_log['count'][m300] = 0
#     else:
#         tip_log['count'] = {m300: 0}
#
#     tip_log['tips'] = {
#         m300: [tip for rack in tips300 for tip in rack.rows()[0]]}
#     tip_log['max'] = {m300: len(tip_log['tips'][m300])}
#
#     def _pick_up(pip, loc=None):
#         nonlocal tip_log
#         if tip_log['count'][pip] == tip_log['max'][pip] and not loc:
#             ctx.pause('Replace ' + str(pip.max_volume) + 'µl tipracks before \
# resuming.')
#             pip.reset_tipracks()
#             tip_log['count'][pip] = 0
#         if loc:
#             pip.pick_up_tip(loc)
#         else:
#             pip.pick_up_tip(tip_log['tips'][pip][tip_log['count'][pip]])
#             tip_log['count'][pip] += 1
#
#     switch = True
#     drop_count = 0
#     # number of tips trash will accommodate before prompting user to empty
#     drop_threshold = 120
#
#     def _drop(pip):
#         nonlocal switch
#         nonlocal drop_count
#         side = 30 if switch else -18
#         drop_loc = ctx.loaded_labwares[12].wells()[0].top().move(
#             Point(x=side))
#         pip.drop_tip(drop_loc)
#         switch = not switch
#         if pip.type == 'multi':
#             drop_count += 8
#         else:
#             drop_count += 1
#         if drop_count >= drop_threshold:
#             # Setup for flashing lights notification to empty trash
#             if flash:
#                 if not ctx._hw_manager.hardware.is_simulator:
#                     cancellationToken.set_true()
#                 thread = create_thread(ctx, cancellationToken)
#             m300.home()
#             ctx.pause('Please empty tips from waste before resuming.')
#             ctx.home()  # home before continuing with protocol
#             if flash:
#                 cancellationToken.set_false()  # stop light flashing after home
#                 thread.join()
#             drop_count = 0
#
#     waste_vol = 0
#     waste_threshold = 185000
#
#     def remove_supernatant(vol, park=False):
#         """REMOVE SUPER."""
#         """
#         `remove_supernatant` will transfer supernatant from the deepwell
#         extraction plate to the liquid waste reservoir.
#         :param vol (float): The amount of volume to aspirate from all deepwell
#                             sample wells and dispense in the liquid waste.
#         :param park (boolean): Whether to pick up sample-corresponding tips
#                                in the 'parking rack' or to pick up new tips.
#         """
#
#         def _waste_track(vol):
#             nonlocal waste_vol
#             if waste_vol + vol >= waste_threshold:
#                 # Setup for flashing lights notification to empty liquid waste
#                 if flash:
#                     if not ctx._hw_manager.hardware.is_simulator:
#                         cancellationToken.set_true()
#                     thread = create_thread(ctx, cancellationToken)
#                 m300.home()
#                 ctx.pause('Please empty liquid waste (slot 11) before \
# resuming.')
#
#                 ctx.home()  # home before continuing with protocol
#                 if flash:
#                     # stop light flashing after home
#                     cancellationToken.set_false()
#                     thread.join()
#
#                 waste_vol = 0
#             waste_vol += vol
#
#         m300.flow_rate.aspirate = 30
#         num_trans = math.ceil(vol/200)
#         vol_per_trans = vol/num_trans
#         for i, (m, spot) in enumerate(zip(mag_samples_m, parking_spots)):
#             if park:
#                 _pick_up(m300, spot)
#             else:
#                 _pick_up(m300)
#             side = -1 if i % 2 == 0 else 1
#             loc = m.bottom(0.5).move(Point(x=side*2))
#             for _ in range(num_trans):
#                 _waste_track(vol_per_trans)
#                 if m300.current_volume > 0:
#                     # void air gap if necessary
#                     m300.dispense(m300.current_volume, m.top())
#                 # WIP add slower descend into well, break out transfer function
#                 m300.move_to(m.center())
#                 m300.transfer(vol_per_trans, loc, waste, new_tip='never',
#                               air_gap=20)
#                 m300.blow_out(waste)
#                 m300.air_gap(20)
#             _drop(m300)
#         m300.flow_rate.aspirate = 150
#
#     def resuspend_pellet(well, pip, mvol, reps=5):
#         """PELLET SUSPEND."""
#         """
#         'resuspend_pellet' will forcefully dispense liquid over the pellet
#         after the magdeck engage in order to more thoroughly resuspend the
#         pellet. param well: The current well that the resuspension will occur
#         in. param pip: The pipet that is currently attached/ being used.
#         param mvol: The volume that is transferred before the mixing steps.
#         param reps: The number of mix repetitions that should occur. Note~
#         During each mix rep, there are 2 cycles of aspirating from center,
#         dispensing at the top and 2 cycles of aspirating from center,
#         dispensing at the bottom (5 mixes total)
#         """
#
#         rightLeft = int(str(well).split(' ')[0][1:]) % 2
#         """
#         'rightLeft' will determine which value to use in the list of 'top' and
#         'bottom' (below), based on the column of the 'well' used.
#         In the case that an Even column is used, the first value of 'top' and
#         'bottom' will be used, otherwise, the second value of each will be
#         used.
#         """
#         # N.B. waaaaay too much, change offsets
#         center = well.bottom().move(types.Point(x=0, y=0, z=1))
#         top = [
#             well.bottom().move(types.Point(x=-1, y=1, z=1)),
#             well.bottom().move(types.Point(x=1, y=1, z=1))
#         ]
#         bottom = [
#             well.bottom().move(types.Point(x=-1, y=-1, z=1)),
#             well.bottom().move(types.Point(x=1, y=-1, z=1))
#         ]
#
#         pip.flow_rate.dispense = 500
#         pip.flow_rate.aspirate = 150
#
#         mix_vol = 0.9 * mvol
#
#         pip.move_to(center)
#         for _ in range(reps):
#             for _ in range(2):
#                 pip.aspirate(mix_vol, center)
#                 pip.dispense(mix_vol, top[rightLeft])
#             for _ in range(2):
#                 pip.aspirate(mix_vol, center)
#                 pip.dispense(mix_vol, bottom[rightLeft])
#
#     def bind(vol, park=True):
#         """BIND."""
#         """
#         `bind` will perform magnetic bead binding on each sample in the
#         deepwell plate. Each channel of binding beads will be mixed before
#         transfer, and the samples will be mixed with the binding beads after
#         the transfer. The magnetic deck activates after the addition to all
#         samples, and the supernatant is removed after bead bining.
#         :param vol (float): The amount of volume to aspirate from the elution
#                             buffer source and dispense to each well containing
#                             beads.
#         :param park (boolean): Whether to save sample-corresponding tips
#                                between adding elution buffer and transferring
#                                supernatant to the final clean elutions PCR
#                                plate.
#         """
#         latest_chan = -1
#         for i, (well, spot) in enumerate(zip(mag_samples_m, parking_spots)):
#             if park:
#                 _pick_up(m300, spot)
#             else:
#                 _pick_up(m300)
#             num_trans = math.ceil(vol/200)
#             vol_per_trans = vol/num_trans
#             asp_per_chan = (0.95*res1.wells()[0].max_volume)//(vol_per_trans*8)
#             for t in range(num_trans):
#                 chan_ind = int((i*num_trans + t)//asp_per_chan)
#                 source = binding_buffer[chan_ind]
#                 if m300.current_volume > 0:
#                     # void air gap if necessary
#                     m300.dispense(m300.current_volume, source.top())
#                 if chan_ind > latest_chan:  # mix if accessing new channel
#                     for _ in range(5):
#                         m300.aspirate(180, source.bottom(0.5))
#                         m300.dispense(180, source.bottom(5))
#                     latest_chan = chan_ind
#                 m300.transfer(vol_per_trans, source, well.top(), air_gap=20,
#                               new_tip='never')
#                 if t < num_trans - 1:
#                     m300.air_gap(20)
#             m300.mix(5, 200, well)
#
#             m300.blow_out(well.top(-2))
#             m300.air_gap(20)
#             if park:
#                 m300.drop_tip(spot)
#             else:
#                 _drop(m300)
#         if TEST_MODE:
#             ctx.delay(seconds=3, msg='Bind off-deck on a heater/shaker')
#             ctx.delay(seconds=settling_time, msg='Incubating on MagDeck for \
#             ' + str(settling_time) + ' minutes.')
#         else:
#             ctx.delay(minutes=10, msg='Bind off-deck on a heater/shaker')
#             magdeck.engage()
#             ctx.delay(minutes=settling_time, msg='Incubating on MagDeck for \
#             ' + str(settling_time) + ' minutes.')
#
#         # remove initial supernatant
#         remove_supernatant(vol+starting_vol, park=park)
#
#     def wash(vol, source, mix_reps=15, park=True, resuspend=True):
#         """WASH."""
#         """
#         `wash` will perform bead washing for the extraction protocol.
#         :param vol (float): The amount of volume to aspirate from each
#                             source and dispense to each well containing beads.
#         :param source (List[Well]): A list of wells from where liquid will be
#                                     aspirated. If the length of the source list
#                                     > 1, `wash` automatically calculates
#                                     the index of the source that should be
#                                     accessed.
#         :param mix_reps (int): The number of repititions to mix the beads with
#                                specified wash buffer (ignored if resuspend is
#                                False).
#         :param park (boolean): Whether to save sample-corresponding tips
#                                between adding wash buffer and removing
#                                supernatant.
#         :param resuspend (boolean): Whether to resuspend beads in wash buffer.
#         """
#
#         if resuspend and magdeck.status == 'engaged':
#             magdeck.disengage()
#
#         num_trans = math.ceil(vol/200)
#         vol_per_trans = vol/num_trans
#         for i, (m, spot) in enumerate(zip(mag_samples_m, parking_spots)):
#             _pick_up(m300)
#             # side = 1 if i % 2 == 0 else -1
#             # loc = m.bottom(0.5).move(Point(x=side*2))
#             src = source[i//(12//len(source))]
#             for n in range(num_trans):
#                 if m300.current_volume > 0:
#                     m300.dispense(m300.current_volume, src.top())
#                 m300.transfer(vol_per_trans, src, m.top(), air_gap=20,
#                               new_tip='never')
#                 if n < num_trans - 1:  # only air_gap if going back to source
#                     m300.air_gap(20)
#             if resuspend:
#                 # m300.mix(mix_reps, 150, loc)
#                 resuspend_pellet(m, m300, 180)
#
#             m300.blow_out(m.top())
#             m300.air_gap(20)
#             if park:
#                 m300.drop_tip(spot)
#             else:
#                 _drop(m300)
#
#         if magdeck.status == 'disengaged':
#             magdeck.engage()
#
#         if TEST_MODE:
#             ctx.delay(seconds=settling_time, msg='Incubating on MagDeck for \
#             ' + str(settling_time) + ' minutes.')
#         else:
#             ctx.delay(minutes=settling_time, msg='Incubating on MagDeck for \
#             ' + str(settling_time) + ' minutes.')
#
#         remove_supernatant(vol, park=park)
#
#     def elute(vol, park=True):
#         """ELUTE."""
#         """
#         `elute` will perform elution from the deepwell extraciton plate to the
#         final clean elutions PCR plate to complete the extraction protocol.
#         :param vol (float): The amount of volume to aspirate from the elution
#                             buffer source and dispense to each well containing
#                             beads.
#         :param park (boolean): Whether to save sample-corresponding tips
#                                between adding elution buffer and transferring
#                                supernatant to the final clean elutions PCR
#                                plate.
#         """
#
#         # resuspend beads in elution
#         if magdeck.status == 'enagaged':
#             magdeck.disengage()
#         for i, (m, spot) in enumerate(zip(mag_samples_m, parking_spots)):
#             _pick_up(m300)
#             side = 1 if i % 2 == 0 else -1
#             loc = m.bottom(0.5).move(Point(x=side*2))
#             m300.aspirate(vol, elution_solution)
#             m300.move_to(m.center())
#             m300.dispense(vol, loc)
#             m300.mix(mix_reps, 0.8*vol, loc)
#             m300.blow_out(m.bottom(5))
#             m300.air_gap(20)
#             if park:
#                 m300.drop_tip(spot)
#             else:
#                 _drop(m300)
#         if TEST_MODE:
#             ctx.delay(seconds=5, msg='Delay for 5 minutes for elution')
#             magdeck.engage()
#             ctx.delay(seconds=settling_time, msg='Incubating on MagDeck for \
#             ' + str(settling_time) + ' minutes.')
#         else:
#             ctx.delay(minutes=5, msg='Delay for 5 minutes for elution')
#             magdeck.engage()
#             ctx.delay(minutes=settling_time, msg='Incubating on MagDeck for \
#             ' + str(settling_time) + ' minutes.')
#
#         for i, (m, e, spot) in enumerate(
#                 zip(mag_samples_m, elution_samples_m, parking_spots)):
#             if park:
#                 _pick_up(m300, spot)
#             else:
#                 _pick_up(m300)
#             side = -1 if i % 2 == 0 else 1
#             loc = m.bottom(0.5).move(Point(x=side*2))
#             m300.transfer(vol, loc, e.bottom(5), air_gap=20, new_tip='never')
#             m300.blow_out(e.top(-2))
#             m300.air_gap(20)
#             m300.drop_tip()
#
#     """
#     Here is where you can call the methods defined above to fit your specific
#     protocol. The normal sequence is:
#     """
#     bind(binding_buffer_vol, park=park_tips)
#     wash(wash1_vol, wash1, park=park_tips)
#     wash(wash2_vol, wash2, park=park_tips)
#     wash(wash3_vol, wash3, park=park_tips)
#     if TEST_MODE:
#         ctx.delay(seconds=5, msg='Incubate for 5 minutes to dry beads')
#         elute(elution_vol, park=park_tips)
#     else:
#         ctx.delay(minutes=5, msg='Incubate for 5 minutes to dry beads')
#         elute(elution_vol, park=park_tips)
#
#     # track final used tip
#     if tip_track and not ctx.is_simulating():
#         if not os.path.isdir(folder_path):
#             os.mkdir(folder_path)
#         data = {'tips300': tip_log['count'][m300]}
#         with open(tip_file_path, 'w') as outfile:
#             json.dump(data, outfile)
#     for c in ctx.commands():
#         print(c)
