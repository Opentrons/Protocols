def get_values(*names):
    import json
    _all_values = json.loads("""{"csv_samp":",1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24\\nA,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x\\nB,x,A1/A1,A1/A1,A1/A1,A2/A1,A2/A1,A2/A1,A3/A1,A3/A1,A3/A1,0/A1,0/A1,A4/A2,A4/A2,A4/A2,A5/A2,A5/A2,A5/A2,A6/A2,A6/A2,A6/A2,0/A2,0/A2,x\\nC,x,A1/A1,A1/A1,A1/A1,A2/A1,A2/A1,A2/A1,A3/A1,A3/A1,A3/A1,0/A1,0/A1,A4/A2,A4/A2,A4/A2,A5/A2,A5/A2,A5/A2,A6/A2,A6/A2,A6/A2,0/A2,0/A2,x\\nD,x,A1/B1,A1/B1,A1/B1,A2/B1,A2/B1,A2/B1,A3/B1,A3/B1,A3/B1,0/B1,0/B1,A4/B2,A4/B2,A4/B2,A5/B2,A5/B2,A5/B2,A6/B2,A6/B2,A6/B2,0/B2,0/B2,x\\nE,x,A1/B1,A1/B1,A1/B1,A2/B1,A2/B1,A2/B1,A3/B1,A3/B1,A3/B1,0/B1,0/B1,A4/B2,A4/B2,A4/B2,A5/B2,A5/B2,A5/B2,A6/B2,A6/B2,A6/B2,0/B2,0/B2,x\\nF,x,A1/C1,A1/C1,A1/C1,A2/C1,A2/C1,A2/C1,A3/C1,A3/C1,A3/C1,0/C1,0/C1,A4/C2,A4/C2,A4/C2,A5/C2,A5/C2,A5/C2,A6/C2,A6/C2,A6/C2,0/C3,0/C3,x\\nG,x,A1/C1,A1/C1,A1/C1,A2/C1,A2/C1,A2/C1,A3/C1,A3/C1,A3/C1,0/C1,0/C1,A4/C2,A4/C2,A4/C2,A5/C2,A5/C2,A5/C2,A6/C2,A6/C2,A6/C2,0/C3,0/C3,x\\nH,x,A1/D1,A1/D1,A1/D1,A2/D1,A2/D1,A2/D1,A3/D1,A3/D1,A3/D1,0/D1,0/D1,A4/0,A4/0,A4/0,A5/0,A5/0,A5/0,A6/0,A6/0,A6/0,x,x,x\\nI,x,A1/D1,A1/D1,A1/D1,A2/D1,A2/D1,A2/D1,A3/D1,A3/D1,A3/D1,0/D1,0/D1,A4/0,A4/0,A4/0,A5/0,A5/0,A5/0,A6/0,A6/0,A6/0,x,x,x\\nJ,x,A1/0,A1/0,A1/0,A2/0,A2/0,A2/0,A3/0,A3/0,A3/0,x,x,x,x,x,x,x,x,x,x,x,x,x,x\\nK,x,A1/0,A1/0,A1/0,A2/0,A2/0,A2/0,A3/0,A3/0,A3/0,x,x,x,x,x,x,x,x,x,x,x,x,x,x\\nL,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x\\nM,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x\\nN,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x\\nO,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x\\nP,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x\\n","vol_effector_cell":40,"pre_mix":false,"mix_asp_height":1,"mix_disp_height":1,"premix_reps":3,"mix_vol":3,"mix_rate":1,"disp_res_height":1,"asp_height":1,"disp_height":1,"asp_rate":1,"disp_rate":1,"m300_mount":"left"}""")
    return [_all_values[n] for n in names]

"""Protocol."""
import math
from itertools import groupby

metadata = {
    'protocolName': 'Cherrypicking with Multi-Channel Pipette and CSV-Part 2',
    'author': 'Rami Farawi <rami.farawi@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.10'
}


