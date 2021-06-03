import math
from opentrons.protocol_api.labware import OutOfTipsError

metadata = {
    'protocolName': '''NEBNext Ultra II Directional RNA Library Prep Kit
    for Illumina with poly(A) selection: part 4 -
    PCR Enrichment and Bead Clean Up''',
    'author': 'Steve Plonk <protocols@opentrons.com>',
    'apiLevel': '2.9'
}


def run(ctx):

    # get parameter values from json above
    [sample_count, labware_tips300, labware_tips20, labware_pcr_plate,
     labware_reservoir, labware_tube_strip, clearance_sample_plate,
     clearance_reservoir, clearance_strip_tubes, clearance_bead_pellet,
     delay_beads, flow_rate_beads, engage_time, dry_time
     ] = get_values(  # noqa: F821
      'sample_count', 'labware_tips300', 'labware_tips20', 'labware_pcr_plate',
      'labware_reservoir', 'labware_tube_strip', 'clearance_sample_plate',
      'clearance_reservoir', 'clearance_strip_tubes', 'clearance_bead_pellet',
      'delay_beads', 'flow_rate_beads', 'engage_time', 'dry_time')

    ctx.set_rail_lights(True)
    if not 1 <= sample_count <= 48:
        raise Exception('Invalid number of samples (must be 1-48).')

    # tips, p20 multi gen2, p300 multi gen2
    tips20 = [ctx.load_labware(
     labware_tips20, str(slot)) for slot in [2, 5]]
    p20m = ctx.load_instrument(
        "p20_multi_gen2", 'left', tip_racks=tips20)
    tips300 = [ctx.load_labware(labware_tips300, str(slot)) for slot in [6, 9]]
    p300m = ctx.load_instrument(
        "p300_multi_gen2", 'right', tip_racks=tips300)

    """
    helper functions
    """

    def create_chunks(list_name, n):
        for i in range(0, len(list_name), n):
            yield list_name[i:i+n]

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

    def viscous_flow_rates(current_pipette):
        current_pipette.flow_rate.aspirate = flow_rate_beads
        current_pipette.flow_rate.dispense = flow_rate_beads
        current_pipette.flow_rate.blow_out = flow_rate_beads

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

    def reuse_tips(current_pipette, which_tips):
        current_pipette.reset_tipracks()
        current_pipette.starting_tip = named_tips[which_tips]

    named_tips = {}

    def name_the_tips(tip_box, name_list, well_list):
        for name, well in zip(
         name_list, well_list):
            named_tips[name] = tip_box[well]

    ctx.delay(seconds=10)
    pause_attention("""
    Set up for PCR Enrichment and Bead Clean Up:

    sample plate (from part 3) on deck slot 7
    (15 ul end-prepped, adaptor ligated cDNA with
    up to 48 samples arranged in columns of 8)

    Reagents in strip tubes on 4 degree temp module:
    column 1 - NEBNext Q5 Master Mix
    column 2 - index primer mix

    p20 tips in slot 2 and 5.
    """)

    ctx.comment("""
    reagent reservoir in deck slot 1:
    col 1 - beads
    col 2 - freshly prepared 80 percent ethanol
    col 4 - 0.1x TE
    col 12 - waste
    """)
    reagent_reservoir = ctx.load_labware(
     labware_reservoir, '1', 'Reagent Reservoir')
    [beads, etoh, te, waste] = [reagent_reservoir.wells_by_name()[
     well] for well in ['A1', 'A2', 'A4', 'A12']]

    ctx.comment("""
    mag plate on magnetic module
    """)
    mag = ctx.load_module('magnetic module gen2', '4')
    mag.disengage()
    mag_plate = mag.load_labware(labware_pcr_plate, 'Mag Plate')

    ctx.comment("""
    reagent block for tube strips on 4 degree temperature module
    """)
    temp = ctx.load_module('temperature module gen2', '3')
    reagent_block = temp.load_labware(labware_tube_strip, '4 Degree Block')
    [q5_mm, index_mx] = [
     reagent_block.columns_by_name()[str(name + 1)] for name in [*range(2)]]

    ctx.comment("""
    Sample plate in deck slot 7:
    containing 15 ul double-stranded cDNA
    samples arranged in columns of 8
    up to 48 samples total
    {} samples in this run
    """.format(str(sample_count)))
    num_cols = math.ceil(sample_count / 8)
    sample_plate = ctx.load_labware(
     labware_pcr_plate, '7', 'cDNA Sample Plate')

    ctx.comment("""
    elution plate in deck slot 8
    """)
    elution_plate = ctx.load_labware(labware_pcr_plate, '8', 'Elution Plate')

    ctx.comment("""
    PCR enrichment:
    add NEBNext Q5 Master Mix and mix
    add index primer mix
    mix

    liquid handling method for master mix:
    slow flow rate for aspiration and dispense
    wait for liquid to finish moving after aspiration and dispense
    withdraw tip slowly from liquid
    """)
    viscous_flow_rates(p300m)
    for column in sample_plate.columns()[:num_cols]:
        p300m.pick_up_tip()
        aspirate_with_delay(p300m, 25, q5_mm[0].bottom(
         clearance_strip_tubes), delay_beads)
        slow_tip_withdrawal(p300m, q5_mm[0])
        dispense_with_delay(p300m, 25, column[0].bottom(
         clearance_sample_plate), delay_beads)
        for repeat in range(10):
            mix_with_delay(p300m, 20, column[0].bottom(
             clearance_sample_plate), delay_beads)
        slow_tip_withdrawal(p300m, column[0])
        p300m.drop_tip()
    default_flow_rates(p300m)
    p20m.transfer(
     10, index_mx[0].bottom(clearance_strip_tubes), [column[0].bottom(
      clearance_sample_plate) for column in sample_plate.columns()[
      :num_cols]], mix_after=(10, 20), new_tip='always')

    pause_attention("""
        pausing for off-deck steps

        first, spin the plate
        then, on thermocycler-

        30 sec 98 C

        8-16 cycles:
        10 sec 98 C
        75 sec 65 C

        5 min 65 C
        hold 4 C

        return the plate to the magnetic module for bead clean up

        set up for bead clean up:
        replenish the tip boxes
        add reagents to reservoir in deck slot 1:
        col 1 - beads
        col 2 - freshly prepared 80 percent ethanol
        col 4 - 0.1x TE
        col 12 - waste
        place elution plate in deck slot 8
        resume
        """)
    p300m.reset_tipracks()
    p20m.reset_tipracks()

    ctx.comment("""
    bead clean up:

    add beads, mix, wait

    liquid handling method for beads:
    slow flow rate for aspiration and dispense
    wait for liquid to finish moving after aspiration and dispense
    withdraw tip slowly from liquid
    """)
    viscous_flow_rates(p300m)
    for column in mag_plate.columns()[:num_cols]:
        p300m.pick_up_tip()
        aspirate_with_delay(p300m, 45, beads.bottom(
         clearance_reservoir), delay_beads)
        slow_tip_withdrawal(p300m, beads)
        dispense_with_delay(p300m, 45, column[0].bottom(
         clearance_sample_plate), delay_beads)
        for repeat in range(10):
            mix_with_delay(p300m, 50, column[0].bottom(
             clearance_sample_plate), delay_beads)
        p300m.drop_tip()
    default_flow_rates(p300m)
    ctx.delay(minutes=5)
    pause_attention("""
    spin and return the plate
    resume
    """)
    mag.engage()
    ctx.delay(minutes=engage_time)
    ctx.comment("""
    remove sup

    add 80 percent ethanol
    wait 30 sec
    remove sup
    repeat

    liquid handling method for ethanol:
    prewet tips
    15 ul air gap
    dispense from top
    repeated delayed blowout
    increased blow out flow rate
    """)
    for column in mag_plate.columns()[:num_cols]:
        pick_up_or_refill(p300m)
        p300m.transfer(95, column[0].bottom(
         clearance_bead_pellet), waste.top(), new_tip='never')
        p300m.drop_tip()
    etoh_flow_rates(p300m)
    for rep in range(2):
        pick_up_or_refill(p300m)
        for column in mag_plate.columns()[:num_cols]:
            pre_wet(p300m, 150, etoh.bottom(clearance_reservoir))
            p300m.aspirate(150, etoh.bottom(clearance_reservoir))
            p300m.air_gap(15)
            p300m.dispense(165, column[0].top())
            for rep in range(3):
                if rep > 0:
                    p300m.aspirate(150, column[0].top())
                ctx.delay(seconds=1)
                p300m.blow_out(column[0].top())
        p300m.drop_tip()
        ctx.delay(seconds=30)
        for column in mag_plate.columns()[:num_cols]:
            pick_up_or_refill(p300m)
            p300m.aspirate(150, column[0].bottom(clearance_bead_pellet))
            p300m.air_gap(15)
            p300m.dispense(165, waste.top())
            for rep in range(3):
                if rep > 0:
                    p300m.aspirate(150, waste.top())
                ctx.delay(seconds=1)
                p300m.blow_out(waste.top())
            p300m.drop_tip()
    default_flow_rates(p300m)
    pause_attention("""
    spin and return the plate
    resume
    """)
    mag.engage()
    pause_attention("""
    manually remove last traces of ethanol with 10 ul tip
    resume
    """)
    ctx.comment("""
    air dry beads
    """)
    ctx.delay(minutes=dry_time)
    mag.disengage()
    ctx.comment("""
    add TE and mix
    """)
    for column in mag_plate.columns()[:num_cols]:
        pick_up_or_refill(p300m)
        p300m.transfer(
         23, te.bottom(clearance_reservoir), column[0].bottom(
          clearance_sample_plate), mix_after=(10, 15), new_tip='never')
        p300m.drop_tip()
    pause_attention("""
    spin and return the plate
    resume
    """)
    ctx.delay(minutes=2)
    mag.engage()
    ctx.delay(minutes=engage_time)
    ctx.comment("""
    transfer to elution plate
    """)
    for index, column in enumerate(mag_plate.columns()[:num_cols]):
        pick_up_or_refill(p20m)
        p20m.transfer(
         20, column[0].bottom(clearance_bead_pellet), elution_plate.columns()[
          index][0].bottom(clearance_sample_plate), new_tip='never')
        p20m.drop_tip()
