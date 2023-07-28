from opentrons import protocol_api
from opentrons.types import Point
import math

metadata = {
    'protocolName': 'Paragon Cleanup',
    'author': 'Opentrons <protocols@opentrons.com>',
    'apiLevel': '2.14'
}

TEST_MODE_BEADS = False
TEST_MODE_BIND_INCUBATE = False
TEST_MODE_TEMP = False
TEST_MODE_DROP = False


def run(ctx):

    [num_samples, vol_beads] = get_values(  # noqa: F821
        'num_samples', 'vol_beads')

    if TEST_MODE_BEADS:
        mixreps = 1
    else:
        mixreps = 10
    time_settling_minutes_wash = 0.5
    time_settling_minutes_elution = 5
    vol_initial = 30.0
    vol_beads = 66.0
    vol_wash = 200.0
    vol_elution = 11.0
    z_offset = 3.0
    radial_offset_fraction = 0.3  # fraction of radius
    engage_height = 8.5

    # tuning parameters
    ctx.max_speeds['X'] = 200
    ctx.max_speeds['Y'] = 200

    # modules
    magdeck = ctx.load_module('magnetic module gen2', '4')
    magdeck.disengage()

    # labware
    elution_plate = ctx.load_labware(
        'nest_96_wellplate_100ul_pcr_full_skirt', '1', 'elution plate')
    mag_plate = magdeck.load_labware(
            'nest_96_wellplate_100ul_pcr_full_skirt', 'TAG1 plate')
    reservoir = ctx.load_labware('nest_12_reservoir_15ml', '2',
                                 'reagent reservoir')
    tips20 = [
        ctx.load_labware('opentrons_96_filtertiprack_20ul', slot)
        for slot in ['5']]
    tips200 = [
        ctx.load_labware('opentrons_96_filtertiprack_200ul', slot)
        for slot in ['3', '6', '9']]

    # load P300M pipette
    m20 = ctx.load_instrument(
        'p20_multi_gen2', 'right', tip_racks=tips20)
    m300 = ctx.load_instrument(
         'p300_multi_gen2', 'left', tip_racks=tips200)

    # reagents and variables
    num_cols = math.ceil(num_samples/8)
    mag_samples = mag_plate.rows()[0][:num_cols]
    elution_samples = elution_plate.rows()[0][:num_cols]
    beads = reservoir.rows()[0][0]
    etoh = reservoir.rows()[0][:(math.ceil(num_cols/6))]
    elution_buffer = [reservoir.rows()[0][3]]
    liquid_trash = [ctx.loaded_labwares[12].wells()[0].top()]*num_cols

    # define liquids
    try:
        beads_liq = ctx.define_liquid(
            name='Beads', description='ampure beads', display_color='B925FF')
        etoh_liq = ctx.define_liquid(
            name='EtOH', description='ethanol for washing',
            display_color='FFD600')
        elution_buffer_liq = ctx.define_liquid(
            name='TE Buffer', description='low TE buffer for elution',
            display_color='9DFFD8')
        beads.load_liquid(
            liquid=beads_liq, volume=vol_beads*num_samples+2000)
        etoh.load_liquid(
            liquid=etoh_liq, volume=vol_wash*num_samples/len(etoh)+2000)
        elution_buffer.load_liquid(
            liquid=elution_buffer_liq, volume=vol_elution*num_samples+2000)
    except AttributeError:
        pass

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
        del ctx.max_speeds['A']
        del ctx.max_speeds['Z']

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

    parked_tips = {m300: [], m20: []}

    def remove_supernatant(vol,
                           pip=None,
                           z_asp=0.2,
                           park=True,
                           destinations=liquid_trash):
        nonlocal parked_tips
        if not pip:
            pip = m300 if vol >= 20 else m20
        for i, (s, d) in enumerate(zip(mag_samples, liquid_trash)):
            if not pip.has_tip:
                if park:
                    pick_up(pip, parked_tips[pip][i])
                else:
                    pick_up(pip)
            pip.move_to(s.top())
            ctx.max_speeds['A'] = 25
            ctx.max_speeds['Z'] = 25
            side = 0
            pip.aspirate(vol, s.bottom().move(Point(x=side, z=z_asp)))
            pip.move_to(s.top())
            del ctx.max_speeds['A']
            del ctx.max_speeds['Z']
            pip.dispense(vol, d)
            if TEST_MODE_DROP:
                pip.return_tip()
            else:
                pip.drop_tip()
        parked_tips[pip] = []

    def resuspend(pip, location, vol, reps=mixreps,
                  samples=mag_samples, x_mix_fraction=radial_offset_fraction,
                  z_mix=z_offset, dispense_height_rel=2.0):
        pip.flow_rate.aspirate *= 4
        pip.flow_rate.dispense *= 4
        side_x = 1 if samples.index(location) % 2 == 0 else -1
        pip.move_to(location.center())
        for r_ind in range(reps):
            bead_loc = location.bottom().move(
                Point(x=side_x*radius*radial_offset_fraction,
                      z=z_mix))
            pip.aspirate(vol, bead_loc)
            pip.dispense(vol, bead_loc.move(Point(z=dispense_height_rel)))
        pip.flow_rate.aspirate /= 4
        pip.flow_rate.dispense /= 4

    def wash(pip, vol, reagent, time_incubation=0,
             time_settling=0, premix=False,
             do_discard_supernatant=True, do_resuspend=False,
             vol_supernatant=0, park=True, z_resuspension=z_offset,
             supernatant_destinations=liquid_trash):
        nonlocal parked_tips

        columns_per_channel = 12//len(reagent)
        num_transfers = math.ceil(vol/pip.tip_racks[0].wells()[0].max_volume)
        vol_per_transfer = round(vol/num_transfers, 2)

        last_source = None

        for i, well in enumerate(mag_samples):
            source = reagent[i//columns_per_channel]
            pick_up(pip)
            if park:
                parked_tips[pip].append(pip._last_tip_picked_up_from)
            if premix and last_source != source:
                pip.flow_rate.aspirate *= 4
                pip.flow_rate.dispense *= 4
                for _ in range(5):
                    pip.aspirate(200, source.bottom(0.5))
                    pip.dispense(200, source.bottom(5))
                pip.flow_rate.aspirate /= 4
                pip.flow_rate.dispense /= 4
            last_source = source
            for _ in range(num_transfers):
                pip.aspirate(vol_per_transfer, source)
                slow_withdraw(pip, source)
                pip.dispense(vol_per_transfer, well.top())
            if do_resuspend:
                resuspend(pip, well, vol*0.8)
            else:
                if mixreps > 0:
                    pip.flow_rate.aspirate *= 4
                    pip.flow_rate.dispense *= 4
                    pip.mix(mixreps, vol*0.8, well.bottom(2))
                    pip.flow_rate.aspirate /= 4
                    pip.flow_rate.dispense /= 4
            pip.air_gap(20)
            if park or TEST_MODE_DROP:
                pip.return_tip()
            else:
                pip.drop_tip()

        if not TEST_MODE_BIND_INCUBATE:
            ctx.delay(minutes=time_incubation,
                      msg=f'Incubating off MagDeck for \
{time_incubation} minutes.')
        if do_discard_supernatant:
            magdeck.engage(engage_height)
            if not TEST_MODE_BEADS:
                ctx.delay(minutes=time_settling, msg=f'Incubating on \
MagDeck for {time_settling} minutes.')

            remove_supernatant(
                vol_supernatant,
                pip=pip,
                destinations=supernatant_destinations)
            magdeck.disengage()

    pick_up(m300)
    # premix beads and transfer to plate
    for _ in range(mixreps):
        m300.aspirate(200, beads.bottom(1))
        m300.dispense(200, beads.bottom(10))
    for d in mag_samples:
        if not m300.has_tip:
            pick_up(m300)
        m300.aspirate(vol_beads, beads.bottom(0.5))
        slow_withdraw(m300, beads)
        m300.dispense(m300.current_volume, d.bottom(2))
        m300.mix(mixreps, (vol_beads+vol_initial)*0.8, d.bottom(2))
        slow_withdraw(m300, d)
        m300.return_tip()
        parked_tips[m300].append(m300._last_tip_picked_up_from)

    magdeck.engage()
    ctx.delay(minutes=10)

    # remove initial supernatant
    remove_supernatant(vol_initial+vol_beads)

    # wash
    wash(m300, vol_wash, etoh, time_incubation=0,
         time_settling=time_settling_minutes_wash,
         premix=False, do_discard_supernatant=True, do_resuspend=True,
         vol_supernatant=vol_wash)
    wash(m300, vol_wash, etoh, time_incubation=0,
         time_settling=time_settling_minutes_wash,
         premix=False, do_discard_supernatant=False, do_resuspend=True,
         vol_supernatant=vol_wash, park=False)

    # air dry
    ctx.delay(minutes=5, msg='Air Drying')

    # transfer final elution
    wash(m20, vol_elution, elution_buffer, time_incubation=5.0,
         time_settling=time_settling_minutes_elution, vol_supernatant=10.0,
         do_discard_supernatant=True, supernatant_destinations=elution_samples)
