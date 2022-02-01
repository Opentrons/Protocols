import json
import os

# metadata
metadata = {
    'protocolName': 'Manual Cleave',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.11'
}


def run(ctx):

    [plate_1_rows, plate_1_cols, plate_2_rows, plate_2_cols, plate_3_rows,
     plate_3_cols, plate_4_rows, plate_4_cols, reagent_type, m300_mount,
     tip_track] = get_values(  # noqa: F821
        'plate_1_rows', 'plate_1_cols', 'plate_2_rows', 'plate_2_cols',
        'plate_3_rows', 'plate_3_cols', 'plate_4_rows', 'plate_4_cols',
        'reagent_type', 'm300_mount', 'tip_track')

    # load labware
    racks = [
        ctx.load_labware('custom_96_tuberack_500ul', f'{slot}', f'plate {i+1}')
        for i, slot in enumerate(['1', '2', '4', '5'])]
    reagent_map = {
        'EDA': {
            'slot': '3',
            'volume': 200,
            'flow-rate-asp': 50,
            'flow-rate-disp': 50,
            'blow-out': False
        },
        'ACN': {
            'slot': '6',
            'volume': 200,
            'flow-rate-asp': 50,
            'flow-rate-disp': 50,
            'blow-out': False
        }
    }
    reagent = ctx.load_labware(
        'nest_1_reservoir_195ml', reagent_map[reagent_type]['slot'],
        reagent_type).wells()[0]
    tips300 = [
        ctx.load_labware('opentrons_96_tiprack_300ul', slot,
                         '300ul tiprack')
        for slot in ['7', '8', '10', '11']]

    def all_tips_full():
        for rack in tips300:
            for well in rack.wells():
                well.has_tip = True

    folder_path = '/data/manual_cleave'
    tip_file_path = folder_path + '/tip_log.json'
    if tip_track and not ctx.is_simulating():
        if os.path.isfile(tip_file_path):
            with open(tip_file_path) as json_file:
                tip_data = json.load(json_file)
                for slot in tip_data.keys():
                    for well, tip_bool in tip_data[slot].items():
                        ctx.loaded_labwares[int(slot)].wells_by_name()[
                            well].has_tip = tip_bool
        else:
            all_tips_full()
    else:
        all_tips_full()

    # load pipette
    m300 = ctx.load_instrument(
        'p300_multi_gen2', m300_mount, tip_racks=tips300)

    # samples and reagents
    def slide_window(num_tips, col):
        num_slides = 9 - num_tips
        for slide in range(num_slides):
            window_start_index = 8 + -1*num_tips - slide
            window = col[window_start_index:(window_start_index+num_tips)]
            window_full = True
            for tip in window:
                if not tip.has_tip:
                    window_full = False
            if window_full:
                return window[0]
        return False

    def scan_racks(num_tips):
        all_columns = [col for rack in tips300 for col in rack.columns()]
        for col in all_columns:
            pick_up_loc = slide_window(num_tips, col)
            if pick_up_loc:
                return pick_up_loc
        return False

    def pick_up(num_tips=8):
        if not 1 <= num_tips <= 8:
            raise Exception(f'INVALID NUMBER OF TIPS: {num_tips}.')
        pip = m300
        scan_result = scan_racks(num_tips)
        if scan_racks(num_tips):
            pip.pick_up_tip(scan_result)
        else:
            ctx.pause('REFILL TIPRACKS BEFORE RESUMING.')
            [rack.reset() for rack in tips300]
            scan_result = scan_racks(num_tips)
            pip.pick_up_tip(scan_result)

    def check_rows(rows):
        if not 0 <= rows <= 8:
            raise Exception(f'Invalid number of rows: {rows}')

    def check_cols(cols):
        if not 0 <= cols <= 12:
            raise Exception(f'Invalid number of columns: {cols}')

    m300.flow_rate.aspirate = reagent_map[reagent_type]['flow-rate-asp']
    m300.flow_rate.dispense = reagent_map[reagent_type]['flow-rate-disp']

    for num_rows, num_cols, plate in zip(
            [plate_1_rows, plate_2_rows, plate_3_rows, plate_1_rows],
            [plate_1_cols, plate_2_cols, plate_3_cols, plate_4_cols],
            racks):
        if num_cols == 0 or num_rows == 0:
            continue
        check_rows(num_rows)
        check_cols(num_cols)
        pick_up(num_rows)

        for col in plate.rows()[0][:num_cols]:
            m300.transfer(
                reagent_map[reagent_type]['volume'], reagent, col.top(),
                blow_out=reagent_map[reagent_type]['blow-out'],
                new_tip='never')
        m300.drop_tip()

    # track final used tip
    tip_data = {
        str(rack.parent):
            {well.display_name.split(' ')[0]: well.has_tip
             for well in rack.wells()}
        for rack in tips300
    }
    if tip_track and not ctx.is_simulating():
        if not os.path.isdir(folder_path):
            os.mkdir(folder_path)
        with open(tip_file_path, 'w') as outfile:
            json.dump(tip_data, outfile)
