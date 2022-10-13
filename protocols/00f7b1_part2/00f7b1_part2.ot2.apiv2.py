"""OPENTRONS."""
from opentrons import protocol_api
import math
import threading
from time import sleep
from opentrons import types

metadata = {
    'protocolName': 'NEBNext Ultra II Directional RNA Library Prep Kit for Illumina Part 2: RNA Isolation',
    'author': 'John C. Lynch <john.lynch@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.13'   # CHECK IF YOUR API LEVEL HERE IS UP TO DATE
                         # IN SECTION 5.2 OF THE APIV2 "VERSIONING"
}

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


def run(ctx: protocol_api.ProtocolContext):
    """PROTOCOLS."""
    [
     num_samples,
     m300_mount, flash
    ] = get_values(  # noqa: F821 (<--- DO NOT REMOVE!)
        "num_samples", "m300_mount", "flash")

    TEST_MODE = True
    bead_delay_time = 2
    wash_delay_time = 2
    supernatant_headspeed_modulator = 10
    mag_height = 3.5
    ctx.max_speeds['Z'] = 400
    ctx.max_speeds['A'] = 400
    # Setup for flashing lights notification to empty trash
    cancellationToken = CancellationToken()

    # define all custom variables above here with descriptions:
    num_columns = math.ceil(num_samples/8)
    if m300_mount == 'right':
        m20_mount = 'left'
    else:
        m20_mount = 'right'
    # load modules
    mag_deck = ctx.load_module('magnetic module gen2', '1')
    temp_deck = ctx.load_module('temperature module gen2', '3')
    print(num_columns)

    # load labware
    mag_plate = mag_deck.load_labware('thermofisher_96_wellplate_200ul')
    temp_plate = temp_deck.load_labware('opentrons_96_aluminumblock_generic_'
                                        'pcr_strip_200ul')
    dwp = ctx.load_labware('nest_96_wellplate_2ml_deep', '4')
    final_plate = ctx.load_labware('thermofisher_96_wellplate_200ul', '2')
    trash = ctx.load_labware('nest_1_reservoir_195ml', '8').wells()[0].top()
    # load tipracks

    tips300 = [ctx.load_labware('opentrons_96_filtertiprack_200ul', slot)
               for slot in ['7', '10']]
    tips20 = [ctx.load_labware('opentrons_96_filtertiprack_20ul', slot)
              for slot in ['11']]
    # load instrument

    m300 = ctx.load_instrument(
        'p300_multi_gen2', m300_mount, tip_racks=tips300)

    m20 = ctx.load_instrument('p20_multi_gen2', m20_mount, tip_racks=tips20)

    # pipette functions   # INCLUDE ANY BINDING TO CLASS

    def pick_up(pip):
        try:
            pip.pick_up_tip()
        except protocol_api.labware.OutOfTipsError:
            if flash:
                if not ctx._hw_manager.hardware.is_simulator:
                    cancellationToken.set_true()
                thread = create_thread(ctx, cancellationToken)
            pip.home()
            ctx.pause('\n\n~~~~~~~~~~~~~~PLEASE REPLACE TIPRACKS~~~~~~~~~~~~~~~\n')  # noqa: E501
            ctx.home()  # home before continuing with protocol
            if flash:
                cancellationToken.set_false()  # stop light flashing after home
                thread.join()
            ctx.set_rail_lights(True)
            pip.reset_tipracks()
            pick_up(pip)

    tips_dropped = 0

    def drop_tip(pip, home=True):
        nonlocal tips_dropped
        pip.drop_tip(home_after=home)
        if pip == m300:
            tips_dropped += 8
        else:
            tips_dropped += 1
        if tips_dropped == 288:
            if flash:
                if not ctx._hw_manager.hardware.is_simulator:
                    cancellationToken.set_true()
                thread = create_thread(ctx, cancellationToken)
            pip.home()
            ctx.pause('\n\n~~~~~~~~~~~~~~PLEASE EMPTY TRASH~~~~~~~~~~~~~~~\n')
            ctx.home()  # home before continuing with protocol
            if flash:
                cancellationToken.set_false()  # stop light flashing after home
                thread.join()
            ctx.set_rail_lights(True)
            tips_dropped = 0

    def bead_mixing(well, pip, mvol, reps=10):
        """bead_mixing."""
        """
        'bead_mixing' will mix liquid that contains beads. This will be done by
        aspirating from the middle of the well & dispensing from the bottom to
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
        for _ in range(reps):
            pip.aspirate(vol, well.bottom(1), rate=2)
            pip.dispense(vol, well.bottom(5), rate=2)
            pip.aspirate(vol, well.bottom(5), rate=2)
            pip.dispense(vol, well.bottom(1), rate=2)
    # reagents

    samples = mag_plate.rows()[0][:num_columns]
    beads = dwp.rows()[0][0]
    wash_1 = dwp.rows()[0][2]
    wash_2 = dwp.rows()[0][4]
    tris = dwp.rows()[0][6]
    wash_3 = dwp.rows()[0][8]
    strand_primer_mix = temp_plate.rows()[0][:num_columns]
    bead_wash = dwp.rows()[0][-1]
    final_dest = final_plate.rows()[0][:num_columns]

    # protocol
    ctx.comment('\n~~~~~~~~~~~~~~ADDING BEADS~~~~~~~~~~~~~~\n')
    pick_up(m300)
    bead_mixing(beads, m300, 200)
    for i, dest in enumerate(samples):
        if i > 0:
            pick_up(m300)
        m300.aspirate(50, beads, rate=0.5)
        ctx.delay(seconds=1.5)
        ctx.max_speeds['Z'] /= supernatant_headspeed_modulator
        ctx.max_speeds['A'] /= supernatant_headspeed_modulator
        m300.move_to(beads.top())
        ctx.max_speeds['Z'] *= supernatant_headspeed_modulator
        ctx.max_speeds['A'] *= supernatant_headspeed_modulator
        m300.dispense(50, dest, rate=0.5)
        bead_mixing(dest, m300, 100, reps=5)
        drop_tip(m300)

    if flash:
        if not ctx._hw_manager.hardware.is_simulator:
            cancellationToken.set_true()
        thread = create_thread(ctx, cancellationToken)
    m300.home()
    ctx.pause('\n\nMOVE PLATE IN SLOT 1 TO OFF-DECK THERMOCYCLER\n'
              'REFER TO 1.2.12 FOR SPECIFIC HEATING/COOLING CYCLE\n'
              'RETURN PLATE TO SLOT 1 WHEN FINISHED')
    ctx.home()  # home before continuing with protocol
    if flash:
        cancellationToken.set_false()  # stop light flashing after home
        thread.join()
    ctx.set_rail_lights(True)

    ctx.comment('\n~~~~~~~~~~~~~~MIXING~~~~~~~~~~~~~~\n')
    for dest in samples:
        pick_up(m300)
        bead_mixing(dest, m300, 100, reps=6)
        drop_tip(m300)
    if TEST_MODE:
        ctx.delay(seconds=5)
    else:
        ctx.delay(minutes=5)

    ctx.comment('\n~~~~~~~~~~~~~~ENGAGING MAGNET~~~~~~~~~~~~~~\n')
    mag_deck.engage(height_from_base=mag_height)
    if TEST_MODE:
        ctx.delay(seconds=bead_delay_time)
    else:
        ctx.delay(minutes=bead_delay_time)

    ctx.comment('\n~~~~~~~~~~~~~~REMOVING SUPERNATANT~~~~~~~~~~~~~~\n')
    for dest in samples:
        pick_up(m300)
        ctx.max_speeds['Z'] /= supernatant_headspeed_modulator
        ctx.max_speeds['A'] /= supernatant_headspeed_modulator
        m300.aspirate(100, dest.bottom().move(types.Point(x=-1, y=0, z=0)),
                      rate=0.5)
        ctx.delay(seconds=1)
        m300.move_to(dest.top())
        m300.aspirate(10, dest.top())
        ctx.max_speeds['Z'] *= supernatant_headspeed_modulator
        ctx.max_speeds['A'] *= supernatant_headspeed_modulator
        m300.dispense(m300.current_volume, trash)
        drop_tip(m300)

    ctx.comment('\n~~~~~~~~~~~~~WASHING BEADS TWICE WITH BUFFER~~~~~~~~~~~~\n')
    for wash in [wash_1, wash_2]:
        for dest in samples:
            pick_up(m300)
            m300.aspirate(200, wash)
            m300.dispense(200, dest)
            bead_mixing(dest, m300, 200, reps=6)
            drop_tip(m300)

        mag_deck.engage(height_from_base=mag_height)
        if TEST_MODE:
            ctx.delay(seconds=wash_delay_time)
        else:
            ctx.delay(minutes=wash_delay_time)
        for dest in samples:
            pick_up(m300)
            m300.move_to(dest.top())
            ctx.max_speeds['Z'] /= supernatant_headspeed_modulator
            ctx.max_speeds['A'] /= supernatant_headspeed_modulator
            m300.aspirate(200,
                          dest.bottom().move(types.Point(x=-1, y=0, z=0)),
                          rate=0.5)
            m300.move_to(dest.top())
            ctx.max_speeds['Z'] *= supernatant_headspeed_modulator
            ctx.max_speeds['A'] *= supernatant_headspeed_modulator
            m300.dispense(200, trash)
            drop_tip(m300)

    ctx.comment('\n~~~~~~~~~~~~~ADDING TRIS BUFFER~~~~~~~~~~~~\n')
    for dest in samples:
        pick_up(m300)
        m300.aspirate(50, tris)
        m300.dispense(50, dest)
        bead_mixing(dest, m300, 50, reps=6)
        drop_tip(m300)

    if flash:
        if not ctx._hw_manager.hardware.is_simulator:
            cancellationToken.set_true()
        thread = create_thread(ctx, cancellationToken)
    m300.home()
    ctx.pause('\n\nMOVE PLATE IN SLOT 1 TO OFF-DECK THERMOCYCLER\n'
              'REFER TO 1.2.24 FOR SPECIFIC HEATING/COOLING CYCLE\n'
              'RETURN PLATE TO SLOT 1 WHEN FINISHED\n\n')
    ctx.home()  # home before continuing with protocol
    if flash:
        cancellationToken.set_false()  # stop light flashing after home
        thread.join()
    ctx.set_rail_lights(True)

    ctx.comment('\n~~~~~~~~~~~~~ADDING BINDING BUFFER~~~~~~~~~~~~\n')
    for dest in samples:
        pick_up(m300)
        m300.aspirate(50, bead_wash)
        m300.dispense(50, dest)
        bead_mixing(dest, m300, 100, reps=6)
        drop_tip(m300)

    ctx.comment('\n~~~~~~~~~~~~~INCUBATING 5 MINUTES~~~~~~~~~~~~\n')
    if TEST_MODE:
        ctx.delay(seconds=5)
    else:
        ctx.delay(minutes=5)

    ctx.comment('\n~~~~~~~~~~~~~ENGAGING MAGNENTIC MODULE~~~~~~~~~~~~\n')
    if TEST_MODE:
        ctx.delay(seconds=bead_delay_time)
    else:
        ctx.delay(minutes=bead_delay_time)

    ctx.comment('\n~~~~~~~~~~~~~REMOVING SUPERNATANT~~~~~~~~~~~~\n')
    for dest in samples:
        pick_up(m300)
        m300.move_to(dest.top())
        ctx.max_speeds['Z'] /= supernatant_headspeed_modulator
        ctx.max_speeds['A'] /= supernatant_headspeed_modulator
        m300.aspirate(200, dest.bottom().move(types.Point(x=-1, y=0, z=0)),
                      rate=0.5)
        m300.move_to(dest.top())
        ctx.max_speeds['Z'] *= supernatant_headspeed_modulator
        ctx.max_speeds['A'] *= supernatant_headspeed_modulator
        m300.dispense(200, trash)
        drop_tip(m300)

    ctx.comment('\n~~~~~~~~~~~~~WASHING BEADS WITH BUFFER~~~~~~~~~~~~\n')
    for dest in samples:
        pick_up(m300)
        m300.aspirate(200, wash_3)
        m300.dispense(200, dest)
        bead_mixing(dest, m300, 200, reps=6)
        drop_tip(m300)

    mag_deck.engage(height_from_base=mag_height)
    if TEST_MODE:
        ctx.delay(seconds=wash_delay_time)
    else:
        ctx.delay(minutes=wash_delay_time)

    ctx.comment('\n~~~~~~~~~~~~~REMOVING SUPERNATANT~~~~~~~~~~~~\n')
    for dest in samples:
        pick_up(m300)
        m300.move_to(dest.top())
        ctx.max_speeds['Z'] /= supernatant_headspeed_modulator
        ctx.max_speeds['A'] /= supernatant_headspeed_modulator
        m300.aspirate(200, dest.bottom().move(types.Point(x=-1, y=0, z=0)),
                      rate=0.5)
        m300.move_to(dest.top())
        ctx.max_speeds['Z'] *= supernatant_headspeed_modulator
        ctx.max_speeds['A'] *= supernatant_headspeed_modulator
        m300.dispense(200, trash)
        drop_tip(m300)
        pick_up(m20)
        m20.move_to(dest.top())
        ctx.max_speeds['Z'] /= supernatant_headspeed_modulator
        ctx.max_speeds['A'] /= supernatant_headspeed_modulator
        m20.aspirate(10, dest.bottom().move(types.Point(x=-1, y=0, z=0)),
                     rate=0.5)
        m20.move_to(dest.top())
        ctx.max_speeds['Z'] *= supernatant_headspeed_modulator
        ctx.max_speeds['A'] *= supernatant_headspeed_modulator
        m20.dispense(10, trash)
        drop_tip(m20)

    for src, dest in zip(strand_primer_mix, samples):
        pick_up(m20)
        m20.aspirate(11.5, src)
        m20.dispense(11.5, dest)
        m20.mix(5, 10, dest, rate=0.5)
        drop_tip(m20)

    if flash:
        if not ctx._hw_manager.hardware.is_simulator:
            cancellationToken.set_true()
        thread = create_thread(ctx, cancellationToken)
    m300.home()
    ctx.pause('\n\nMOVE PLATE IN SLOT 1 TO OFF-DECK THERMOCYCLER\n'
              'REFER TO 1.2.37 FOR SPECIFIC HEATING/COOLING CYCLE\n'
              'SPIN PLATE DOWN BEFORE RETURNING TO DECK\n'
              'RETURN PLATE TO SLOT 1 WHEN FINISHED\n\n')
    ctx.home()  # home before continuing with protocol
    if flash:
        cancellationToken.set_false()  # stop light flashing after home
        thread.join()
    ctx.set_rail_lights(True)

    ctx.comment('\n~~~~~~~~~~~~~SEPARATING RNA SOLUTION~~~~~~~~~~~~\n')
    mag_deck.engage(height_from_base=mag_height)
    if TEST_MODE:
        ctx.delay(seconds=2)
    else:
        ctx.delay(minutes=2)

    ctx.comment('\n~~~~~~~~~~~~~MOVING RNA TO NEW PLATE~~~~~~~~~~~~\n')
    for s, d in zip(samples, final_dest):
        pick_up(m20)
        m20.aspirate(10, s)
        m20.dispense(10, d)
        drop_tip(m20)

    if flash:
        if not ctx._hw_manager.hardware.is_simulator:
            cancellationToken.set_true()
        thread = create_thread(ctx, cancellationToken)
    m300.home()
    ctx.pause('\n\n~~~~~~~~~~~~~~PROTOCOL COMPLETE~~~~~~~~~~~~~~~\n')
    ctx.home()  # home before continuing with protocol
    if flash:
        cancellationToken.set_false()  # stop light flashing after home
        thread.join()
    ctx.set_rail_lights(True)

    for c in ctx.commands():
        print(c)
