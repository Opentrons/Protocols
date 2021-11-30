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

    dividers = []
    for row in list_of_rows:
        dividers.append(row[slot_num_source])

    # transfer target cell
    sections = [list(j) for i, j in groupby(dividers)]

    for i, _ in enumerate(list_of_rows[:len(sections[0])]):
        source = all_labware[int(_[slot_num_source])-1]
        source_well = _[tube_source]
        dest = all_labware[int(_[slot_num_dest])-1]
        dest_well = _[tube_dest]
        transfer_vol = float(_[vol])
        pip = p20 if transfer_vol < 100 else p1000
        if i == 0:
            pip.pick_up_tip()

        if pip.current_volume < transfer_vol-100:
            if pip.current_volume > 0:
                pip.dispense(pip.current_volume,
                             source.wells_by_name()[source_well])
            pip.aspirate(pip.max_volume, source.wells_by_name()[source_well])

        pip.dispense(transfer_vol, dest.wells_by_name()[dest_well].top())
        pip.blow_out()

        if i == len(sections[0])-1:
            pip.dispense(pip.current_volume,
                         source.wells_by_name()[source_well])
            pip.drop_tip()

    ctx.comment('\n\n\n')

    for _ in list_of_rows[len(sections[0]):]:
        source = all_labware[int(_[slot_num_source])-1]
        source_well = _[tube_source]
        dest = all_labware[int(_[slot_num_dest])-1]
        dest_well = _[tube_dest]
        transfer_vol = float(_[vol])
        pip = p20 if transfer_vol < 100 else p1000

        pip.pick_up_tip()
        pip.transfer(transfer_vol,
                     source.wells_by_name()[source_well],
                     dest.wells_by_name()[dest_well].top(),
                     new_tip='never',
                     mix_after=(2, 0.6*transfer_vol if 0.6*transfer_vol <
                                pip.max_volume else pip.max_volume),
                     blow_out=True,
                     blowout_location='destination well'
                     )

        pip.drop_tip()
