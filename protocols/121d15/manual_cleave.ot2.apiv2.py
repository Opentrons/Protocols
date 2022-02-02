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

    [occupied_well_csv1, occupied_well_csv2, occupied_well_csv3, reagent_type,
     m300_mount, p300_mount, tip_track] = get_values(  # noqa: F821
        'occupied_well_csv1', 'occupied_well_csv2', 'occupied_well_csv3',
        'reagent_type', 'm300_mount', 'p300_mount', 'tip_track')

    # load labware
    racks = [
        ctx.load_labware('custom_96_tuberack_500ul', f'{slot}', f'plate {i+1}')
        for i, slot in enumerate(['4', '5', '6'])]
    tips300 = [
        ctx.load_labware('opentrons_96_tiprack_300ul', slot,
                         '300ul tiprack')
        for slot in ['10', '11']]

    reagent_map = {
        'EDA': {
            'slot': '7',
            'tips': [col for rack in tips300 for col in rack.columns()][:8],
            'volume': 200,
            'flow-rate-asp': 50,
            'flow-rate-disp': 50,
            'blow-out': False
        },
        'ACN': {
            'slot': '8',
            'tips': [col for rack in tips300 for col in rack.columns()][8:16],
            'volume': 200,
            'flow-rate-asp': 50,
            'flow-rate-disp': 50,
            'blow-out': False
        },
        'amino': {
            'slot': '9',
            'tips': [col for rack in tips300 for col in rack.columns()][16:],
            'volume': 200,
            'flow-rate-asp': 50,
            'flow-rate-disp': 50,
            'blow-out': False
        }
    }
    reagent = ctx.load_labware(
        'nest_1_reservoir_195ml', reagent_map[reagent_type]['slot'],
        reagent_type).wells()[0]

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
    p300 = ctx.load_instrument(
        'p300_single_gen2', p300_mount, tip_racks=tips300)

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

    def scan_racks(num_tips, reagent_type):
        all_columns = reagent_map[reagent_type]['tips']
        for col in all_columns:
            pick_up_loc = slide_window(num_tips, col)
            if pick_up_loc:
                return pick_up_loc
        return False

    per_tip_pickup_current = .1

    def pick_up(num_tips, reagent_type):
        if not 1 <= num_tips <= 8:
            raise Exception(f'INVALID NUMBER OF TIPS: {num_tips}.')
        if num_tips > 1:
            pip = m300
            pick_up_current = num_tips*per_tip_pickup_current
            ctx._implementation._hw_manager.hardware._attached_instruments[
                pip._implementation.get_mount()].update_config_item(
                    'pick_up_current', pick_up_current)
        else:
            pip = p300

        scan_result = scan_racks(num_tips, reagent_type)
        if scan_result:
            pip.pick_up_tip(scan_result)
        else:
            ctx.pause('REFILL TIPRACKS BEFORE RESUMING.')
            [rack.reset() for rack in tips300]
            scan_result = scan_racks(num_tips, reagent_type)
            pip.pick_up_tip(scan_result)

    # parse wells into chunks
    for csv, rack in zip(
            [occupied_well_csv1, occupied_well_csv2, occupied_well_csv3],
            racks):
        occupied_wells = [
            rack.wells_by_name()[line.upper()]
            for line in csv.splitlines() if line]
        chunk_map = {num: [] for num in range(1, 9)}
        for col in rack.columns():
            running = None
            chunk_length = 0
            for well in col[::-1]:
                if well in occupied_wells:
                    running = well
                    chunk_length += 1
                else:
                    if running:
                        chunk_map[chunk_length].append(running)
                    running = None
                    chunk_length = 0
            if running:
                chunk_map[chunk_length].append(running)

        m300.flow_rate.aspirate = reagent_map[reagent_type]['flow-rate-asp']
        m300.flow_rate.dispense = reagent_map[reagent_type]['flow-rate-disp']

        for num_tips, dests in chunk_map.items():
            if len(dests) > 0:
                pick_up(num_tips, reagent_type)
                for dest in dests:
                    m300.aspirate(reagent_map[reagent_type]['volume'], reagent)
                    m300.dispense(reagent_map[reagent_type]['volume'],
                                  dest.top(-1))
                if reagent_map[reagent_type]['blow-out']:
                    m300.blow_out(dest.top(-1))
                m300.return_tip()

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
