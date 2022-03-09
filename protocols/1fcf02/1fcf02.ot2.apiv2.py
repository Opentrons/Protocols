import math
from opentrons import protocol_api

metadata = {
    'protocolName': 'Chemical Denaturation with CSV Input',
    'author': 'Rami Farawi <rami.farawi@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.11'
}


def run(ctx):

    [csv1_urea,
     csv2_urea,
     csv3_urea,
     csv1_buff,
     csv2_buff,
     csv3_buff,
     csv1_samp,
     csv2_samp,
     csv3_samp,
     start_urea_vol,
     start_buff_vol,
     p20_mount,
     p300_mount] = get_values(  # noqa: F821
             "csv1_urea",
             "csv2_urea",
             "csv3_urea",
             "csv1_buff",
             "csv2_buff",
             "csv3_buff",
             "csv1_samp",
             "csv2_samp",
             "csv3_samp",
             "start_urea_vol",
             "start_buff_vol",
             "p20_mount",
             "p300_mount")

    # load labware
    plates = [ctx.load_labware('greiner_384_wellplate_138ul', slot)
              for slot in ['1', '2', '3']]
    sample_rack = ctx.load_labware('opentrons_24_tuberack_eppendorf_2ml_safelock_snapcap', '4')  # noqa: E501
    reagent_rack = ctx.load_labware('opentrons_10_tuberack_falcon_4x50ml_6x15ml_conical', '5')  # noqa: E501
    tiprack20 = [ctx.load_labware('opentrons_96_tiprack_20ul', slot)
                 for slot in ['6', '7', '8']]
    tiprack300 = [ctx.load_labware('opentrons_96_tiprack_300ul', slot)
                  for slot in ['9', '10', '11']]

    # load instrument
    p20 = ctx.load_instrument('p20_single_gen2', p20_mount,
                              tip_racks=tiprack20)
    p300 = ctx.load_instrument('p300_single_gen2',
                               p300_mount, tip_racks=tiprack300)

    # declare any variables, plate mapping, any pre-transfer step functions

    all_csvs = [
                csv1_urea,
                csv2_urea,
                csv3_urea,
                csv1_buff,
                csv2_buff,
                csv3_buff,
                csv1_samp,
                csv2_samp,
                csv3_samp
                ]

    all_csv_rows = []
    for csv in all_csvs:
        if ',' in csv:
            csv_rows = [[val.strip() for val in line.split(',')[1:]]
                        for line in csv.splitlines()
                        if line.split(',')[0].strip()][1:]
            all_csv_rows.append(csv_rows)

        elif ';' in csv:
            csv_rows = [[val.strip() for val in line.split(';')[1:]]
                        for line in csv.splitlines()
                        if line.split(';')[0].strip()][1:]

            all_csv_rows.append(csv_rows)

    urea_csvs = all_csv_rows[:3]
    buffer_csvs = all_csv_rows[3:6]
    sample_csvs = all_csv_rows[6:9]
    urea = reagent_rack.wells_by_name()['A3']
    buffer = reagent_rack.wells_by_name()['B3']

    # liquid height tracking
    v_naught_urea, v_naught_buffer = start_urea_vol*1000, start_buff_vol*1000
    radius = reagent_rack.wells()[0].diameter/2
    h_naught_urea, h_naught_buffer = 0.8*v_naught_urea/(math.pi*radius**2), 0.8*v_naught_buffer/(math.pi*radius**2)  # noqa: E501
    h1, h2 = h_naught_urea, h_naught_buffer

    def adjust_height(tube, vol):
        nonlocal h1
        nonlocal h2
        dh = vol/(math.pi*radius**2)
        if tube == 1:
            h1 -= dh
        else:
            h2 -= dh
        if h1 < 20:
            h1 = 1
        if h2 < 20:
            h2 = 1

    def pick_up(pip):
        try:
            pip.pick_up_tip()
        except protocol_api.labware.OutOfTipsError:
            ctx.pause("Replace empty tip racks")
            pip.reset_tipracks()
            pip.pick_up_tip()

    # protocol
    ctx.comment('\n\n\nADDING UREA\n')
    for csv, plate in zip(urea_csvs, plates):
        for i, row in enumerate(csv):
            for vol, well in zip(row, plate.rows()[i]):
                if vol == 'x':
                    continue
                vol = int(vol)
                pip = p300 if vol > 20 else p20
                if not pip.has_tip:
                    pip.pick_up_tip()
                pip.aspirate(vol, urea.bottom(h1))
                pip.dispense(vol, well)
                pip.blow_out()
                pip.touch_tip()
                adjust_height(1, vol)
            ctx.comment('\n')
    if p300.has_tip:
        p300.drop_tip()
    if p20.has_tip:
        p20.drop_tip()

    ctx.comment('\n\n\nADDING BUFFER\n')
    for csv, plate in zip(buffer_csvs, plates):
        for i, row in enumerate(csv):
            for vol, well in zip(row, plate.rows()[i]):
                if vol == 'x':
                    continue
                vol = int(vol)
                pip = p300 if vol > 20 else p20
                if not pip.has_tip:
                    pip.pick_up_tip()
                pip.aspirate(vol, buffer.bottom(h2))
                pip.dispense(vol, well.bottom(z=5))
                pip.blow_out()
                pip.touch_tip()
                adjust_height(2, vol)
            ctx.comment('\n')
    if p300.has_tip:
        p300.drop_tip()
    if p20.has_tip:
        p20.drop_tip()

    ctx.comment('\n\n\nADDING SAMPLE\n')
    for csv, plate in zip(sample_csvs, plates):
        for i, row in enumerate(csv):
            for vol_well, well in zip(row, plate.rows()[i]):
                if vol_well.lower() == 'x':
                    continue
                left_and_right = vol_well.split('/')
                left = left_and_right[0]
                right = left_and_right[1]
                if left.lower() == 'x':
                    continue
                else:
                    source = sample_rack.wells_by_name()[right]
                vol = int(left)
                pip = p300 if vol > 20 else p20
                pick_up(pip)
                pip.aspirate(vol, source)
                pip.dispense(vol, well)
                pip.mix(3, 20, well)
                pip.blow_out()
                pip.touch_tip()
                pip.drop_tip()
            ctx.comment('\n')
