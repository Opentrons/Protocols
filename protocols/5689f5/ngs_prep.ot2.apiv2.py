from opentrons.types import Point
import math

metadata = {
    'protocolName': 'NGS Clean Up v8',
    'author': 'Opentrons <protocols@opentrons.com>',
    'apiLevel': '2.12'
}

TEST_MODE_BEADS = False
TEST_MODE_BIND_INCUBATE = False
TEST_MODE_AIRDRY = False


def run(ctx):

    [num_samples, mount_m20, mount_m300] = get_values(  # noqa: F821
        'num_samples', 'mount_m20', 'mount_m300')

    if TEST_MODE_BEADS:
        mixreps = 1
    else:
        mixreps = 15
    z_offset_resuspension = 2.0
    z_offset_supernatant_initial = 0.5
    z_offset_supernatant = 0.3
    radial_offset_fraction_resuspension = 0.6
    radial_offset_fraction_supernatant = 0.5
    time_incubation_minutes = 5
    time_settling_minutes = 5
    time_incubation_elution_minutes = 3
    time_settling_minutes_elution = 3
    vol_starting = 5
    vol_binding_buffer = 5
    vol_ampure_beads = 8
    vol_ethanol = 50
    vol_elution_buffer = 7.6
    vol_elution_final = 6.6

    ctx.max_speeds['X'] = 200
    ctx.max_speeds['Y'] = 200

    magdeck = ctx.load_module('magnetic module gen2', '4')
    magdeck.disengage()
    magplate = magdeck.load_labware('nest_96_wellplate_100ul_pcr_full_skirt',
                                    'sample plate')
    elution_plate = ctx.load_labware('nest_96_wellplate_100ul_pcr_full_skirt',
                                     '1', 'elution plate')
    res1 = ctx.load_labware('nest_12_reservoir_15ml', '5',
                            'reagent reservoir (ethanol and waste)')
    res2 = ctx.load_labware('nest_96_wellplate_100ul_pcr_full_skirt', '2',
                            'reagent plate')
    tips200 = [
        ctx.load_labware('opentrons_96_filtertiprack_200ul', slot,
                         '200µl filtertiprack')
        for slot in ['3', '6'][:math.ceil(num_samples/48)]]
    tips20 = [
        ctx.load_labware('opentrons_96_filtertiprack_20ul', slot,
                         '20µl filtertiprack')
        for slot in ['7', '8', '9', '11'][:math.ceil(num_samples/24)]]

    # load P300M pipette
    m20 = ctx.load_instrument('p20_multi_gen2', mount_m20, tip_racks=tips20)
    m300 = ctx.load_instrument('p300_multi_gen2', mount_m300,
                               tip_racks=tips200)

    """
    Here is where you can define the locations of your reagents.
    """
    etoh = res1.rows()[0][0]
    waste = res1.rows()[0][-1].top()
    dna_binding_buffer = res2.rows()[0][0]
    ampure_beads = res2.rows()[0][1]
    elution_buffer = res2.rows()[0][2]

    num_cols = math.ceil(num_samples/8)
    mag_samples = magplate.rows()[0][:num_cols]
    elution_samples = elution_plate.rows()[0][5:5+num_cols]

    parking_sets20 = [
        [tip for rack in m20.tip_racks
         for tip in rack.rows()[0]][i*num_cols:(i+1)*num_cols]
        for i in range(4)]
    parking_sets300 = [
        [tip for rack in m300.tip_racks
         for tip in rack.rows()[0]][i*num_cols:(i+1)*num_cols]
        for i in range(2)]

    waste_vol = 0
    waste_threshold = waste.labware.as_well().max_volume * 0.95  # 95% cap

    def remove_supernatant(pip, vol, z_offset=z_offset_supernatant,
                           parking_spots=None):
        """
        `remove_supernatant` will transfer supernatant from the deepwell
        extraction plate to the liquid waste reservoir.
        :param vol (float): The amount of volume to aspirate from all deepwell
                            sample wells and dispense in the liquid waste.
        :param park (boolean): Whether to pick up sample-corresponding tips
                               in the 'parking rack' or to pick up new tips.
        """

        def _waste_track(vol):
            nonlocal waste_vol
            if waste_vol + vol >= waste_threshold:
                # Setup for flashing lights notification to empty liquid waste
                ctx.home()
                ctx.pause('Please empty liquid waste before resuming.')
                waste_vol = 0
            waste_vol += vol

        if not parking_spots:
            parking_spots = [None for _ in range(num_cols)]

        pip.flow_rate.aspirate /= 5
        for m, spot in zip(mag_samples, parking_spots):
            side = -1 if magplate.rows()[0].index(m) % 2 == 0 else 1
            if not pip.has_tip:
                pip.pick_up_tip(spot)
            _waste_track(vol)
            asp_loc = m.bottom().move(Point(
                x=side*m.diameter/2*radial_offset_fraction_supernatant,
                z=z_offset))
            pip.move_to(m.center())
            pip.aspirate(vol, asp_loc)
            pip.move_to(m.bottom().move(Point(z=z_offset)))
            pip.dispense(vol, waste)
            pip.air_gap(5)
            pip.drop_tip()
        pip.flow_rate.aspirate *= 5

    def wick(pip, well, side=1):
        pip.move_to(well.bottom().move(Point(x=side*well.diameter/2*0.8, z=3)))

    # transfer binding buffer
    parking_set = parking_sets20.pop(0)
    for m, p in zip(mag_samples, parking_set):
        m20.pick_up_tip(p)
        m20.transfer(vol_binding_buffer, dna_binding_buffer.bottom(0.5),
                     m.bottom(1), mix_after=(mixreps, vol_binding_buffer),
                     new_tip='never')
        wick(m20, m)
        m20.drop_tip()

    if not TEST_MODE_BIND_INCUBATE:
        ctx.delay(minutes=time_incubation_minutes, msg=f'Incubating off magnet \
for {time_incubation_minutes} minutes.')

    # transfer ampure beads
    parking_set = parking_sets20.pop(0)
    for m, p in zip(mag_samples, parking_set):
        m20.pick_up_tip(p)
        m20.transfer(vol_ampure_beads, ampure_beads.bottom(0.5), m.bottom(1),
                     new_tip='never')
        for _ in range(mixreps):
            m20.aspirate(vol_ampure_beads, m.bottom(1))
            m20.dispense(vol_ampure_beads, m.bottom(3))
        wick(m20, m)
        m20.drop_tip(p)

    if not TEST_MODE_BIND_INCUBATE:
        ctx.delay(minutes=time_incubation_minutes, msg=f'Incubating off magnet \
for {time_incubation_minutes} minutes.')

    magdeck.engage()
    if not TEST_MODE_BEADS:
        ctx.delay(minutes=time_settling_minutes, msg=f'Incubating on magnet \
for {time_settling_minutes} minutes.')

    remove_supernatant(m20, vol_starting+vol_binding_buffer+vol_ampure_beads-2,
                       z_offset=z_offset_supernatant_initial,
                       parking_spots=parking_set)

    # etoh washes
    wells_per_asp_etoh = math.floor(
        m300.tip_racks[0].wells()[0].max_volume/vol_ethanol)
    num_chunks = math.ceil(num_cols/wells_per_asp_etoh)
    chunks = [
        mag_samples[i*wells_per_asp_etoh:(i+1)*wells_per_asp_etoh]
        if i < num_chunks - 1
        else mag_samples[i*wells_per_asp_etoh:]
        for i in range(num_chunks)
    ]
    m300.flow_rate.dispense /= 2
    for _ in range(2):
        parking_set = parking_sets300.pop(0)
        m300.pick_up_tip(parking_set[0])
        for chunk in chunks:
            m300.aspirate(len(chunk)*vol_ethanol, etoh)
            for m in chunk:
                m300.dispense(vol_ethanol, m.top())
                ctx.delay(seconds=1)
        m300.move_to(etoh.top())
        ctx.delay(seconds=10)
        remove_supernatant(m300, 50, z_offset_supernatant_initial,
                           parking_spots=parking_set)
    m300.flow_rate.dispense *= 2

    ctx.pause('Centrifuge the plate on the magnetic module, and replace before \
resuming.')

    # remove residual ethanol
    if not TEST_MODE_BEADS:
        ctx.delay(minutes=3)
    parking_set = parking_sets20.pop(0)
    remove_supernatant(m20, 20, parking_spots=parking_set)

    if not TEST_MODE_AIRDRY:
        ctx.delay(minutes=1, msg='Airdrying on magnet.')
    magdeck.disengage()

    # elute
    parking_set = parking_sets20.pop()
    for m, p in zip(mag_samples, parking_set):
        side_beads = 1 if magplate.rows()[0].index(m) % 2 == 0 else -1
        side_elution = -1 if magplate.rows()[0].index(m) % 2 == 0 else 1
        m20.pick_up_tip(p)
        m20.aspirate(vol_elution_buffer, elution_buffer.bottom(0.5))
        m20.move_to(m.center())

        # custom bead resuspension
        m20.flow_rate.aspirate *= 2
        m20.flow_rate.dispense *= 2
        asp_loc = m.bottom(0.2)
        disp_loc = m.bottom().move(Point(
            x=m.diameter/2*side_beads*radial_offset_fraction_resuspension,
            z=z_offset_resuspension))
        m20.dispense(vol_elution_buffer, disp_loc)
        for _ in range(mixreps+5):
            m20.aspirate(vol_elution_buffer*0.8, asp_loc)
            m20.dispense(vol_elution_buffer*0.8, disp_loc)
        m20.flow_rate.aspirate /= 2
        m20.flow_rate.dispense /= 2

        wick(m20, m)
        m20.drop_tip(p)

    if not TEST_MODE_BIND_INCUBATE:
        ctx.delay(minutes=time_incubation_elution_minutes, msg=f'Incubating \
off magnet for {time_incubation_elution_minutes} minutes.')

    magdeck.engage()
    if not TEST_MODE_BEADS:
        ctx.delay(minutes=time_settling_minutes_elution, msg=f'Incubating on \
magnet for {time_settling_minutes_elution} minutes.')

    m20.flow_rate.aspirate /= 5
    for m, e, p in zip(mag_samples, elution_samples, parking_set):
        side_elution = -1 if magplate.rows()[0].index(m) % 2 == 0 else 1
        m20.pick_up_tip(p)
        m20.move_to(m.center())
        m20.aspirate(vol_elution_final, m.bottom().move(Point(
            x=side_elution*m.diameter/2*radial_offset_fraction_supernatant,
            z=z_offset_supernatant)))
        m20.dispense(vol_elution_final, e.bottom(1))
        wick(m20, e)
        m20.drop_tip()
    m20.flow_rate.aspirate /= 5

    magdeck.disengage()
