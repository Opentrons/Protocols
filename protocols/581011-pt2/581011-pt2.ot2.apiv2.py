"""Protocol."""
import math
from itertools import groupby

metadata = {
    'protocolName': 'Cherrypicking with Multi-Channel Pipette and CSV-Part 2',
    'author': 'Rami Farawi <rami.farawi@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.10'
}
def get_values(*names):
    import json
    _all_values = json.loads("""{"csv_samp":",1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24\\nA,x,A1/A1,A1/A1,A1/A1,A2/A2,A2/A2,A2/A2,A3/A3,A3/A3,A3/A3,x,A4/A1,A4/A1,A4/A1,A5/A1,A5/A1,A5/A1,A6/A1,A6/A1,A6/A1,0/A1,0/A1,0/A2,0/A3\\nB,x,A1/A1,A1/A1,A1/A1,A2/A2,A2/A2,A2/A2,A3/A3,A3/A3,A3/A3,x,A4/A1,A4/A1,A4/A1,A5/A1,A5/A1,A5/A1,A6/A1,A6/A1,A6/A1,0/A1,0/A1,0/A2,0/A3\\nC,x,A1/B1,A1/B1,A1/B1,A2/B2,A2/B2,A2/B2,A3/B3,A3/B3,A3/B3,x,A4/B1,A4/B1,A4/B1,A5/B1,A5/B1,A5/B1,A6/B1,A6/B1,A6/B1,0/B1,0/B1,0/B2,0/B3\\nD,x,A1/B1,A1/B1,A1/B1,A2/B2,A2/B2,A2/B2,A3/B3,A3/B3,A3/B3,x,A4/B1,A4/B1,A4/B1,A5/B1,A5/B1,A5/B1,A6/B1,A6/B1,A6/B1,0/B1,0/B1,0/B2,0/B3\\nE,x,A1/C1,A1/C1,A1/C1,A2/C2,A2/C2,A2/C2,A3/C3,A3/C3,A3/C3,x,A4/C1,A4/C1,A4/C1,A5/C1,A5/C1,A5/C1,A6/C1,A6/C1,A6/C1,0/C1,0/C1,0/C2,0/C3\\nF,x,A1/C1,A1/C1,A1/C1,A2/C2,A2/C2,A2/C2,A3/C3,A3/C3,A3/C3,x,A4/C1,A4/C1,A4/C1,A5/C1,A5/C1,A5/C1,A6/C1,A6/C1,A6/C1,0/C1,0/C1,0/C2,0/C3\\nG,x,A1/D1,A1/D1,A1/D1,A2/D2,A2/D2,A2/D2,A3/D3,A3/D3,A3/D3,x,A4/D1,A4/D1,A4/D1,A5/D1,A5/D1,A5/D1,A6/D1,A6/D1,A6/D1,0/D1,0/D1,0/D2,0/D3\\nH,x,A1/D1,A1/D1,A1/D1,A2/D2,A2/D2,A2/D2,A3/D3,A3/D3,A3/D3,x,A4/D1,A4/D1,A4/D1,A5/D1,A5/D1,A5/D1,A6/D1,A6/D1,A6/D1,0/D1,0/D1,0/D2,0/D3\\nI,x,A1/E1,A1/E1,A1/E1,A2/E2,A2/E2,A2/E2,A3/E3,A3/E3,A3/E3,x,A4/E1,A4/E1,A4/E1,A5/E1,A5/E1,A5/E1,A6/E1,A6/E1,A6/E1,0/E1,0/E1,0/E2,0/E3\\nJ,x,A1/E1,A1/E1,A1/E1,A2/E2,A2/E2,A2/E2,A3/E3,A3/E3,A3/E3,x,A4/E1,A4/E1,A4/E1,A5/E1,A5/E1,A5/E1,A6/E1,A6/E1,A6/E1,0/E1,0/E1,0/E2,0/E3\\nK,x,A1/F1,A1/F1,A1/F1,A2/F2,A2/F2,A2/F2,A3/F3,A3/F3,A3/F3,x,A4/F1,A4/F1,A4/F1,A5/F1,A5/F1,A5/F1,A6/F1,A6/F1,A6/F1,0/F1,0/F1,0/F2,0/F3\\nL,x,A1/F1,A1/F1,A1/F1,A2/F2,A2/F2,A2/F2,A3/F3,A3/F3,A3/F3,x,A4/F1,A4/F1,A4/F1,A5/F1,A5/F1,A5/F1,A6/F1,A6/F1,A6/F1,0/F1,0/F1,0/F2,0/F3\\nM,x,A1/0,A1/0,A1/0,A2/0,A2/0,A2/0,A3/0,A3/0,A3/0,x,A4/0,A4/0,A4/0,A5/0,A5/0,A5/0,A6/0,A6/0,A6/0,x,x,x,x\\nN,x,A1/0,A1/0,A1/0,A2/0,A2/0,A2/0,A3/0,A3/0,A3/0,x,A4/0,A4/0,A4/0,A5/0,A5/0,A5/0,A6/0,A6/0,A6/0,x,x,x,x\\nO,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x\\nP,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x","vol_effector_cell":40,"pre_mix":false,"mix_asp_height":1,"mix_disp_height":1,"premix_reps":3,"mix_vol":3,"mix_rate":1,"asp_height":1,"disp_height":1,"asp_rate":1,"disp_rate":1,"m300_mount":"left"}""")
    return [_all_values[n] for n in names]

def run(ctx):
    """Protocol."""
    [csv_samp, vol_effector_cell, pre_mix, mix_asp_height, mix_disp_height,
     premix_reps, mix_vol, mix_rate,
     asp_height, disp_height, asp_rate,
        disp_rate, m300_mount] = get_values(  # noqa: F821
        "csv_samp", "vol_effector_cell", "pre_mix",
        "mix_asp_height", "mix_disp_height", "premix_reps",
        "mix_vol", "mix_rate", "asp_height", "disp_height",
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

    # find the num channels per pickup
    letter_to_num = {'A': '1', 'B': '2', 'C': '3', 'D': '4',
                     'E': '5', 'F': '6', 'G': '7', 'H': '8'}
    effector_numbers = []

    for row in plate_map:
        for well in row:
            if '/' in well:
                elements = well.split('/')
                if elements[1] == '0' or elements[0] == '0':
                    continue
                else:
                    effector_numbers.append(int(letter_to_num[elements[1][0]]))

    max_effector_number = max(effector_numbers)
    num_channels_per_pickup = max_effector_number
    tips_ordered = [
        tip for rack in tiprack
        for row in rack.rows()[
            len(rack.rows())-num_channels_per_pickup::
            -1*num_channels_per_pickup]
        for tip in row]

    # pick up function
    tip_count = 0

    def pickup():
        nonlocal tip_count
        m300.pick_up_tip(tips_ordered[tip_count])
        tip_count += 1

    def check_volume(counter, tot_vol, chunk, source_well):
        if m300.current_volume < vol_effector_cell:
            if m300.current_volume > 0:
                m300.dispense(m300.current_volume, source_well)
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

    dispense_wells = [list(j) for i, j in groupby(effector_columns)]

    # transfer effector cell
    wells_by_row = [well for row in plate.rows() for well in row]
    for j, chunk in enumerate(dispense_wells):
        if 'x' in chunk or 'X' in chunk or chunk[0][0] == '0':
            if j > 0:
                start_well += 1
            continue
        pickup()
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
        if m300.current_volume > 0:
            m300.dispense(m300.current_volume,
                          source_well)
        m300.drop_tip()
        ctx.comment('\n\n')
