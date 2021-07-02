import csv

metadata = {
    'protocolName': 'Cherrypicking Final',
    'author': 'Steve <protocols@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.9'
}


def run(ctx):

    [uploaded_csv] = get_values(  # noqa: F821
        "uploaded_csv")

    # lines from uploaded csv file
    [*csv_lines] = uploaded_csv.splitlines()
    csv_reader = csv.DictReader(csv_lines)

    # tips, p300 multi, p20 single, LB reservoir, source and destination plates
    tips300 = [ctx.load_labware(
     'opentrons_96_filtertiprack_200ul', str(slot)) for slot in [10, 11]]
    p300m = ctx.load_instrument("p300_multi_gen2", 'left', tip_racks=tips300)

    tips20 = [ctx.load_labware('opentrons_96_filtertiprack_20ul', '7')]
    p20s = ctx.load_instrument("p20_single_gen2", 'right', tip_racks=tips20)

    # set default flow rates for p20 to match PD tool default values
    p20s.flow_rate.aspirate = 3.78
    p20s.flow_rate.dispense = 3.78

    [lb, source, dest] = [ctx.load_labware(
     labware, str(slot), display_name) for labware, slot, display_name in zip(
     ['nest_1_reservoir_195ml', 'white_96well_plate_340ul',
      'tpp_96well_plate_340ul'
      ], [5, 8, 6], [
      'NEST 1 WELL RESERVOIR 195 ML', 'SOURCE', 'DESTINATION'])]

    # step 1: p300m transfer 198 ul LB to destination columns with same tips
    p300m.transfer(198, lb['A1'].bottom(3), [
     column[0].bottom(1.5) for column in dest.columns()])

    # step 2: p300m mix 10 columns of SOURCE 80 ul 5X
    for column in source.columns()[1:11]:
        p300m.pick_up_tip()
        p300m.mix(5, 80, column[0].bottom(1.5))
        p300m.drop_tip()

    # step 3: p20s 2 ul SOURCE A2, A11, 30 custom to DESTINATION top
    # step 4: p20s 2 ul SOURCE 30 custom, H2, H11 to DESTINATION bottom
    # top dispense of air gap volume to replicate PD tool behavior
    for line in csv_reader:
        p20s.pick_up_tip()
        p20s.aspirate(2, source.wells_by_name()[line['source well']].bottom(1))
        p20s.air_gap(2)
        p20s.dispense(2, dest.wells_by_name()[line['destination well']].top())
        p20s.dispense(
         2, dest.wells_by_name()[line['destination well']].bottom(0.5))
        p20s.mix(
         5, 5, dest.wells_by_name()[line['destination well']].bottom(0.5))
        p20s.drop_tip()

    # step 5: p300m mix columns of DESTINATION 80 ul 5X
    for column in dest.columns():
        p300m.pick_up_tip()
        p300m.mix(5, 80, column[0].bottom(1.5))
        p300m.drop_tip()
