from opentrons import types

metadata = {
    'protocolName': 'Functionalization of Electrodes',
    'author': 'Steve <protocols@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.9'
}


def run(ctx):

    [offset_end, clearance_bar, clearance_reservoir, clearance_small_well,
     clearance_bar_pvc, clearance_aqueous_conditioning
     ] = get_values(  # noqa: F821
        "offset_end", "clearance_bar", "clearance_reservoir",
        "clearance_small_well", "clearance_bar_pvc",
        "clearance_aqueous_conditioning")

    ctx.set_rail_lights(True)
    ctx.delay(seconds=10)

    # tips, p20 single
    tips20 = [ctx.load_labware(
     'opentrons_96_tiprack_20ul', str(slot)) for slot in [10, 11]]
    p20s = ctx.load_instrument("p20_single_gen2", 'right', tip_racks=tips20)

    # reagents
    reservoir = ctx.load_labware(
     "nest_12_reservoir_15ml", "3", "Reagent Reservoir")
    ag = reservoir['A1']
    pvc = [reservoir[well_name] for well_name in ['A2', 'A3', 'A4', 'A5']]
    reference_pvc = reservoir['A6']
    aqueous_conditioning = [
     reservoir[well_name] for well_name in ['A7', 'A8', 'A9', 'A10']]

    # custom 5 x 10 arrangement of 50 electrode boards
    arrangement = ctx.load_labware(
     "custom_board_5_by_10", "1", "5 x 10 Arrangement")

    # rows of small electrode wells
    small_electrode_wells = arrangement.rows()[0::2]

    # rows of reference electrode bars
    reference_electrode_bars = arrangement.rows()[1::2]

    # step 1- three deposits of 40 ul Ag/AgCl to each reference electrode bar
    for row in reference_electrode_bars:
        for bar in row:
            # end offset less than half the bar length
            if not 0 <= offset_end < bar.length / 2:
                raise Exception("""end offset value must be smaller than
                half the electrode bar length""")
            for offset in [-1*offset_end, 0, offset_end]:
                dispense_location = bar.bottom(
                 clearance_bar).move(types.Point(x=offset, y=0, z=0))
                p20s.transfer(
                 40, ag.bottom(clearance_reservoir), dispense_location)

    # step 2- overnight delay for solvent evaporation
    ctx.delay(minutes=960)
    ctx.pause("resume when ready to proceed with step 3")

    # steps 3 and 4- 10 uL PVC memb to each 1st small well, then 2nd, 3rd, 4th
    group = 4
    for position in range(group):
        p20s.pick_up_tip()
        for row in small_electrode_wells:
            for well in row[position::group]:
                p20s.aspirate(10, pvc[position].bottom(clearance_reservoir))
                p20s.air_gap(2)
                p20s.dispense(12, well.bottom(clearance_small_well))
        p20s.drop_tip()

    # step 5- 30 uL ref PVC memb on top of Ag/AgCl on reference electrode bar
    p20s.pick_up_tip()
    for row in reference_electrode_bars:
        for bar in row:
            for offset in [-1*offset_end, 0, offset_end]:
                dispense_location = bar.bottom(
                 clearance_bar_pvc).move(types.Point(x=offset, y=0, z=0))
                p20s.transfer(30, reference_pvc.bottom(
                 clearance_reservoir), dispense_location, air_gap=2,
                 new_tip='never')
    p20s.drop_tip()

    # step 6- one hour delay for solvent evaporation
    ctx.delay(minutes=60)

    # step 7- 30 uL aq cond soln to each 1st small well, then 2nd, 3rd, 4th
    for position in range(group):
        p20s.pick_up_tip()
        for row in small_electrode_wells:
            for well in row[position::group]:
                p20s.transfer(
                 30, aqueous_conditioning[position].bottom(
                  clearance_reservoir), well.bottom(
                  clearance_aqueous_conditioning), new_tip='never')
        p20s.drop_tip()
