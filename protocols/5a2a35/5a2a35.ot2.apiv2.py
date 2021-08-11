import csv

metadata = {
    'title': 'Cherrypicking',
    'author': 'Steve Plonk',
    'apiLevel': '2.10'
}


def run(ctx):

    [starting_tip_slot, starting_tip_well, plate_count, labware_plate,
     uploaded_csv] = get_values(  # noqa: F821
        "starting_tip_slot", "starting_tip_well", "plate_count",
        "labware_plate", "uploaded_csv")

    ctx.set_rail_lights(True)
    ctx.delay(seconds=10)

    # p300 single, tips
    tip_slots = [7, 8, 9]
    if starting_tip_slot not in tip_slots:
        raise Exception(
         """Starting tip must be located in deck slots {}""".format(
          str(tip_slots)))
    tips300 = [ctx.load_labware(
     'opentrons_96_filtertiprack_200ul', str(slot)) for slot in tip_slots]
    p300s = ctx.load_instrument("p300_single_gen2", 'right', tip_racks=tips300)

    # plates
    [*plates] = [ctx.load_labware(
     labware_plate, str(slot), 'Plate') for slot in [
     1, 2, 3, 4, 5, 6][:plate_count]]

    # comment added to satisfy linter
    ctx.comment(
     """Elution plate labware loaded: {}.""".format(plates))

    # list loaded labware
    loaded_lbwr = ctx.loaded_labwares.values()

    # starting tip
    for lbwr in loaded_lbwr:
        if int(lbwr.parent) == starting_tip_slot:
            p300s.starting_tip = lbwr[starting_tip_well]

    # csv input
    picks = [line for line in csv.DictReader(uploaded_csv.splitlines())]

    for pick in picks:
        p300s.transfer(int(pick['transfer_volume']),
                       [lbwr.wells_by_name()[
                        pick['source_well']].bottom(1)
                        for lbwr in loaded_lbwr if str(
                            lbwr.parent) == pick['Source_location']],
                       [lbwr.wells_by_name()[
                        pick['destination_well']].bottom(1)
                        for lbwr in loaded_lbwr if str(
                            lbwr.parent) == pick['Destination_location']],
                       air_gap=5,
                       new_tip='always')
