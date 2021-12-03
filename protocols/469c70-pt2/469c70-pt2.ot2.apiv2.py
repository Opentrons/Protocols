import math
from itertools import groupby

metadata = {
    'protocolName': 'Fresh Spiking with CSV',
    'author': 'Rami Farawi <rami.farawi@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.11'
}


def run(ctx):

    [csv, p20_mount, p1000_mount] = get_values(  # noqa: F821
        "csv", "p20_mount", "p1000_mount")

    # load labware
    final_rack1 = ctx.load_labware(
                    'opentrons_24_tuberack_eppendorf_2ml_safelock_snapcap',
                    '2',
                    label='FINAL RACK 1')
    final_rack2 = ctx.load_labware(
                    'opentrons_24_tuberack_eppendorf_2ml_safelock_snapcap',
                    '4',
                    label='FINAL RACK 2')

    matrix_rack = ctx.load_labware(
                    'opentrons_15_tuberack_falcon_15ml_conical', '3',
                    label='MATRIX RACK')
    analyte_rack = ctx.load_labware(
        'opentrons_24_tuberack_eppendorf_2ml_safelock_snapcap', '1',
        label='ANALYTE RACK')

    tiprack20 = [ctx.load_labware('opentrons_96_tiprack_20ul', slot)
                 for slot in ['5']]
    tiprack1000 = [ctx.load_labware('opentrons_96_tiprack_1000ul', slot)
                   for slot in ['8']]
    # load instrument
    p20 = ctx.load_instrument('p20_single_gen2',
                              p20_mount, tip_racks=tiprack20)
    p1000 = ctx.load_instrument('p1000_single_gen2',
                                p1000_mount, tip_racks=tiprack1000)

    # protocol
    list_of_rows = [[val.strip() for val in line.split(',')]
                    for line in csv.splitlines()
                    if line.split(',')[0].strip()][1:]

    slot_num_source = 0
    tube_source = 1
    vol = 3
    slot_num_dest = 4
    tube_dest = 5
    all_labware = [analyte_rack,
                   final_rack1,
                   matrix_rack,
                   final_rack2]

    a1_v_naught = 0
    a2_v_naught = 0
    for row in list_of_rows:
        if row[slot_num_source] == "3":
            if row[tube_source] == "A1":
                a1_v_naught += float(row[vol])
            else:
                a2_v_naught += float(row[vol])

    # liquid height tracking
    v_naught1 = a1_v_naught
    v_naught2 = a2_v_naught
    radius = matrix_rack.wells()[0].diameter/2
    h_naught1 = v_naught1/(math.pi*radius**2)
    h_naught2 = v_naught2/(math.pi*radius**2)
    h1 = h_naught1
    h2 = h_naught2

    def adjust_height(vol, matrix_tube):
        nonlocal h1
        nonlocal h2
        dh = vol/(math.pi*radius**2)
        if matrix_tube == "A1":
            h1 -= dh
            if h1 < 20:
                h1 = 1
            else:
                return h1 - 20
        else:
            h2 -= dh
            if h2 < 20:
                h2 = 1
            else:
                return h2 - 20

    # divide betweeen first and second half of protocol based on slot num
    dividers = []
    for row in list_of_rows:
        dividers.append(row[slot_num_source])

    # transfer target cell
    sections = [list(j) for i, j in groupby(dividers)]

    for i, _ in enumerate(list_of_rows[:len(sections[0])]):

        # well nomenclature for easier use
        source = all_labware[int(_[slot_num_source])-1]
        source_well = _[tube_source]
        dest = all_labware[int(_[slot_num_dest])-1]
        dest_well = _[tube_dest]
        transfer_vol = float(_[vol])
        pip = p20 if transfer_vol < 100 else p1000

        # liquid height tracking between A1 and A2 on slot 3
        if _[slot_num_source] == "3":
            if source_well == "A1":
                asp_loc_z = h1
            elif source_well == "A2":
                asp_loc_z = h2

        if i == 0:
            pip.pick_up_tip()

        # aspirate if low on volume
        if pip.current_volume < transfer_vol-100:
            if pip.current_volume > 0:
                pip.dispense(pip.current_volume,
                             source.wells_by_name()[source_well])
            pip.aspirate(pip.max_volume,
                         source.wells_by_name()[source_well].bottom(asp_loc_z))

        pip.dispense(transfer_vol, dest.wells_by_name()[dest_well].top())

        # adjust liquid height
        if _[slot_num_source] == "3":
            adjust_height(transfer_vol, source_well)

        # get rid of final tip volume at end and drop tip
        if i == len(sections[0])-1:
            pip.dispense(pip.current_volume,
                         source.wells_by_name()[source_well])
            pip.drop_tip()

    ctx.comment('\n\n\n')

    for _ in list_of_rows[len(sections[0]):]:

        # well nomenclature for easier use
        source = all_labware[int(_[slot_num_source])-1]
        source_well = _[tube_source]
        dest = all_labware[int(_[slot_num_dest])-1]
        dest_well = _[tube_dest]
        transfer_vol = float(_[vol])
        pip = p20 if transfer_vol < 100 else p1000

        # dispense into top if visiting source and well multiple times
        # to avoid cross contam
        if transfer_vol > 20:
            pip.pick_up_tip()
            pip.transfer(transfer_vol,
                         source.wells_by_name()[source_well],
                         dest.wells_by_name()[dest_well].top(),
                         new_tip='never')
            pip.blow_out()

        # volumes too low to dispense from top so go into well
        else:
            pip.pick_up_tip()
            pip.transfer(transfer_vol,
                         source.wells_by_name()[source_well],
                         dest.wells_by_name()[dest_well],
                         new_tip='never')
            pip.blow_out()

        pip.mix(2, 0.6*transfer_vol if 0.6*transfer_vol <
                pip.max_volume else pip.max_volume,
                dest.wells_by_name()[dest_well])
        pip.drop_tip()
