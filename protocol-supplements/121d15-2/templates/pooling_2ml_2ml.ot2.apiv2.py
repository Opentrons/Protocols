from opentrons import protocol_api
import threading
import math
import os
import json

# metadata
metadata = {
    'protocolName': 'Pooling - 2ml Tuberack to 2ml Tuberack',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.11'
}


# Definitions for deck light flashing
@contextlib.contextmanager
def flashing_rail_lights(
    protocol: protocol_api.ProtocolContext, seconds_per_flash_cycle=1.0
):
    """Flash the rail lights on and off in the background.

    Source: https://github.com/Opentrons/opentrons/issues/7742

    Example usage:

        # While the robot is doing nothing for 2 minutes, flash lights quickly.
        with flashing_rail_lights(protocol, seconds_per_flash_cycle=0.25):
            protocol.delay(minutes=2)

    When the ``with`` block exits, the rail lights are restored to their
    original state.

    Exclusive control of the rail lights is assumed. For example, within the
    ``with`` block, you must not call `ProtocolContext.set_rail_lights`
    yourself, inspect `ProtocolContext.rail_lights_on`, or nest additional
    calls to `flashing_rail_lights`.
    """
    original_light_status = protocol.rail_lights_on

    stop_flashing_event = threading.Event()

    def background_loop():
        while True:
            protocol.set_rail_lights(not protocol.rail_lights_on)
            # Wait until it's time to toggle the lights for the next flash or
            # we're told to stop flashing entirely, whichever comes first.
            got_stop_flashing_event = stop_flashing_event.wait(
                timeout=seconds_per_flash_cycle/2
            )
            if got_stop_flashing_event:
                break

    background_thread = threading.Thread(
        target=background_loop, name="Background thread for flashing rail \
lights"
    )

    try:
        if not protocol.is_simulating():
            background_thread.start()
        yield

    finally:
        # The ``with`` block might be exiting normally, or it might be exiting
        # because something inside it raised an exception.
        #
        # This accounts for user-issued cancelations because currently
        # (2021-05-04), the Python Protocol API happens to implement user-
        # issued cancellations by raising an exception from internal API code.
        if not protocol.is_simulating():
            stop_flashing_event.set()
            background_thread.join()

        # This is questionable: it may issue a command to the API while the API
        # is in an inconsistent state after raising an exception.
        protocol.set_rail_lights(original_light_status)


def run(ctx):

    tip_track = True
    p300_mount = 'left'
    flash = True

    # load labware
    rack = ctx.load_labware('eurofins_96x2ml_tuberack', '2', 'tuberack')
    tips300 = [
        ctx.load_labware('opentrons_96_tiprack_300ul', slot)
        for slot in ['11']]

    # pipette
    p300 = ctx.load_instrument('p300_single_gen2', p300_mount,
                               tip_racks=tips300)

    tip_log = {val: {} for val in ctx.loaded_instruments.values()}

    folder_path = '/data/tip_track'
    tip_file_path = folder_path + '/tip_log.json'
    if tip_track and not ctx.is_simulating():
        if os.path.isfile(tip_file_path):
            with open(tip_file_path) as json_file:
                tip_data = json.load(json_file)
                for pip in tip_log:
                    if pip.name in tip_data:
                        tip_log[pip]['count'] = tip_data[pip.name]
                    else:
                        tip_log[pip]['count'] = 0
        else:
            for pip in tip_log:
                tip_log[pip]['count'] = 0
    else:
        for pip in tip_log:
            tip_log[pip]['count'] = 0

    for pip in tip_log:
        if pip.type == 'multi':
            tip_log[pip]['tips'] = [tip for rack in pip.tip_racks
                                    for tip in rack.rows()[0]]
        else:
            tip_log[pip]['tips'] = [tip for rack in pip.tip_racks
                                    for tip in rack.wells()]
        tip_log[pip]['max'] = len(tip_log[pip]['tips'])

    def _pick_up(pip, loc=None):
        if tip_log[pip]['count'] == tip_log[pip]['max'] and not loc:
            if flash:
                if not ctx._hw_manager.hardware.is_simulator:
                    with flashing_rail_lights(ctx, seconds_per_flash_cycle=1):
                        ctx.pause('Replace ' + str(pip.max_volume) + 'µl \
tipracks before resuming.')
            pip.reset_tipracks()
            tip_log[pip]['count'] = 0
        if loc:
            pip.pick_up_tip(loc)
        else:
            pip.pick_up_tip(tip_log[pip]['tips'][tip_log[pip]['count']])
            tip_log[pip]['count'] += 1

    # check barcode scans (tube, plate)
    tuberack1_bar, tuberack2_bar = input_file.splitlines()[3].split(',')[:2]
    if not tuberack1_scan[:len(tuberack1_scan)-4] == tuberack1_bar.strip():
        raise Exception(f'Tuberack 1 scans do not match ({tuberack1_bar}, \
{tuberack1_scan})')
    if not tuberack2_scan[:len(tuberack2_scan)-4] == tuberack2_bar.strip():
        raise Exception(f'Tuberack 2 scans do not match ({tuberack2_bar}, \
{tuberack2_bar})')

    # parse
    data = [
        [val.strip() for val in line.split(',')]
        for line in input_file.splitlines()[4:]
        if line and line.split(',')[0].strip()]

    tubes1_ordered = [
        well for col in rack.columns()
        for well in col[:8]]

    tubes2_ordered = [
        well for col in rack.columns()
        for well in col[8:]]

    prev_dest = None
    for line in data:
        tube1 = tubes1_ordered[int(line[0])-1]
        tube2 = tubes2_ordered[int(line[1])-1]
        if len(line) >= 3 and line[2]:
            transfer_vol = float(line[2])
        else:
            transfer_vol = default_transfer_vol

        # tip capacity 280 with 20 uL air gap
        reps = math.ceil(transfer_vol / 280)

        vol = transfer_vol / reps

        # transfer
        if tube2 != prev_dest:
            if p300.has_tip:
                p300.drop_tip()
            _pick_up(p300)

        for rep in range(reps):
            p300.move_to(tube1.top())
            p300.air_gap(20)
            p300.aspirate(vol, tube1.bottom(0.5))
            p300.dispense(vol+20, tube2.top(-5), rate=2)
            ctx.delay(seconds=1)
            p300.blow_out()

        prev_dest = tube2
    p300.drop_tip()

    # track final used tip
    if not ctx.is_simulating():
        if not os.path.isdir(folder_path):
            os.mkdir(folder_path)
        tip_data = {pip.name: tip_log[pip]['count'] for pip in tip_log}
        with open(tip_file_path, 'w') as outfile:
            json.dump(tip_data, outfile)
