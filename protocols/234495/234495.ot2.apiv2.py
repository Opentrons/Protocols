from opentrons import types

metadata = {
    'protocolName': '''LC-MS Sample Prep: part 1 -
                       Standards/Calibration Curves''',
    'author': 'Steve Plonk <protocols@opentrons.com>',
    'apiLevel': '2.9'
}


def run(ctx):

    # get parameter values from json above
    [labware_tips20, labware_tips300, labware_tuberack, clearance_meoh_water,
     clearance_dil_dispense, touch_radius, touch_v_offset, track_start,
     clearance_tfa, clearance_mecn] = get_values(  # noqa: F821
      'labware_tips20', 'labware_tips300', 'labware_tuberack',
      'clearance_meoh_water', 'clearance_dil_dispense', 'touch_radius',
      'touch_v_offset', 'track_start', 'clearance_tfa', 'clearance_mecn')

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

    def pre_wet(current_pipette, volume, location):
        for rep in range(2):
            current_pipette.aspirate(volume, location)
            current_pipette.dispense(volume, location)

    def meoh_flow_rates(current_pipette):
        if (current_pipette.name == 'p300_multi_gen2' or
           current_pipette.name == 'p300_single_gen2'):
            current_pipette.flow_rate.aspirate = 92.86
            current_pipette.flow_rate.dispense = 300
            current_pipette.flow_rate.blow_out = 300
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

    ctx.comment("""
    tube rack in deck slot 1:
    A1-A6,B1-B6 - 200 uM unlabeled solution
    followed by 11 serial 1:2 dilutions
    D1 - 1:1 MeOH:Water
    D2 - 100 uM labeled solution
    D3 - 100 mM NEM
    D4 - Golden Plasma
    reservoir in deck slot 5:
    A1 - TFA in MeCN
    A2 - 4:1 MeCN:Water
    """)

    # reagents and dilutions
    tuberack = ctx.load_labware(
     labware_tuberack, '1', 'Tube Rack')
    unlabeled_soln_200um, *dilutions = [
     well for row in tuberack.rows() for well in row][:12]
    meoh_water, labeled_soln_100um, nem_100mm, golden_plasma = [
     tuberack.wells_by_name()[well] for well in ['D1', 'D2', 'D3', 'D4']]
    reservoir = ctx.load_labware('nest_12_reservoir_15ml', '5', 'Reservoir')
    tfa = reservoir.wells_by_name()['A1']
    mecn = reservoir.wells_by_name()['A2']

    # samples
    sample_tuberack = ctx.load_labware(
     labware_tuberack, '4', 'Sample Tube Rack')
    [*samples] = [well for row in sample_tuberack.rows() for well in row][:12]
    [*amicon_filters] = [
     well for row in sample_tuberack.rows() for well in row][12:]

    ctx.delay(seconds=10)
    pause_attention("""
    Set up: Unlabeled 200 uM soln in A1 of tuberack deck slot 1,
    1:2 dilutions in A2-A6,B1-B6 in tuberack slot 1,
    1:1 MeOH:Water in D1 in tuberack slot 1
    Labeled 100 uM soln in D2 tuberack slot 1
    100 mM NEM in D3 tuberack slot 1
    Golden Plasma in D4 tuberack slot 1
    12 sample tubes in A1-A6, B1-B6 of tuberack deck slot 4
    12 amicon filters in C1-C6, D1-D6 of tuberack deck slot 4
    reservoir with TFA in MeCN and MeCN:Water in deck slot 5
    p20 tips in slot 2
    p300 tips in slot 9.
    """)

    ctx.comment("""
    add 20 ul 1:1 MeOH:Water (one tube at a time, pausing to vortex)
    to make 200 uM unlabeled soln then 11 serial dilutions 1:2

    liquid handling method for methanol:water:
    fast flow rate for blow out
    pre-wet the tips twice (saturate air)
    15 ul air gap
    delayed blowout after dispense (let meoh fall to bottom of tip first)
    repeat blowout (for complete dispense)
    tip touch
    """)

    meoh_flow_rates(p300s)
    p300s.pick_up_tip()
    pre_wet(p300s, 150, meoh_water.bottom(clearance_meoh_water))
    p300s.aspirate(20, meoh_water.bottom(clearance_meoh_water))
    p300s.air_gap(15)
    p300s.dispense(35, unlabeled_soln_200um.bottom(clearance_dil_dispense))
    for rep in range(3):
        if rep > 0:
            p300s.aspirate(
             100, unlabeled_soln_200um.bottom(clearance_dil_dispense))
        ctx.delay(seconds=1)
        p300s.blow_out(unlabeled_soln_200um.bottom(clearance_dil_dispense))
    p300s.touch_tip(radius=touch_radius, v_offset=touch_v_offset, speed=20)
    p300s.move_to(unlabeled_soln_200um.bottom(
     clearance_dil_dispense).move(types.Point(x=0, y=0, z=15)))
    ctx.pause("""Vortex 5 min and return the tube.""")
    p300s.drop_tip()

    for index, dilution in enumerate(dilutions):
        p300s.pick_up_tip()
        pre_wet(p300s, 150, meoh_water.bottom(clearance_meoh_water))
        p300s.aspirate(20, meoh_water.bottom(clearance_meoh_water))
        p300s.air_gap(15)
        p300s.dispense(35, dilution.bottom(clearance_dil_dispense))
        for rep in range(3):
            if rep > 0:
                p300s.aspirate(
                 100, unlabeled_soln_200um.bottom(clearance_dil_dispense))
            ctx.delay(seconds=1)
            p300s.blow_out(unlabeled_soln_200um.bottom(clearance_dil_dispense))
        p300s.touch_tip(radius=touch_radius, v_offset=touch_v_offset, speed=20)
        if index == 0:
            source = unlabeled_soln_200um.bottom(1)
        else:
            source = dilutions[index-1].bottom(1)
        p300s.move_to(unlabeled_soln_200um.bottom(
         clearance_dil_dispense).move(types.Point(x=0, y=0, z=25)))
        ctx.pause("""Vortex and return the tube.""")
        p300s.aspirate(20, source)
        p300s.air_gap(15)
        p300s.dispense(35, dilution.bottom(clearance_dil_dispense))
        for rep in range(3):
            if rep > 0:
                p300s.aspirate(
                 100, unlabeled_soln_200um.bottom(clearance_dil_dispense))
            ctx.delay(seconds=1)
            p300s.blow_out(unlabeled_soln_200um.bottom(clearance_dil_dispense))
        p300s.touch_tip(radius=touch_radius, v_offset=touch_v_offset, speed=20)
        p300s.drop_tip()

    ctx.comment("""
    add 100 ul 1:1 MeOH:Water to make 100 uM labeled soln
    pause to vortex and sonicate
    use liquid handling method for meoh:water
    """)

    p300s.pick_up_tip()
    pre_wet(p300s, 150, meoh_water)
    p300s.aspirate(100, meoh_water)
    p300s.air_gap(15)
    p300s.dispense(115, labeled_soln_100um.top())
    for rep in range(3):
        if rep > 0:
            p300s.aspirate(100, labeled_soln_100um.top())
        ctx.delay(seconds=1)
        p300s.blow_out(labeled_soln_100um.top())
    p300s.touch_tip(radius=0.75, v_offset=-2, speed=20)
    p300s.move_to(labeled_soln_100um.top().move(types.Point(x=0, y=0, z=15)))
    ctx.pause("""Vortex 5 min. Sonicate 5 min. Return the tube.""")
    p300s.drop_tip()
    default_flow_rates(p300s)

    ctx.comment("""
    add 90 ul Golden Plasma to each of 12 sample tubes

    use liquid handling method for plasma
    aspirate extra volume
    prewet tip
    reduced aspirate and dispense speeds
    slow tip withdrawal from plasma
    avoid over-immersion of tip (liquid height tracking)
    """)

    plasma_flow_rates(p300s)
    p300s.pick_up_tip()
    starting_clearance = track_start
    tracking_clearance = starting_clearance
    ending_clearance = 2
    increment = (starting_clearance - ending_clearance) / len(samples)
    p300s.aspirate(35, golden_plasma.bottom(starting_clearance))
    pre_wet(p300s, 100, golden_plasma.bottom(starting_clearance))
    for sample in samples:
        p300s.aspirate(90, golden_plasma.bottom(tracking_clearance))
        slow_tip_withdrawal(p300s, golden_plasma)
        if tracking_clearance >= ending_clearance + increment:
            tracking_clearance -= increment
        else:
            tracking_clearance = ending_clearance
        p300s.dispense(90, sample.bottom(2))
        slow_tip_withdrawal(p300s, sample)
    p300s.drop_tip()
    default_flow_rates(p300s)

    ctx.comment("""
    transfer 10 ul of each serial dilution to the corresponding sample tube
    vortex 5 min
    use liquid handling method for MeOH:Water
    """)
    meoh_flow_rates(p20s)
    dilutions.insert(0, unlabeled_soln_200um)
    for index, dilution in enumerate(dilutions):
        p20s.pick_up_tip()
        pre_wet(p20s, 20, meoh_water.bottom(clearance_meoh_water))
        p20s.aspirate(10, meoh_water.bottom(clearance_meoh_water))
        p20s.air_gap(2)
        p20s.dispense(12, samples[index].bottom(3))
        slow_tip_withdrawal(p20s, samples[index], to_center=True)
        for rep in range(3):
            if rep > 0:
                p20s.aspirate(10, samples[index].center())
            ctx.delay(seconds=1)
            p20s.blow_out(samples[index].center())
        p20s.touch_tip(radius=0.75, v_offset=-2, speed=20)
        p20s.drop_tip()
    default_flow_rates(p20s)

    pause_attention("Vortex samples 5 min and return.")

    ctx.comment("""
    add 10 ul NEM to each sample tube
    vortex 15 min
    """)
    for sample in samples:
        p20s.pick_up_tip()
        p20s.aspirate(10, nem_100mm.bottom(3))
        p20s.dispense(10, sample.bottom(3))
        slow_tip_withdrawal(p20s, sample, to_center=True)
        p20s.blow_out(sample.center())
        p20s.touch_tip(radius=0.75, v_offset=-2, speed=20)
        p20s.drop_tip()

    pause_attention("Vortex samples 15 min and return.")

    ctx.comment("""
    add 5 ul 100 uM labelled standard to each sample tube
    vortex 5 min
    use liquid handling method for MeOH:Water
    """)
    meoh_flow_rates(p20s)
    for sample in samples:
        p20s.pick_up_tip()
        pre_wet(p20s, 15, labeled_soln_100um.bottom(2))
        p20s.aspirate(10, labeled_soln_100um.bottom(2))
        p20s.air_gap(2)
        p20s.dispense(12, sample.bottom(3))
        slow_tip_withdrawal(p20s, sample, to_center=True)
        for rep in range(3):
            if rep > 0:
                p20s.aspirate(10, sample.center())
            ctx.delay(seconds=1)
            p20s.blow_out(sample.center())
        p20s.touch_tip(radius=0.75, v_offset=-2, speed=20)
        p20s.drop_tip()
    default_flow_rates(p20s)

    pause_attention("Vortex samples 5 min and return.")

    ctx.comment("""
    add 540 ul TFA in acetonitrile to each sample tube
    vortex 10 min
    spin 15 min
    use same liquid handling method as for MeOH:Water
    """)
    meoh_flow_rates(p300s)
    for sample in samples:
        p300s.pick_up_tip()
        pre_wet(p300s, 150, tfa.bottom(clearance_tfa))
        for rep in range(3):
            p300s.aspirate(180, tfa.bottom(clearance_tfa))
            p300s.air_gap(15)
            p300s.dispense(195, sample.top())
            for rep in range(3):
                if rep > 0:
                    p300s.aspirate(180, sample.top())
                ctx.delay(seconds=1)
                p300s.blow_out(sample.top())
                if rep == 2:
                    p300s.touch_tip(radius=0.75, v_offset=-2, speed=20)
        p300s.drop_tip()
    default_flow_rates(p300s)

    pause_attention("Vortex samples 10 min, spin 15 min, and return.")

    ctx.comment("""
    transfer 500 ul sup from each sample tube to Amicon filter
    spin 2.5 hours
    dry in speedvac aqueous dry setting 1.5 hours
    return
    resuspend in 4:1 acetonitrile:water
    use same liquid handling method as for MeOH:Water
    """)
    for index, sample in enumerate(samples):
        p300s.pick_up_tip()
        default_flow_rates(p300s)
        pre_wet(p300s, 150, sample.bottom(4))
        meoh_flow_rates(p300s)
        for rep in range(3):
            p300s.aspirate(166.7, sample.bottom(4))
            p300s.air_gap(15)
            p300s.dispense(181.7, amicon_filters[index].top())
            for rep in range(3):
                if rep > 0:
                    p300s.aspirate(180, amicon_filters[index].top())
                ctx.delay(seconds=1)
                p300s.blow_out(amicon_filters[index].top())
            p300s.touch_tip(radius=0.75, v_offset=-2, speed=20)
        p300s.drop_tip()
    default_flow_rates(p300s)

    pause_attention("Spin filters 2.5 hours, dry 1.5 hours, return.")

    meoh_flow_rates(p300s)
    for filter in amicon_filters:
        p300s.pick_up_tip()
        pre_wet(p300s, 150, mecn.bottom(clearance_mecn))
        p300s.aspirate(40, mecn.bottom(clearance_mecn))
        p300s.air_gap(15)
        p300s.dispense(55, filter.top())
        for rep in range(3):
            if rep > 0:
                p300s.aspirate(180, filter.top())
            ctx.delay(seconds=1)
            p300s.blow_out(filter.top())
        p300s.touch_tip(radius=0.75, v_offset=-2, speed=20)
        p300s.drop_tip()
    default_flow_rates(p300s)

    pause_attention("Transfer to vials, load QQQ7 LC-MS, inject 5 μl.")
