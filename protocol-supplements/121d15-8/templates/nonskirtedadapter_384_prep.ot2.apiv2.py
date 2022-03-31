from opentrons import protocol_api
import threading
import contextlib
import os
import json
import math

INPUT_FILE = """Number of Transfers
23
TB_RCK pos,pos in TB_RCK,pos in 384Plate,VolumeFromTube
384Platebarcode,RunId
1,1,4
3,150,4
4,96,2
48,204,2
"""

COLUMN_MAP = """96-1,12
96-2,12
96-3,3
96-4,12"""


# metadata
metadata = {
    'protocolName': '384-well Prep',
    'author': 'Nick <ndiehl@opentrons.com>',
    'source': 'Custom Protocol',
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
    sample_column_numbers = [
        int(line.split(',')[1]) for line in COLUMN_MAP.splitlines()]

    # load labware and pipettes
    tipracks_m = [
        ctx.load_labware('opentrons_96_tiprack_20ul', slot)
        for slot in ['6', '9', '8']]
    tipracks_s = [
        ctx.load_labware('opentrons_96_tiprack_20ul', slot)
        for slot in ['11']]
    src_plates = [
        ctx.load_labware('eurofinsadapter_96_wellplate_200ul', slot,
                         f'src plate {i+1}')
        for i, slot in enumerate(['1', '4', '7', '10'])]
    dest_plate = ctx.load_labware('appliedbiosystemsmicroampcustom_384_wellplate_40ul', '3')
    primer_racks = [
        ctx.load_labware('opentrons_24_tuberack_generic_2ml_screwcap', slot,
                         f'primer rack {i+1}')
        for i, slot in enumerate(['2', '5'])]

    # pipette
    m20 = ctx.load_instrument('p20_multi_gen2', 'right', tip_racks=tipracks_m)
    p20 = ctx.load_instrument('p20_single_gen2', 'left', tip_racks=tipracks_s)

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

    src_sets = [
        plate.rows()[0][:num_cols]
        for num_cols, plate in zip(sample_column_numbers,
                                   src_plates[:len(sample_column_numbers)])]
    pcr_dests_quadrants = [
        row[i::2] for row in dest_plate.rows()[:2] for i in range(2)]

    # pre-add primers
    data = [
        [val.strip() for val in line.split(',')]
        for line in INPUT_FILE.splitlines()
        if line and line.split(',')][4:]

    tubes_ordered = [
        tube for rack in primer_racks for tube in rack.wells()]

    last_accessed_primer = None
    for line in data:
        primer = tubes_ordered[int(line[0])-1]
        dest = dest_plate.wells()[int(line[1])-1]
        primer_vol = float(line[2])

        if not p20 == last_accessed_primer:
            if p20.has_tip:
                p20.drop_tip()
            _pick_up(p20)
        p20.aspirate(5, primer.top())
        p20.aspirate(primer_vol, primer)
        p20.dispense(p20.current_volume, dest.bottom(0.5))
        p20.blow_out()
    p20.drop_tip()

    # add samples
    sample_volume = 2
    for src_set, dest_quadrant in zip(src_sets, pcr_dests_quadrants):
        for s, d in zip(src_set, dest_quadrant[:len(src_set)]):
            _pick_up(m20)
            m20.aspirate(5, s.top())
            m20.aspirate(sample_volume, s)
            m20.dispense(m20.current_volume, d.bottom(1))
            m20.blow_out()
            m20.drop_tip()

    # track final used tip
    if not ctx.is_simulating():
        if not os.path.isdir(folder_path):
            os.mkdir(folder_path)
        tip_data = {pip.name: tip_log[pip]['count'] for pip in tip_log}
        with open(tip_file_path, 'w') as outfile:
            json.dump(tip_data, outfile)
