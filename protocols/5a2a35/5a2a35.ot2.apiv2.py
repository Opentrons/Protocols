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

    # starting tip
    for box in tips300:
        if int(box.parent) == starting_tip_slot:
            p300s.starting_tip = box[starting_tip_well]

    # list each csv input line (represents a transfer) as dict
    picks = [line for line in csv.DictReader(uploaded_csv.splitlines())]

    # perform transfers in order
    # source = plates[0].wells_by_name()['A1']
    # dest = plates[0].wells_by_name()['A1']
    # vol = 20
    for pick in picks:
        for plate in plates:
            if pick['Source_location'] == str(plate.parent):
                source = plate.wells_by_name()[pick['source_well']]
            elif pick['Destination_location'] == str(plate.parent):
                dest = plate.wells_by_name()[pick['destination_well']]
        vol = int(pick['transfer_volume'])
        p300s.pick_up_tip()
        p300s.aspirate(vol, source.bottom(1))
        p300s.air_gap(5)
        p300s.dispense(vol, dest.bottom(1))
        p300s.drop_tip()
