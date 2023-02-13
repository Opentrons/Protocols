from opentrons import protocol_api
from opentrons.types import Point
import math
import time

metadata = {
    'protocolName': '4. Illumina DNA Prep - Clean Up Libraries',
    'author': 'Opentrons <protocols@opentrons.com>',
    'apiLevel': '2.13'
}

TEST_MODE_BEADS = False
TEST_MODE_BIND_INCUBATE = False
TEST_MODE_TEMP = False
TEST_MODE_DROP = False


def run(ctx):

    [num_samples] = get_values(  # noqa: F821
        "num_samples")

    reps_mix = 1 if TEST_MODE_BEADS else 10
    vol_mix = 70
    z_offset = 3.0
    radial_offset_fraction = 0.3

    # tuning parameters
    ctx.max_speeds['X'] = 200
    ctx.max_speeds['Y'] = 200

    # modules
    tempdeck = ctx.load_module('temperature module gen2', '7')
    magdeck = ctx.load_module('magnetic module gen2', '4')
    if not TEST_MODE_TEMP:
        tempdeck.set_temperature(4)
    magdeck.disengage()

    # labware
    mag_plate = magdeck.load_labware(
        'nest_96_wellplate_100ul_pcr_full_skirt', 'PCR plate')
    reagent_plate = tempdeck.load_labware(
        'opentrons_96_aluminumblock_nest_wellplate_100ul', 'reagent plate')
    pcr_plate = ctx.load_labware(
        'nest_96_wellplate_100ul_pcr_full_skirt', '1', 'clean PCR plate')
    reservoir = ctx.load_labware('nest_12_reservoir_15ml', '2', 'reservoir')
    waste_res = ctx.load_labware('nest_1_reservoir_195ml', '5', 'waste')
    tips20 = [
        ctx.load_labware('opentrons_96_filtertiprack_20ul', slot)
        for slot in ['3', '6']]
    tips200 = [
        ctx.load_labware('opentrons_96_filtertiprack_200ul', slot)
        for slot in ['8', '9', '10', '11']]

    # load P300M pipette
    m20 = ctx.load_instrument(
        'p20_multi_gen2', 'right', tip_racks=tips20)
    m300 = ctx.load_instrument(
         'p300_multi_gen2', 'left', tip_racks=tips200)

    # reagents and variables
    num_cols = math.ceil(num_samples/8)
    mag_samples = mag_plate.rows()[0][:num_cols]
    pcr_samples = pcr_plate.rows()[0][:num_cols]
    spb = reagent_plate.rows()[0][6:9]
    spb2 = reagent_plate.rows()[0][9]
    rsb = reagent_plate.rows()[0][10:12]
    water = reservoir.rows()[0][0]
    liquid_trash = [
        waste_res.wells()[0].top()
        for _ in range(math.ceil(num_cols/6))]

    vol_supernatant = 45.0
    vol_supernatant2 = 125.0
    vol_water = 40.0
    vol_spb = 45.0
    vol_spb2 = 15.0
    vol_rsb = 32.0
    vol_elution = 30.0
    ref_well = mag_plate.wells()[0]
    if ref_well.width:
        radius = ref_well.width/2
    else:
        radius = ref_well.diameter/2

    def wick(pip, well, side=1):
        pip.move_to(well.bottom().move(Point(x=side*radius*0.7, z=3)))

    def slow_withdraw(pip, well):
        ctx.max_speeds['A'] = 25
        ctx.max_speeds['Z'] = 25
        pip.move_to(well.top())
        ctx.max_speeds['A'] = 200
        ctx.max_speeds['Z'] = 200

    def pick_up(pip, spot=None):
        if spot:
            pip.pick_up_tip(spot)
        else:
            try:
                pip.pick_up_tip()
            except protocol_api.labware.OutOfTipsError:
                ctx.pause("\n\n\n\nReplace 200ul filtertipracks before \
resuming.\n\n\n\n")
                pip.reset_tipracks()
                pip.pick_up_tip()

    parked_tips = []

    def remove_supernatant(vol, pip=None, z_asp=0.2, park=False):
        nonlocal parked_tips
        if not pip:
            pip = m300 if vol >= 20 else m20
        pip.flow_rate.aspirate /= 5
        for i, s in enumerate(mag_samples):
            if not pip.has_tip:
                if park:
                    pick_up(pip, parked_tips[i])
                else:
                    pick_up(pip)
            pip.move_to(s.top())
            ctx.max_speeds['A'] = 25
            ctx.max_speeds['Z'] = 25
            side = -1 if mag_samples.index(s) % 2 == 0 else 1
            pip.aspirate(vol, s.bottom().move(Point(x=side, z=z_asp)))
            pip.move_to(s.top())
            del ctx.max_speeds['A']
            del ctx.max_speeds['Z']
            pip.dispense(vol, liquid_trash[i//6])
            pip.blow_out(liquid_trash[i//6])
            pip.air_gap(10)
            if TEST_MODE_DROP:
                pip.return_tip()
            else:
                pip.drop_tip()
        parked_tips = []
        pip.flow_rate.aspirate *= 5

    def resuspend(location, reps=reps_mix, vol=vol_mix,
                  samples=mag_samples, x_mix_fraction=radial_offset_fraction,
                  z_mix=z_offset, dispense_height_rel=5.0, rate=1.0):
        side_x = 1 if samples.index(location) % 2 == 0 else -1
        m300.move_to(location.center())
        for r_ind in range(reps):
            bead_loc = location.bottom().move(
                Point(x=side_x*radius*radial_offset_fraction,
                      z=z_mix))
            m300.aspirate(vol, bead_loc, rate=rate)
            m300.dispense(vol, bead_loc.move(Point(z=dispense_height_rel)),
                          rate=rate)
        slow_withdraw(m300, location)

    magdeck.engage()
    if not TEST_MODE_BEADS:
        ctx.delay(minutes=5, msg='Incubating on MagDeck for 5 minutes.')

    # transfer supernatant to clean plate
    for s, d in zip(mag_samples, pcr_samples):
        pick_up(m300)
        m300.move_to(s.top())
        ctx.max_speeds['A'] = 25
        ctx.max_speeds['Z'] = 25
        side = -1 if mag_samples.index(s) % 2 == 0 else 1
        m300.aspirate(vol_supernatant, s.bottom().move(
            Point(x=side, z=0.2)))
        m300.move_to(s.top())
        del ctx.max_speeds['A']
        del ctx.max_speeds['Z']
        m300.dispense(vol_supernatant, d.bottom(2))
        ctx.delay(seconds=2)
        slow_withdraw(m300, d)
        if TEST_MODE_DROP:
            m300.return_tip()
        else:
            m300.drop_tip()

    magdeck.disengage()

    # add water
    for d in mag_samples:
        pick_up(m300)
        m300.aspirate(vol_water, water)
        slow_withdraw(m300, water)
        m300.dispense(vol_water, d.bottom(2))
        ctx.delay(seconds=2)
        # m20.mix(reps_mix, 20, d.bottom(2))
        slow_withdraw(m300, d)
        if TEST_MODE_DROP:
            m300.return_tip()
        else:
            m300.drop_tip()

    # add SPB
    last_spb = None
    for i, d in enumerate(mag_samples):
        pick_up(m300)
        spb_source = spb[i//4]
        if not spb_source == last_spb and not TEST_MODE_BEADS:
            m300.mix(5, 30, spb_source)  # mix if new SPB column
            last_spb = spb_source
        m300.aspirate(vol_spb, spb_source)
        slow_withdraw(m300, spb_source)
        m300.dispense(vol_spb, d.bottom(2))
        m300.mix(reps_mix, vol_water+vol_spb+vol_supernatant*0.8, d.bottom(2))
        ctx.delay(seconds=2)
        slow_withdraw(m300, d)
        if TEST_MODE_DROP:
            m300.return_tip()
        else:
            m300.drop_tip()

    ctx.pause('Move the PCR plate on slot 1 to the magnetic module. Place a \
clean PCR plate in slot 1.')

    start = time.time()

    # pre-add SPB to new plate
    pick_up(m20)
    for d in pcr_samples:
        m20.mix(reps_mix, 10, spb2.bottom(2))
        m20.aspirate(vol_spb2, spb2)
        slow_withdraw(m20, spb2)
        m20.dispense(vol_spb2, d.bottom(0.5))
        wick(m20, d)
        slow_withdraw(m20, d)

    end = time.time()
    delay_time_minutes = 5 - round((end - start) / 60, 2)
    if not TEST_MODE_BIND_INCUBATE:
        ctx.delay(minutes=delay_time_minutes, msg=f'Incubating off magnet for \
{delay_time_minutes} minutes.')

    magdeck.engage()
    if not TEST_MODE_BEADS:
        ctx.delay(minutes=delay_time_minutes, msg='Incubating on magnet for \
5 minutes.')

    # transfer supernatant to plate with SPB
    for s, d in zip(mag_samples, pcr_samples):
        pick_up(m300)
        m300.move_to(s.top())
        ctx.max_speeds['A'] = 25
        ctx.max_speeds['Z'] = 25
        side = -1 if mag_samples.index(s) % 2 == 0 else 1
        m300.aspirate(vol_supernatant2, s.bottom().move(
            Point(x=side, z=0.2)))
        m300.move_to(s.top())
        ctx.max_speeds['A'] = 200
        ctx.max_speeds['Z'] = 200
        m300.dispense(vol_supernatant2, d.bottom(2))
        m300.mix(reps_mix, vol_supernatant2*0.8, d.bottom(2))
        ctx.delay(seconds=2)
        slow_withdraw(m300, d)
        if TEST_MODE_DROP:
            m300.return_tip()
        else:
            m300.drop_tip()

    magdeck.disengage()

    ctx.pause('Move PCR plate from slot 1 to magnetic module. Place a clean \
plate in slot 1.')

    if not TEST_MODE_BIND_INCUBATE:
        ctx.delay(minutes=5, msg='Incubating off magnet for 5 minutes.')

    magdeck.engage()
    if not TEST_MODE_BEADS:
        ctx.delay(minutes=delay_time_minutes, msg='Incubating on magnet for \
5 minutes.')

    remove_supernatant(vol_supernatant2 + vol_spb2, pip=m300)
    remove_supernatant(10, pip=m20)

    if not TEST_MODE_BIND_INCUBATE:
        ctx.delay(minutes=5, msg='Airdrying for 5 minutes.')

    magdeck.disengage()

    # resuspend elution
    for i, d in enumerate(mag_samples):
        rsb_source = rsb[i//6]
        pick_up(m300)
        m300.aspirate(vol_rsb, rsb_source.bottom(0.5))
        slow_withdraw(m300, rsb_source)
        side = 1 if mag_plate.rows()[0].index(d) % 2 == 0 else -1
        loc_dispense = d.bottom().move(
            Point(x=side*radial_offset_fraction, z=z_offset))
        m300.dispense(vol_rsb, loc_dispense)
        resuspend(d)
        ctx.delay(seconds=2)
        slow_withdraw(m300, d)
        if TEST_MODE_DROP:
            m300.return_tip()
        else:
            m300.drop_tip()

    if not TEST_MODE_BIND_INCUBATE:
        ctx.delay(minutes=2, msg='Incubating off magnet for 2 minutes.')

    magdeck.engage()
    if not TEST_MODE_BEADS:
        ctx.delay(minutes=2, msg='Incubating on MagDeck for 2 minutes.')

    # transfer final elution to new PCR plate
    for s, d in zip(mag_samples, pcr_samples):
        pick_up(m300)
        m300.move_to(s.top())
        ctx.max_speeds['A'] = 25
        ctx.max_speeds['Z'] = 25
        side = -1 if mag_samples.index(s) % 2 == 0 else 1
        m300.aspirate(vol_elution, s.bottom().move(
            Point(x=side, z=0.2)))
        m300.move_to(s.top())
        ctx.max_speeds['A'] = 200
        ctx.max_speeds['Z'] = 200
        m300.dispense(vol_elution, d.bottom(2))
        ctx.delay(seconds=2)
        slow_withdraw(m300, d)
        if TEST_MODE_DROP:
            m300.return_tip()
        else:
            m300.drop_tip()

    magdeck.disengage()
