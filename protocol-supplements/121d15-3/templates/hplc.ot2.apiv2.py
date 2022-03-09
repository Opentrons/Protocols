from opentrons import protocol_api
import math
import threading
import os
import json
import contextlib

# metadata
metadata = {
    'protocolName': 'HPLC Picking',
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
    flash = True

    # load labware
    rack = ctx.load_labware('eurofins_96x2ml_tuberack', '2', 'tuberack')
    tips300 = [ctx.load_labware('opentrons_96_tiprack_300ul', '11')]

    # pipette
    p300 = ctx.load_instrument('p300_single_gen2', 'left',
                               tip_racks=tips300)
    p300.flow_rate.dispense = 120

    tip_log = {val: {} for val in ctx.loaded_instruments.values()}

    folder_path = '/data/tip_track'
    tip_file_path = folder_path + '/tip_log.json'
    if tip_track and not ctx.is_simulating():
        if os.path.isfile(tip_file_path):
            with open(tip_file_path) as json_file:
                data = json.load(json_file)
                for pip in tip_log:
                    if pip.name in data:
                        tip_log[pip]['count'] = data[pip.name]
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

    # parse
    data = [
        line.split(',') for line in INPUT_FILE.splitlines()
        if line and line.split(',')[0].strip()]

    # determine plates in use
    plates_used = {key: False for key in range(4)}
    for i, line in enumerate(data):
        source_ind = int(line[0]) - 1
        plates_used[source_ind//96] = True

    if not plates_used[3]:
        plates = [
            ctx.load_labware('irishlifesciences_96_wellplate_2200ul', slot,
                             f'plate {i+1}')
            for i, slot in enumerate(['10', '7', '4'])]
        water = ctx.load_labware('test_1_reservoir_300000ul', '1').wells()[0]
    else:
        plates = [
            ctx.load_labware('irishlifesciences_96_wellplate_2200ul', slot,
                             f'plate {i+1}')
            for i, slot in enumerate(['10', '7', '4', '1'])]
        water = plates[-1].wells_by_name()['D6']

    # order
    wells_ordered = [
        well for plate in plates for row in plate.rows() for well in row]

    dest_vols = {}
    prev_dest = None
    for i, line in enumerate(data):
        source = wells_ordered[int(line[0]) - 1]
        dest = rack.wells_by_name()[line[1].upper()]
        if len(line) > 2 and line[2]:
            vol = round(float(line[2]))
        else:
            vol = DEFAULT_TRANSFER_VOL

        if dest != prev_dest:
            if p300.has_tip:
                p300.drop_tip()
            _pick_up(p300)

        # check for volumes slightly over 300ul from HPLC input files
        vol = 300 if 300 < vol < 305 else vol
        # effective tip capacity 280 with 20 uL air gap
        reps = math.ceil(vol / 300)

        v = vol / reps

        for rep in range(reps):
            p300.aspirate(v, source.bottom(0.5))
            p300.dispense(
             v+50, dest.top(-5), rate=2)
            ctx.delay(seconds=1)
            p300.blow_out()

        prev_dest = dest

        # track volumes for final adjustment
        if dest not in dest_vols:
            dest_vols[dest] = vol
        else:
            dest_vols[dest] += vol
    p300.drop_tip()

    # final adjustment with water up to 1500ul
    ctx.pause('Replace plate 4 in slot 1 with water reservoir. Resume once \
finished.')
    _pick_up(p300)
    for tube, vol in dest_vols.items():
        adjustment = 1500 - vol
        if adjustment > 0:
            # effective tip capacity 280 uL with 20 uL air gap
            reps = math.ceil(adjustment / 300)

            v = adjustment / reps

            for rep in range(reps):
                p300.aspirate(v, water.bottom(1))
                p300.dispense(
                 v+50, tube.top(-5), rate=2)
                ctx.delay(seconds=1)
                p300.blow_out()

    p300.drop_tip()

    # track final used tip
    if not ctx.is_simulating():
        if not os.path.isdir(folder_path):
            os.mkdir(folder_path)
        data = {pip.name: tip_log[pip]['count'] for pip in tip_log}
        with open(tip_file_path, 'w') as outfile:
            json.dump(data, outfile)
