from opentrons.protocol_api.labware import OutOfTipsError
from opentrons import types

metadata = {
    'protocolName': '''LC-MS Sample Prep: part 1 -
                       Standards/Calibration Curves''',
    'author': 'Steve Plonk <protocols@opentrons.com>',
    'apiLevel': '2.9'
}


def run(ctx):

    # get the parameter values from json above
    [full_volume, include_standards_only, include_patient_samples,
     labware_tips20, labware_tips300, labware_tuberack, clearance_meoh_water,
     clearance_dil_dispense, touch_radius, touch_v_offset, track_start,
     clearance_tfa, clearance_mecn, mix_reps] = get_values(  # noqa: F821
      'full_volume', 'include_standards_only', 'include_patient_samples',
      'labware_tips20', 'labware_tips300', 'labware_tuberack',
      'clearance_meoh_water', 'clearance_dil_dispense', 'touch_radius',
      'touch_v_offset', 'track_start', 'clearance_tfa', 'clearance_mecn',
      'mix_reps')

    ctx.set_rail_lights(True)

    # tips, p20 multi gen2, p300 multi gen2
    tips20 = [ctx.load_labware(
     labware_tips20, str(slot)) for slot in [2]]
    p20s = ctx.load_instrument(
        "p20_single_gen2", 'left', tip_racks=tips20)
    tips300 = [ctx.load_labware(labware_tips300, str(slot)) for slot in [6]]
    p300s = ctx.load_instrument(
        "p300_single_gen2", 'right', tip_racks=tips300)

    """
    helper functions
    """
    def pick_up_or_refill(current_pipette):
        try:
            current_pipette.pick_up_tip()
        except OutOfTipsError:
            pause_attention(
             """Please Refill the {} Tip Boxes
                and Empty the Tip Waste.""".format(current_pipette))
            current_pipette.reset_tipracks()
            current_pipette.pick_up_tip()

    def pause_attention(message):
        ctx.set_rail_lights(False)
        ctx.delay(seconds=10)
        ctx.pause(message)
        ctx.set_rail_lights(True)

    def slow_tip_withdrawal(current_pipette, well_location, to_center=False):
        if current_pipette.mount == 'right':
            axis = 'A'
        else:
            axis = 'Z'
        ctx.max_speeds[axis] = 10
        if to_center is False:
            current_pipette.move_to(well_location.top())
        else:
            current_pipette.move_to(well_location.center())
        ctx.max_speeds[axis] = None

    def meoh_flow_rates(current_pipette):
        if (current_pipette.name == 'p300_multi_gen2' or
           current_pipette.name == 'p300_single_gen2'):
            current_pipette.flow_rate.aspirate = 92.86
            current_pipette.flow_rate.dispense = 100
            current_pipette.flow_rate.blow_out = 100
        elif (current_pipette.name == 'p20_multi_gen2' or
              current_pipette.name == 'p20_single_gen2'):
            current_pipette.flow_rate.aspirate = 7.56
            current_pipette.flow_rate.dispense = 22
            current_pipette.flow_rate.blow_out = 22

    def plasma_flow_rates(current_pipette):
        if (current_pipette.name == 'p300_multi_gen2' or
           current_pipette.name == 'p300_single_gen2'):
            current_pipette.flow_rate.aspirate = 60
            current_pipette.flow_rate.dispense = 60
            current_pipette.flow_rate.blow_out = 60
        elif (current_pipette.name == 'p20_multi_gen2' or
              current_pipette.name == 'p20_single_gen2'):
            current_pipette.flow_rate.aspirate = 3.5
            current_pipette.flow_rate.dispense = 3.5
            current_pipette.flow_rate.blow_out = 3.5

    def default_flow_rates(current_pipette):
        if (current_pipette.name == 'p300_multi_gen2' or
           current_pipette.name == 'p300_single_gen2'):
            current_pipette.flow_rate.aspirate = 92.86
            current_pipette.flow_rate.dispense = 92.86
            current_pipette.flow_rate.blow_out = 92.86
        elif (current_pipette.name == 'p20_multi_gen2' or
              current_pipette.name == 'p20_single_gen2'):
            current_pipette.flow_rate.aspirate = 7.56
            current_pipette.flow_rate.dispense = 7.56
            current_pipette.flow_rate.blow_out = 7.56

    """
    **custom tube rack definition**
    **theoretically extends eppendorfs**
    **to 6 mm above the top of the rack**
    **to match height of filters**
    **locations relative to top and center coded accordingly**
    """

    ctx.comment("""
    tube rack in deck slot 1:
    A1-A6,B1-B6 - 200 uM unlabeled solution
    followed by 11 serial 1:2 dilutions
    C1-C3 three pooled samples (if included)
    C4-C6 amicon filters (for pooled samples if included)
    D1 - 100 uM labeled solution
    D2 - 1:1 MeOH:Water
    D3 - 100 mM NEM
    D4 - Golden Plasma
    D5 - 4:1 MeCN:Water
    reservoir in deck slot 5:
    A1 - TFA in MeCN
    """)

    # reagents and dilutions
    tuberack = ctx.load_labware(
     labware_tuberack, '1', 'Tube Rack')
    unlabeled_soln_200um, *dilutions = [
     well for row in tuberack.rows() for well in row][:12]
    labeled_soln_100um, meoh_water, nem_100mm, golden_plasma, mecn = [
     tuberack.wells_by_name()[well] for well in ['D1', 'D2', 'D3', 'D4', 'D5']]
    reservoir = ctx.load_labware('nest_12_reservoir_15ml', '5', 'Reservoir')
    tfa = reservoir.wells_by_name()['A1']

    # samples
    sample_tuberack = ctx.load_labware(
     labware_tuberack, '4', 'Sample Tube Rack')
    [*samples] = [well for row in sample_tuberack.rows() for well in row][:12]
    [*amicon_filters] = [
     well for row in sample_tuberack.rows() for well in row][12:]

    # pooled samples if included
    if not include_standards_only:
        ctx.comment("""
        ***POOLED SAMPLES INCLUDED IN THIS RUN***
        tube rack in deck slot 1:
        C1-C3 three pooled samples
        C4-C6 corresponding amicon filters
        """)
        [*samples_pooled] = [
         well for row in tuberack.rows() for well in row][12:15]
        [*amicon_filters_pooled] = [
         well for row in tuberack.rows() for well in row][15:18]

        if include_patient_samples:
            ctx.comment("""
            ***24 PATIENT SAMPLES INCLUDED IN THIS RUN***
            tube rack in deck slot 7:
            A1-A6,B1-B6 1st twelve patient samples
            C1-C6,D1-D6 corresponding amicon filters
            tube rack in deck slot 10:
            A1-A6,B1-B6 another twelve patient samples
            C1-C6,D1-D6 corresponding amicon filters
            """)

            # patient samples
            [*pt_tuberacks] = [
             ctx.load_labware(labware_tuberack, str(slot),
                              'Patient Tube Rack') for slot in [7, 10]]

            pt_samples = []
            for rack in pt_tuberacks:
                new = [well for row in rack.rows() for well in row][:12]
                pt_samples.extend(new)

            pt_amicon_filters = []
            for rack in pt_tuberacks:
                new = [well for row in rack.rows() for well in row][12:]
                pt_amicon_filters.extend(new)

    else:
        ctx.comment("""
        ***THIS RUN INCLUDES STANDARDS ONLY***
        ***NO POOLED SAMPLES INCLUDED IN THIS RUN***
        tube rack in deck slot 1:
        C1-C3 Empty
        C4-C6 Empty
        """)

    ctx.delay(seconds=10)
    pause_attention("""
    Set up: Unlabeled 200 uM soln in A1 of tuberack deck slot 1,
    1:2 dilutions in A2-A6,B1-B6 in tuberack slot 1,
    1:1 MeOH:Water in D2 in tuberack slot 1
    Labeled 100 uM soln in D1 tuberack slot 1
    100 mM NEM in D3 tuberack slot 1
    Golden Plasma in D4 tuberack slot 1
    4:1 acetonitrile:water in D5 of tuberack slot 1
    12 sample tubes in A1-A6, B1-B6 of tuberack deck slot 4
    12 amicon filters in C1-C6, D1-D6 of tuberack deck slot 4
    reservoir with TFA in MeCN and MeCN:Water in deck slot 5
    p20 tips in slot 2
    p300 tips in slot 6.
    """)

    if not full_volume:
        div = 2
        ctx.comment("""
        ****half-volumes will be used****
        """)
    else:
        div = 1

    ctx.comment("""
    add {} ul 1:1 MeOH:Water
    to make 11 serial dilutions 1:2 from unlabelled 200 um solution in A1

    liquid handling method for methanol:water:
    fast flow rate for blow out
    15 ul air gap
    delayed blowout after dispense (let meoh fall to bottom of tip first)
    repeat blowout (for complete dispense)
    tip touch
    """.format(str(20 / div)))

    if full_volume:
        pip = p300s
    else:
        pip = p20s
    meoh_flow_rates(pip)
    for index, dilution in enumerate(dilutions):
        pip.pick_up_tip()
        pip.aspirate(20 / div, meoh_water.bottom(clearance_meoh_water))
        pip.air_gap(5 / div)
        pip.dispense(
         (20 / div)+(5 / div), dilution.bottom(clearance_dil_dispense))
        for rep in range(3):
            if rep > 0:
                pip.aspirate(
                 20, dilution.bottom(10))
            ctx.delay(seconds=1)
            pip.blow_out(dilution.bottom(10))
        pip.touch_tip(radius=touch_radius, v_offset=touch_v_offset, speed=20)
        if index == 0:
            source = unlabeled_soln_200um.bottom(1)
        else:
            source = dilutions[index-1].bottom(1)
        pip.aspirate(20 / div, source)
        pip.air_gap(5 / div)
        pip.dispense(
         (20 / div)+(5 / div), dilution.bottom(clearance_dil_dispense))
        pip.mix(mix_reps, 20 / div, dilution.bottom(clearance_dil_dispense))
        for rep in range(3):
            if rep > 0:
                pip.aspirate(
                 20, dilution.bottom(10))
            ctx.delay(seconds=1)
            pip.blow_out(dilution.bottom(10))
        pip.touch_tip(radius=touch_radius, v_offset=touch_v_offset, speed=20)
        pip.drop_tip()
    default_flow_rates(pip)

    ctx.comment("""
    add {} ul Golden Plasma to each of 12 sample tubes

    use liquid handling method for plasma
    aspirate extra volume
    reduced aspirate and dispense speeds
    slow tip withdrawal from plasma
    avoid over-immersion of tip (liquid height tracking)
    """.format(str(90 / div)))

    plasma_flow_rates(p300s)
    p300s.pick_up_tip()
    starting_clearance = track_start
    tracking_clearance = starting_clearance
    ending_clearance = 2
    increment = (starting_clearance - ending_clearance) / len(samples)
    p300s.aspirate(35 / div, golden_plasma.bottom(starting_clearance))
    for sample in samples:
        p300s.aspirate(90 / div, golden_plasma.bottom(tracking_clearance))
        slow_tip_withdrawal(p300s, golden_plasma)
        if tracking_clearance >= ending_clearance + increment:
            tracking_clearance -= increment
        else:
            tracking_clearance = ending_clearance
        p300s.dispense(90 / div, sample.bottom(2))
        slow_tip_withdrawal(p300s, sample)
    p300s.drop_tip()
    default_flow_rates(p300s)

    ctx.comment("""
    transfer {} ul of each serial dilution to the corresponding sample tube
    transfer {} ul 1:1 MeOH:Water to pooled and patient samples (if included)
    vortex 5 min
    use liquid handling method for MeOH:Water
    """.format(str(10 / div), str(10 / div)))
    meoh_flow_rates(p20s)
    dilutions.insert(0, unlabeled_soln_200um)
    for index, dilution in enumerate(dilutions):
        p20s.pick_up_tip()
        p20s.aspirate(10 / div, dilution.bottom(clearance_dil_dispense))
        p20s.air_gap(2)
        p20s.dispense((10 / div)+2, samples[index].bottom(3))
        slow_tip_withdrawal(p20s, samples[index], to_center=True)
        for rep in range(3):
            if rep > 0:
                p20s.aspirate(
                 10, samples[index].center().move(types.Point(x=0, y=0, z=-3)))
            ctx.delay(seconds=1)
            p20s.blow_out(
             samples[index].center().move(types.Point(x=0, y=0, z=-3)))
        p20s.touch_tip(radius=0.75, v_offset=-8, speed=20)
        p20s.drop_tip()
    default_flow_rates(p20s)

    if not include_standards_only:
        meoh_flow_rates(p20s)
        for pooled_sample in samples_pooled:
            p20s.pick_up_tip()
            p20s.aspirate(10 / div, meoh_water.bottom(clearance_meoh_water))
            p20s.air_gap(2)
            p20s.dispense((10 / div)+2, pooled_sample.bottom(3))
            slow_tip_withdrawal(p20s, pooled_sample, to_center=True)
            for rep in range(3):
                if rep > 0:
                    p20s.aspirate(
                     10, pooled_sample.center().move(
                      types.Point(x=0, y=0, z=-3)))
                ctx.delay(seconds=1)
                p20s.blow_out(
                 pooled_sample.center().move(types.Point(x=0, y=0, z=-3)))
            p20s.touch_tip(radius=0.75, v_offset=-8, speed=20)
            p20s.drop_tip()
        default_flow_rates(p20s)

        if include_patient_samples:
            meoh_flow_rates(p20s)
            for pt_sample in pt_samples:
                pick_up_or_refill(p20s)
                p20s.aspirate(
                 10 / div, meoh_water.bottom(clearance_meoh_water))
                p20s.air_gap(2)
                p20s.dispense((10 / div)+2, pt_sample.bottom(3))
                slow_tip_withdrawal(p20s, pt_sample, to_center=True)
                for rep in range(3):
                    if rep > 0:
                        p20s.aspirate(
                         10, pt_sample.center().move(
                          types.Point(x=0, y=0, z=-3)))
                    ctx.delay(seconds=1)
                    p20s.blow_out(
                     pt_sample.center().move(types.Point(x=0, y=0, z=-3)))
                p20s.touch_tip(radius=0.75, v_offset=-8, speed=20)
                p20s.drop_tip()
            default_flow_rates(p20s)

    pause_attention("Vortex samples 5 min and return.")

    ctx.comment("""
    add {} ul NEM to each tube
    vortex 15 min
    """.format(str(10 / div)))
    if not include_standards_only:
        for pooled_sample in samples_pooled:
            samples.append(pooled_sample)

        if include_patient_samples:
            for pt_sample in pt_samples:
                samples.append(pt_sample)

    for sample in samples:
        pick_up_or_refill(p20s)
        p20s.aspirate(10 / div, nem_100mm.bottom(3))
        p20s.dispense(10 / div, sample.bottom(3))
        slow_tip_withdrawal(p20s, sample, to_center=True)
        p20s.blow_out(sample.center().move(types.Point(x=0, y=0, z=-3)))
        p20s.touch_tip(radius=0.75, v_offset=-8, speed=20)
        p20s.drop_tip()

    pause_attention("Vortex tubes 15 min and return.")

    ctx.comment("""
    add {} ul 100 uM labelled standard to each tube
    vortex 5 min
    use liquid handling method for MeOH:Water
    """.format(str(5 if div == 1 else 2)))
    meoh_flow_rates(p20s)
    for sample in samples:
        pick_up_or_refill(p20s)
        if full_volume:
            p20s.aspirate(5, labeled_soln_100um.bottom(2))
        else:
            p20s.aspirate(2, labeled_soln_100um.bottom(2))
        p20s.air_gap(2)
        if full_volume:
            p20s.dispense(7, sample.bottom(3))
        else:
            p20s.dispense(4, sample.bottom(3))
        slow_tip_withdrawal(p20s, sample, to_center=True)
        for rep in range(3):
            if rep > 0:
                p20s.aspirate(
                 10, sample.center().move(types.Point(x=0, y=0, z=-3)))
            ctx.delay(seconds=1)
            p20s.blow_out(sample.center().move(types.Point(x=0, y=0, z=-3)))
        p20s.touch_tip(radius=0.75, v_offset=-8, speed=20)
        p20s.drop_tip()
    default_flow_rates(p20s)

    pause_attention("Vortex tubes 5 min and return.")

    ctx.comment("""
    add {} ul TFA in acetonitrile to each tube
    vortex 10 min
    spin 15 min
    use same liquid handling method as for MeOH:Water
    """.format(str(540 / div)))
    meoh_flow_rates(p300s)
    for sample in samples:
        for rep in range(3):
            pick_up_or_refill(p300s)
            p300s.aspirate(180 / div, tfa.bottom(clearance_tfa))
            p300s.air_gap(15)
            p300s.dispense((180 / div)+15, sample.bottom(3))
            p300s.move_to(sample.top(-12))
            for rep in range(3):
                if rep > 0:
                    p300s.aspirate(180, sample.top(-12))
                ctx.delay(seconds=1)
                p300s.blow_out(sample.top(-12))
            p300s.touch_tip(radius=0.75, v_offset=-8, speed=20)
            p300s.drop_tip()
    default_flow_rates(p300s)

    pause_attention("Vortex tubes 10 min, spin 15 min, and return.")

    ctx.comment("""
    transfer {} ul sup from each tube to Amicon filter
    spin 2.5 hours
    dry in speedvac aqueous dry setting 1.5 hours
    return
    resuspend in 4:1 acetonitrile:water
    use same liquid handling method as for MeOH:Water
    """.format(str(500 / div)))
    if not include_standards_only:
        for pooled_filter in amicon_filters_pooled:
            amicon_filters.append(pooled_filter)

        if include_patient_samples:
            for pt_filter in pt_amicon_filters:
                amicon_filters.append(pt_filter)

    for index, sample in enumerate(samples):
        pick_up_or_refill(p300s)
        meoh_flow_rates(p300s)
        for rep in range(3):
            p300s.aspirate(166.7 / div, sample.bottom(round(16/(rep + 1))))
            p300s.air_gap(15)
            p300s.dispense((166.7 / div)+15, amicon_filters[index].top())
            for rep in range(3):
                if rep > 0:
                    p300s.aspirate(
                     180, amicon_filters[index].top())
                ctx.delay(seconds=1)
                p300s.blow_out(amicon_filters[index].top())
            p300s.touch_tip(radius=0.75, v_offset=-2, speed=20)
        p300s.drop_tip()
    default_flow_rates(p300s)

    pause_attention("Spin filters 2.5 hours, dry 1.5 hours, return.")

    # filters removed (tube alone same as eppendorf) dispense .bottom(5)
    meoh_flow_rates(p300s)
    for filter in amicon_filters:
        pick_up_or_refill(p300s)
        p300s.aspirate(40 / div, mecn.bottom(clearance_mecn))
        p300s.air_gap(15)
        p300s.dispense((40 / div)+15, filter.bottom(5))
        p300s.move_to(filter.top(-12))
        for rep in range(3):
            if rep > 0:
                p300s.aspirate(180, filter.top(-12))
            ctx.delay(seconds=1)
            p300s.blow_out(filter.top(-12))
        p300s.touch_tip(radius=0.75, v_offset=-8, speed=20)
        p300s.drop_tip()
    default_flow_rates(p300s)

    pause_attention("Transfer to vials, load QQQ7 LC-MS, inject 5 μl.")
