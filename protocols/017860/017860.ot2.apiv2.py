from opentrons import protocol_api
import csv
import math

metadata = {
    'protocolName': 'CSV Plate Filling',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}


def get_values(*names):
    import json
    _all_values = json.loads("""{
                                  "20_ul_tiprack_lname":"opentrons_96_tiprack_20ul",
                                  "300_ul_tiprack_lname":"opentrons_96_tiprack_300ul"
                                  }
                                  """)
    return [_all_values[n] for n in names]


def run(ctx: protocol_api.ProtocolContext):
    # update the path to your transfer CSV on the robot
    transfer_info_csv_path = "data/csv/rr027-M9_singlesCheck.csv"

    # create custom labware
    # plate_name = 'NUNC-96-flat'
    plate_name = 'nunc_96_wellplate_400ul'
    # database.delete_container(plate_name)
    # if plate_name not in labware.list():
    #   labware.create(
    #   plate_name,
    #   grid=(12, 8),
    #   spacing=(9, 9),
    #   diameter=7,
    #   depth=10.8,
    #   volume=400
    #   )

    # labware
    plates = [ctx.load_labware(plate_name, str(slot+1)) for slot in range(6)]
    tuberack_15_50 = ctx.load_labware('opentrons-tuberack-15_50ml', '8')
    tuberacks_15 = [ctx.load_labware('opentrons-tuberack-15ml', slot)
                    for slot in ['9', '7']]
    tips_300 = ctx.load_labware('opentrons-tiprack-300ul', '11')
    tips_20 = ctx.load_labware('opentrons-tiprack-10ul', '10')
    tips_20 = [ctx.load_labware('opentrons_96_tiprack_20ul', '10')]
    tips_300 = [ctx.load_labware('opentrons_96_tiprack_300ul', '11')]

    # pipettes
    # p10 = (
    #   mount='left',
    #   tip_racks=[tips_10]
    #   )
    # p300 = instruments.P300_Single(
    #   mount='right',
    #   tip_racks=[tips_300]
    #   )
    p20 = ctx.load_instrument(
                              'p20_single_gen2',
                              'left',
                              tip_racks=[tips_20]
                              )
    p300 = ctx.load_instrument(
                              'p300_single_gen2',
                              'right',
                              tip_racks=[tips_300]
                              )

    p20.set_flow_rate(aspirate=100, dispense=1000)
    p300.set_flow_rate(aspirate=100, dispense=250)

    # set up list of all wells
    all_wells = [well for plate in plates for well in plate.wells()]

    # set up list of all source tubes
    # check volume of water necessary and change length of waters accordingly
    NUM_DRUGS = 31
    waters = [tube for tube in tuberack_15_50.wells('A3', length=3)]
    drugs1 = [tube for tube in [
        tuberack_15_50.wells('A1', length=NUM_DRUGS-15*2)]]
    drugs2 = [tube for rack in tuberacks_15 for tube in rack.wells()]
    # run through all of the full 15mL racks before going back
    # to tuberack_15_50
    # barcode dye is the last tube (C1) of the 15/50 rack
    drugs = drugs2 + drugs1

    # CSV parsing function

    def csv_to_list(file_path):
        new_list = []
        with open(file_path, 'r') as csvfile:
            new = csv.reader(csvfile)
            for row in new:
                new_list.append(row)
        new_list = new_list[1:]
        reordered = []
        for col in range(len(new_list[0])):
            temp = []
            for row in new_list:
                temp.append(row[col])
            reordered.append(temp)
        return reordered

    # well height and volume tracking function
    well_V_track = [0 for _ in range(len(plates)*96)]
    well_h_track = [-0.4 for _ in range(len(plates)*96)]
    well_r = 3.43
    pi = math.pi

    def well_height_track(well_ind, vol):
        global well_V_track
        global well_h_track
        global well_r

        dh = vol/(pi*(well_r**2))
        well_h_track[well_ind] += dh

    # water height and volume tracking function
    water = waters[0]
    num_waters = 3
    start_waters = 0
    water_V_track = 70000
    water_h_track = -16
    water_r_cyl = 13.5

    def water_height_track(vol):
        global water_V_track
        global water_h_track
        global water
        global num_waters
        global start_waters

        water_V_track -= vol
        # change and reset water tube if necessary
        if water_V_track < 500:
            num_waters -= 1
            if num_waters == 0:
                ctx.pause("Please replace two 50ml water tubes filled to "
                          "50ml line before resuming.")
                water = waters[0]
            else:
                start_waters += 1
                water = waters[start_waters]
            water_V_track = 70000
            water_h_track = -16

        dh = (0.70*vol)/(pi*(water_r_cyl**2))
        water_h_track -= dh

    # initialize volume and height trackers, assuming that reagents are filled
    # to 14ml line in standard 15ml tube
    drug_V_track = [14000 for _ in range(NUM_DRUGS)]
    drug_h_track = [-24 for _ in range(NUM_DRUGS)]
    drug_r_cyl = 7.52
    drug_r_cone = [7.52 for _ in range(NUM_DRUGS)]
    drug_h_cone = 21.35
    theta = math.atan(drug_r_cyl/drug_h_cone)
    tan = math.tan(theta)
    cone_vol = pi*(drug_r_cyl**2)*drug_h_cone/3

    def drug_height_track(drug_ind, vol):
        global drug_V_track
        global drug_h_track
        global drug_r_cone

        # check that there is sufficient drug left in the tube
        if drug_V_track[drug_ind] - vol < 100:
            ctx.pause("Please fill drug %d to the 14ml line and replace in "
                      "its proper well before resuming." % (drug_ind+1))
            drug_V_track[drug_ind] = 14000
            drug_h_track = -24

        # calculates height to aspirate from if in main cylinder of tube
        if drug_V_track[drug_ind] >= cone_vol:
            drug_V_track[drug_ind] -= vol
            dh = vol/(pi*(drug_r_cyl**2))
            drug_h_track[drug_ind] -= dh

        # calculates height to aspirate from if in cone at bottom of tube
        else:
            new_h = math.pow((drug_V_track[drug_ind]-vol)/(pi/3*(tan**2)), 1/3)
            dh = drug_h_track[drug_ind] - new_h
            drug_h_track[drug_ind] -= dh
            drug_V_track[drug_ind] -= vol
            drug_r_cone[drug_ind] = new_h*tan

    # parses through CSV for transfer data
    csv_info = csv_to_list(transfer_info_csv_path)
    csv_info.pop(0)

    # calculate number of deck fills and initialize counter
    num_wells = len(plates)*96
    num_deck_fills = math.ceil(len(csv_info[0])/num_wells)
    num_total_transfers = len(csv_info[0])

    # perform full deck transfer
    for fill in range(num_deck_fills):

        # define CSV indices that will receive transfer on this deck set
        block_ind = range(fill*num_wells, (fill+1)*num_wells)

        p300.pick_up_tip(tips_300.wells(0))
        p20.pick_up_tip(tips_20.wells(0))

        # set proper tube and height to aspirate from, and initialize volumes
        # and aspirate for distribution
        water_height_track(300)
        p300.aspirate(300, water.top(water_h_track))
        pip_300_v_track = 300

        water_height_track(10)
        p20.aspirate(10, water.top(water_h_track))
        pip_50_v_track = 10

        for i, (ind, well) in enumerate(zip(block_ind, all_wells)):
            if ind == num_total_transfers:
                break
            v = float(csv_info[0][ind])

            # choose pipette
            if v <= 10 and v > 0:
                # check volume in pipette
                if v > pip_50_v_track - 5:
                    p20.blow_out(water.top())
                    water_height_track(10)
                    p20.aspirate(10, water.top(water_h_track))
                    pip_50_v_track = 10

                # perform transfer
                well_height_track(i, v)
                p20.dispense(v, well.bottom(-0.4))
                pip_50_v_track -= v

            elif v > 10:
                if v > pip_300_v_track - 5:
                    p300.blow_out(water.top())
                    water_height_track(300)
                    p300.aspirate(300, water.top(water_h_track))
                    pip_300_v_track = 300

                # perform transfer
                well_height_track(i, v)
                p300.dispense(v, well.bottom(-0.4))
                pip_300_v_track -= v

                # touch tip here if necessary

        p300.drop_tip()
        p20.drop_tip()

        # start P20 at correct tip position
        p20.start_at_tip(tips_20.wells(1))

        # perform drugs transfer
        for drug_ind, drug in enumerate(drugs):
            # range of drug transfers always between 5 and 50ul
            p20.pick_up_tip()

            # initialize volumes and aspirate for distribution
            drug_height_track(drug_ind, 10)
            p20.aspirate(10, drug.top(drug_h_track[drug_ind]))
            pip_v_track = 10

            # loop and distribute drug in proper amounts
            for i, (ind, well) in enumerate(zip(block_ind, all_wells)):
                if ind == num_total_transfers:
                    break
                drug_transfers = csv_info[drug_ind+1]
                v = float(drug_transfers[ind])

                # only begin transfer process if volume is more than 0ul
                if v > 0:
                    # check if volume in pipette tip can accommodate transfer
                    if v > pip_v_track - 5:
                        p20.blow_out(drug.top())
                        drug_height_track(drug_ind, 10)
                        p20.aspirate(10, drug.top(drug_h_track[drug_ind]))
                        pip_v_track = 10

                    # perform transfer
                    print(well_h_track[i])
                    well_height_track(i, v)
                    p20.dispense(v, well.bottom(well_h_track[i]))
                    pip_v_track -= v

                    # touch tip if necessary
                    # drop1 = well.from_center(h=-0.2, theta=0, r=0)
                    # drop2 = well.from_center(h=1.5, theta=0, r=0)
                    # down = (well, drop1)
                    # up = (well, drop2)
                    # p10.move_to(up)
                    # p10.move_to(down)

            # return tip to corresponding well for future deck refills
            p20.drop_tip()

        if fill < num_deck_fills-1:
            ctx.pause("Please remove all sample plates from the deck and "
                      "replace tips in the first 33 wells of the tiprack "
                      "before resuming.")
            p300.reset()
            p20.reset()