def run(ctx):
    """Protocol."""
    [csv_samp, vol_effector_cell, pre_mix, mix_asp_height, mix_disp_height,
     premix_reps, mix_vol, mix_rate, disp_res_height,
     asp_height, disp_height, asp_rate,
        disp_rate, m300_mount] = get_values(  # noqa: F821
        "csv_samp", "vol_effector_cell", "pre_mix",
        "mix_asp_height", "mix_disp_height", "premix_reps",
        "mix_vol", "mix_rate", "disp_res_height",
        "asp_height", "disp_height",
        "asp_rate", "disp_rate", "m300_mount")

    # load labware
    plate = ctx.load_labware('corning_384_wellplate_112ul_flat', '4')
    effector_plate = ctx.load_labware('nest_96_wellplate_2ml_deep', '5')
    tiprack = [ctx.load_labware('opentrons_96_filtertiprack_200ul', slot)
               for slot in ['6']]

    # load instrument
    m300 = ctx.load_instrument('p300_multi_gen2', m300_mount,
                               tip_racks=tiprack)

    m300.well_bottom_clearance.aspirate = asp_height
    m300.well_bottom_clearance.dispense = disp_height
    m300.flow_rate.aspirate = asp_rate*m300.flow_rate.aspirate
    m300.flow_rate.dispense = disp_rate*m300.flow_rate.dispense

    # plate map excluding 1st column and row
    if csv_samp[0] == ',':
        csv_samp = csv_samp[1:]

    plate_map = [[val.strip() for val in line.split(',')][1:]
                 for line in csv_samp.splitlines()
                 if line.split(',')[0].strip()][1:]

    # FIND NUMBER OF TIPS PER COLUMN
    letter_to_num = {'A': '1', 'B': '2', 'C': '3', 'D': '4',
                     'E': '5', 'F': '6', 'G': '7', 'H': '8'}
    num_tips_in_each_column = []

    for column in range(24):
        check_highest_letter = []
        for row in plate_map:
            well = row[column]

            if '/' in well:
                elements = well.split('/')
                if elements[1] == '0' or elements[0] == '0':
                    continue
                else:
                    check_highest_letter.append(int(
                        letter_to_num[elements[1][0]]))
        if len(check_highest_letter) > 0:
            num_tips_in_each_column.append(max(check_highest_letter))
        else:
            num_tips_in_each_column.append('x')

    # pick up function
    tip_count = 0

    def pickup(num_channels_per_pickup):
        nonlocal tip_count
        tips_ordered = [
            tip for rack in tiprack
            for row in rack.rows()[
                len(rack.rows())-num_channels_per_pickup::
                -1*num_channels_per_pickup]
            for tip in row]

        m300.pick_up_tip(tips_ordered[tip_count])
        tip_count += 1

    def check_volume(counter, tot_vol, chunk, source_well):
        if m300.current_volume < vol_effector_cell:
            if m300.current_volume > 0:
                m300.dispense(m300.current_volume,
                              source_well.bottom(disp_res_height))
            if counter != len(chunk)-1:
                if pre_mix:
                    mix_diff_height(source_well)
                m300.aspirate(tot_vol if tot_vol < 200 else
                              200-0.15*vol_effector_cell, source_well)

    def mix_diff_height(well):
        m300.flow_rate.aspirate = m300.flow_rate.aspirate/asp_rate
        m300.flow_rate.dispense = m300.flow_rate.dispense/disp_rate
        for rep in range(premix_reps):
            m300.aspirate(mix_vol,
                          well.bottom(
                           mix_asp_height),
                          rate=mix_rate)
            m300.dispense(mix_vol,
                          well.bottom(
                           mix_disp_height),
                          rate=mix_rate)
        m300.flow_rate.aspirate = asp_rate*m300.flow_rate.aspirate
        m300.flow_rate.dispense = disp_rate*m300.flow_rate.dispense

    # find start well
    start_well = 0
    for row in plate_map:
        for well in row:
            if '/' in well:
                break
            start_well += 1
        if '/' in well:
            break
    start_row = math.floor(start_well/24)

    # find effecor cell column
    effector_columns = []

    for well in plate_map[start_row]:
        if '/' in well:
            left_and_right = well.split('/')
            right = left_and_right[1]
            effector_columns.append(right)
        else:
            effector_columns.append(well)

    dispense_wells = [list(b) for a, b in groupby(effector_columns)]

    # transfer effector cell
    tip_col_ctr = 0
    wells_by_row = [well for row in plate.rows() for well in row]
    for j, chunk in enumerate(dispense_wells):
        # print(tip_col_ctr)

        if 'x' in chunk or 'X' in chunk or chunk[0][0] == '0':
            if j > 0:
                start_well += len(chunk)
                tip_col_ctr += len(chunk)
            else:
                tip_col_ctr += len(chunk)
            continue

        pickup(num_tips_in_each_column[tip_col_ctr])
        tot_vol = vol_effector_cell*len(chunk)*2+20
        for i, well in enumerate(chunk):
            source_well = effector_plate.wells_by_name()[str(chunk[0][0:2])]
            if vol_effector_cell >= 100:
                if pre_mix:
                    mix_diff_height(source_well)
                m300.aspirate(vol_effector_cell, source_well)
                m300.dispense(vol_effector_cell, wells_by_row[start_well])
                if pre_mix:
                    mix_diff_height(source_well)
                m300.aspirate(vol_effector_cell,
                              source_well)
                m300.dispense(vol_effector_cell, wells_by_row[start_well+24])
                start_well += 1
                tip_col_ctr += 1

            else:
                if m300.current_volume < vol_effector_cell:
                    if pre_mix:
                        mix_diff_height(source_well)
                    m300.aspirate(tot_vol if tot_vol < 200
                                  else 200-0.15*vol_effector_cell,
                                  source_well)

                # first row dispense
                m300.dispense(vol_effector_cell, wells_by_row[start_well])
                tot_vol -= vol_effector_cell
                check_volume(i, tot_vol, chunk, source_well)

                # second row dispense
                m300.dispense(vol_effector_cell,
                              wells_by_row[start_well+24])
                tot_vol -= vol_effector_cell
                check_volume(i, tot_vol, chunk, source_well)

                start_well += 1
                tip_col_ctr += 1
        if m300.current_volume > 0:
            m300.dispense(m300.current_volume,
                          source_well)
        m300.drop_tip()
        ctx.comment('\n\n')
