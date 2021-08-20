import csv

metadata = {
    'title': 'Cherrypicking',
    'author': 'Steve Plonk',
    'apiLevel': '2.10'
}


def run(ctx):

    [gantryspeed, flowrate, tip_touch, plate_count, labware_plate,
     uploaded_csv] = get_values(  # noqa: F821
        "gantryspeed", "flowrate", "tip_touch", "plate_count",
        "labware_plate", "uploaded_csv")

    ctx.set_rail_lights(True)
    ctx.delay(seconds=10)

    if flowrate < 0.25 or flowrate > 3:
        raise Exception("""
        Aspirate and dispense rate param value must be between 0.25 and 3.""")

    if gantryspeed < 100 or gantryspeed > 400:
        raise Exception(
         """Gantry speed param value must be between 100 and 400 mm/sec.""")

    # p300 single, tips
    tip_slots = [7, 8, 9]
    tips300 = [ctx.load_labware(
     'opentrons_96_filtertiprack_200ul', str(slot)) for slot in tip_slots]
    p300s = ctx.load_instrument("p300_single_gen2", 'right', tip_racks=tips300)

    # plates
    [*plates] = [ctx.load_labware(
     labware_plate, str(slot), 'Plate') for slot in [
     1, 2, 3, 4, 5, 6][:plate_count]]

    # list each csv input line (represents a transfer) as dict
    picks = [line for line in csv.DictReader(uploaded_csv.splitlines())]

    if int(picks[0]['tip_box_location']) not in tip_slots:
        raise Exception(
         """Starting tip must be located in deck slots {}""".format(
          str(tip_slots)))

    # starting tip
    for box in tips300:
        if int(box.parent) == int(picks[0]['tip_box_location']):
            p300s.starting_tip = box[picks[0]['Starting_tip']]

    # perform transfers in csv order
    p300s.default_speed = gantryspeed
    for plate in plates:
        for pick in picks:
            if pick['Source_location'] == plate.parent:
                vol = int(pick['transfer_volume'])
                p300s.pick_up_tip()
                p300s.aspirate(
                 vol, plate[pick['source_well']].bottom(1), rate=flowrate)
                p300s.air_gap(5)
                for plt in plates:
                    if pick['Destination_location'] == plt.parent:
                        p300s.dispense(
                         vol+5, plt[pick['destination_well']].bottom(1),
                         rate=flowrate)
                        if tip_touch:
                            p300s.touch_tip(radius=0.75, v_offset=-2, speed=20)
                p300s.drop_tip()
