import math
from opentrons import types
from opentrons.protocol_api.labware import OutOfTipsError

metadata = {
    'protocolName': '''Bead Cleanup with Omega MagBind TotalPure NGS Beads''',
    'author': 'Steve Plonk <protocols@opentrons.com>',
    'apiLevel': '2.9'
}


def run(ctx):

    # get parameter values from json above
    [sample_count, labware_tips300, labware_pcr_plate_1, labware_pcr_plate_2,
     labware_reservoir, clearance_reservoir,
     clearance_elution, clearance_bead_pellet,
     flow_rate_beads, delay_beads, engage_height, engage_time, dry_time
     ] = get_values(  # noqa: F821
      'sample_count', 'labware_tips300', 'labware_pcr_plate_1',
      'labware_pcr_plate_2', 'labware_reservoir', 'clearance_reservoir',
      'clearance_elution', 'clearance_bead_pellet', 'flow_rate_beads',
      'delay_beads', 'engage_height', 'engage_time', 'dry_time')

    ctx.set_rail_lights(True)
    if not 1 <= sample_count <= 96:
        raise Exception('Invalid number of samples (must be 1-96).')

    # tips, p300 multi gen2
    tips300 = [
     ctx.load_labware(labware_tips300, str(slot)) for slot in [5, 6, 7, 8, 10]]
    p300m = ctx.load_instrument(
        "p300_multi_gen2", 'right', tip_racks=tips300)

    """
    helper functions
    """
    def pick_up_or_refill(current_pipette):
        try:
            current_pipette.pick_up_tip()
        except OutOfTipsError:
            pause_attention(
             "Please Refill the {} Tip Boxes".format(current_pipette))
            current_pipette.reset_tipracks()
            current_pipette.pick_up_tip()

    def pause_attention(message):
        ctx.set_rail_lights(False)
        ctx.delay(seconds=10)
        ctx.pause(message)
        ctx.set_rail_lights(True)

    def aspirate_with_delay(current_pipette, volume, source, delay_seconds):
        current_pipette.aspirate(volume, source)
        if delay_seconds > 0:
            ctx.delay(seconds=delay_seconds)

    def dispense_with_delay(current_pipette, volume, dest, delay_seconds):
        current_pipette.dispense(volume, dest)
        if delay_seconds > 0:
            ctx.delay(seconds=delay_seconds)

    def mix_with_delay(current_pipette, volume, location, delay_seconds):
        current_pipette.aspirate(volume, location)
        if delay_seconds > 0:
            ctx.delay(seconds=delay_seconds)
        current_pipette.dispense(volume, location)
        if delay_seconds > 0:
            ctx.delay(seconds=delay_seconds)

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

    def set_default_clearances(
     current_pipette, aspirate_setting, dispense_setting):
        if 0 < aspirate_setting < 5 and 0 < dispense_setting < 5:
            current_pipette.well_bottom_clearance.aspirate = aspirate_setting
            current_pipette.well_bottom_clearance.dispense = dispense_setting

    def restore_default_clearances(current_pipette):
        current_pipette.well_bottom_clearance.aspirate = 1
        current_pipette.well_bottom_clearance.dispense = 1

    def custom_flow_rates(current_pipette):
        current_pipette.flow_rate.aspirate = flow_rate_beads
        current_pipette.flow_rate.dispense = flow_rate_beads
        current_pipette.flow_rate.blow_out = 300

    def etoh_flow_rates(current_pipette):
        if (current_pipette.name == 'p300_multi_gen2' or
           current_pipette.name == 'p300_single_gen2'):
            current_pipette.flow_rate.aspirate = 92.86
            current_pipette.flow_rate.dispense = 92.86
            current_pipette.flow_rate.blow_out = 300

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

    named_tips = {}

    def name_the_tips(tip_box, name_list, well_list):
        for name in name_list:
            if name != 'current_tip':
                if name not in named_tips.keys():
                    named_tips[name] = []
        for name, well in zip(name_list, well_list):
            if name != 'current_tip':
                named_tips[name].append(tip_box[well])
            else:
                named_tips[name] = tip_box[well]

    def capture_current_starting_tip():
        for index, box in enumerate(tips300):
            if box.next_tip() is not None:
                current_starting_tip = box.next_tip()
                name_the_tips(tips300[index], ['current_tip'], [
                 current_starting_tip.well_name])
                return (tips300[index], current_starting_tip.well_name)
                break

    ctx.delay(seconds=10)
    pause_attention("""
    Set up for bead cleanup steps:

    reagent reservoir in deck slot 4:
    col 1 - beads
    col 2 - 80 percent ethanol
    col 3 - 80 percent ethanol
    col 5 - water
    col 11 - liquid waste
    col 12 - liquid waste

    PCR1 plate on Magnetic Module
    Magnetic Module in deck slot 3

    Clean plate (PCR2) in deck slot 1

    p300 tips in slots 5,6,7,8,10
    """)
    reagent_reservoir = ctx.load_labware(
     labware_reservoir, '4', 'Reagent Reservoir')
    [beads, etoh_1, etoh_2, water, waste_1, waste_2] = [
     reagent_reservoir.wells_by_name()[well] for well in [
      'A1', 'A2', 'A3', 'A5', 'A12', 'A11']]
    mag = ctx.load_module('magnetic module gen2', '3')
    mag.disengage()
    mag_plate = mag.load_labware(labware_pcr_plate_1, 'PCR1 Mag Plate')

    ctx.comment("""
    PCR1 plate on Magnetic Module:
    containing samples arranged in columns of 8
    up to 96 samples total
    {} samples in this run
    """.format(str(sample_count)))
    num_cols = math.ceil(sample_count / 8)

    ctx.comment("""
    Clean plate (PCR2 plate) in deck slot 1
    """)
    pcr2_plate = ctx.load_labware(
     labware_pcr_plate_2, '1', 'PCR2 Plate')

    ctx.comment("""
    mix beads before each aspiration 2X 100 ul
    transfer 36 ul beads to each PCR1 column
    mix after 6X 50 ul
    wait, engage

    liquid handling method for beads:
    slow flow rate for aspiration and dispense
    wait for liquid to finish moving after aspiration and dispense
    withdraw tip slowly from liquid
    blowout at top of destination well
    touch tip
    """)
    custom_flow_rates(p300m)
    for column in mag_plate.columns()[:num_cols]:
        p300m.pick_up_tip()
        for rep in range(2):
            mix_with_delay(
             p300m, 100, beads.bottom(clearance_reservoir), delay_beads)
        aspirate_with_delay(
         p300m, 36, beads.bottom(clearance_reservoir), delay_beads)
        slow_tip_withdrawal(p300m, beads)
        dispense_with_delay(p300m, 36, column[0].bottom(3), delay_beads)
        for repeat in range(6):
            mix_with_delay(p300m, 50, column[0].bottom(3), delay_beads)
        slow_tip_withdrawal(p300m, column[0])
        p300m.blow_out(column[0].top())
        p300m.touch_tip(radius=0.75, v_offset=-2, speed=20)
        p300m.drop_tip()
    ctx.delay(minutes=2)
    mag.engage(height=engage_height)
    ctx.delay(minutes=engage_time)

    ctx.comment("""
        remove sup to reservoir col 12
        with tips to side to avoid bead pellet
        park tips

        two repeats:
        add EtOH dispensing 3 mm above top
        use parked tips to remove sup to col 11

        dry beads

        liquid handling method for ethanol:
        pre-wet tips (to saturate air inside tip)
        15 ul air gap after aspiration (to avoid drips)
        repeated delayed blowout (for complete dispense)
        """)
    for index, column in enumerate(mag_plate.columns()[:num_cols]):
        capture_current_starting_tip()
        name_the_tips(capture_current_starting_tip()[0], ['sup_tips'], [
         named_tips['current_tip'].well_name])
        p300m.pick_up_tip()
        if index % 2 != 1:
            # offset 1 mm to right for even columns to avoid bead pellet
            aspirate_location = column[0].bottom(
             clearance_bead_pellet).move(types.Point(x=1, y=0, z=0))
        else:
            # offset 1 mm to left for odd columns to avoid bead pellet
            aspirate_location = column[0].bottom(
             clearance_bead_pellet).move(types.Point(x=-1, y=0, z=0))
        aspirate_with_delay(p300m, 60, aspirate_location, delay_beads)
        slow_tip_withdrawal(p300m, column[0])
        dispense_with_delay(p300m, 60, waste_1.top(3), delay_beads)
        p300m.blow_out(waste_1.top(3))
        p300m.return_tip()
    for source in [etoh_1, etoh_2]:
        p300m.pick_up_tip()
        for column in mag_plate.columns()[:num_cols]:
            pre_wet(p300m, 150, source.bottom(clearance_reservoir))
            p300m.aspirate(80, source.bottom(clearance_reservoir))
            p300m.air_gap(20)
            p300m.dispense(100, column[0].top(3))
            for rep in range(3):
                if rep != 0:
                    p300m.aspirate(150, column[0].top(3))
                ctx.delay(seconds=1)
                p300m.blow_out(column[0].top(3))
        p300m.drop_tip()
        for index, column in enumerate(mag_plate.columns()[:num_cols]):
            p300m.pick_up_tip(named_tips['sup_tips'][index])
            if index % 2 != 1:
                # offset 1 mm to right for even columns to avoid bead pellet
                aspirate_location = column[0].bottom(
                 clearance_bead_pellet).move(types.Point(x=1, y=0, z=0))
            else:
                # offset 1 mm to left for odd columns to avoid bead pellet
                aspirate_location = column[0].bottom(
                 clearance_bead_pellet).move(types.Point(x=-1, y=0, z=0))
            p300m.aspirate(85, aspirate_location)
            p300m.air_gap(20)
            p300m.dispense(105, waste_2.top(3))
            for rep in range(3):
                if rep != 0:
                    p300m.aspirate(150, waste_2.top(3))
                ctx.delay(seconds=1)
                p300m.blow_out(waste_2.top(3))
            if source == etoh_1:
                p300m.return_tip()
            else:
                p300m.drop_tip()

    ctx.delay(minutes=dry_time)
    mag.disengage()
    ctx.comment("""
    add water and mix
    wait
    engage magnets
    transfer eluate to clean plate

    liquid handling method for beads:
    slow flow rate for aspiration and dispense
    wait for liquid to finish moving after aspiration and dispense
    withdraw tip slowly from liquid
    blowout at top of destination well
    touch tip
    """)
    for index, column in enumerate(mag_plate.columns()[:num_cols]):
        p300m.pick_up_tip()
        p300m.aspirate(43, water.bottom(clearance_reservoir))
        p300m.dispense(43, column[0].bottom(clearance_elution))
        for rep in range(10):
            mix_with_delay(
             p300m, 20, column[0].bottom(clearance_elution), delay_beads)
        slow_tip_withdrawal(p300m, column[0])
        p300m.blow_out(column[0].top())
        p300m.touch_tip(radius=0.75, v_offset=-2, speed=20)
        p300m.drop_tip()
    ctx.delay(minutes=2)
    mag.engage(height=engage_height)
    ctx.delay(minutes=engage_time)
    for index, column in enumerate(mag_plate.columns()[:num_cols]):
        p300m.pick_up_tip()
        if index % 2 != 1:
            # offset 1 mm to right for even columns to avoid bead pellet
            aspirate_location = column[0].bottom(
             clearance_elution).move(types.Point(x=1, y=0, z=0))
        else:
            # offset 1 mm to left for odd columns to avoid bead pellet
            aspirate_location = column[0].bottom(
             clearance_elution).move(types.Point(x=-1, y=0, z=0))
        p300m.aspirate(40, aspirate_location)
        p300m.dispense(
         40, pcr2_plate.columns()[index][0].bottom(clearance_elution))
        p300m.drop_tip()
    default_flow_rates(p300m)
