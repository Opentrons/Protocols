import math
import json

metadata = {
    'protocolName': 'Normalization',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Protocol Library',
    'apiLevel': '2.10'
}


def run(ctx):

    [dil_json_1, dil_json_2, dil_json_3, p1000_mount, m300_mount
     ] = get_values(  # noqa: F821
        'dil_json_1', 'dil_json_2', 'dil_json_3', 'p1000_mount', 'm300_mount')

    # labware
    dw_plate = ctx.load_labware('thermofisherabgene_96_wellplate_2200ul', '8',
                                'deepwell plate')
    final_dilution_plates = [
        ctx.load_labware('thermofisherabgene_96_wellplate_2200ul', slot,
                         f'dilution plate {i+3}')
        for i, slot in enumerate(['4', '5', '6'])]
    diluent = ctx.load_labware('thermofishernalgene_1_reservoir_300000ul',
                               '9', 'diluent').wells()[0]
    tipracks1000 = [
        ctx.load_labware('opentrons_96_tiprack_1000ul', slot)
        for slot in ['10']]
    tipracks300 = [
        ctx.load_labware('opentrons_96_tiprack_300ul', slot)
        for slot in ['7', '11']]

    # pipettes
    if p1000_mount == m300_mount:
        raise Exception('Pipette mounts cannot match.')
    p1000 = ctx.load_instrument('p1000_single_gen2', p1000_mount,
                                tip_racks=tipracks1000)
    p300 = ctx.load_instrument('p300_multi_gen2', m300_mount,
                               tip_racks=tipracks300)

    tip_data = {
        'single': {
            'count': 0,
            'tips': [
                well for rack in tipracks300[::-1]
                for col in rack.columns()[::-1]
                for well in col[::-1]]
        },
        'multi': {
            'count': 0,
            'tips': [well for rack in tipracks300 for well in rack.rows()[0]]
        }
    }

    def pickup_p300(mode='single'):
        current = 0.1 if mode == 'single' else 0.5
        ctx._implementation._hw_manager.hardware._attached_instruments[
            p300._implementation.get_mount()].update_config_item(
                'pick_up_current', current)

        p300.pick_up_tip(tip_data[mode]['tips'][tip_data[mode]['count']])
        tip_data[mode]['count'] += 1

    def extract_well_name(well_obj):
        return well_obj.display_name.split(' ')[0]

    def custom_transfer(vol, source, dest, pip=p300):
        num_trans = math.ceil(vol/pip.max_volume)
        vol_per_trans = vol/num_trans
        for n in range(num_trans):
            pip.aspirate(vol_per_trans, source)
            pip.dispense(vol_per_trans, dest)

    # read .json files as dictionaries
    # dict1 = {'A1': 15.384615384615385, 'B1': 15.384615384615385, 'C1': 15, 'D1': 15.384615384615385, 'E1': 15, 'F1': 15, 'G1': 15.384615384615385, 'H1': 15.384615384615385, 'A4': 15.384615384615385, 'B4': 15.384615384615385, 'C4': 15.384615384615385, 'D4': 15.384615384615385, 'E4': 15.384615384615385, 'F4': 15.384615384615385, 'G4': 15.384615384615385, 'H4': 15.384615384615385, 'A7': 15.384615384615385, 'B7': 15.384615384615385, 'C7': 15.384615384615385, 'D7': 15.384615384615385, 'E7': 15.384615384615385, 'F7': 15.384615384615385, 'G7': 15.384615384615385, 'H7': 15.384615384615385, 'A10': 15.384615384615385, 'B10': 15.384615384615385, 'C10': 16.666666666666668, 'D10': 15.384615384615385, 'E10': 15.384615384615385, 'F10': 15.384615384615385, 'G10': 15.384615384615385, 'H10': 15.384615384615385}
    # dict2 = {'A2': 94.85458612975391, 'B2': 88.14968814968815, 'C2': 67.379140553911, 'D2': 86.00405679513185, 'E2': 112.86745668638694, 'F2': 25.783657431394744, 'G2': 61.00719424460432, 'H2': 37.890974084003574, 'A5': 107.61421319796953, 'B5': 100.41444641799882, 'C5': 50.236966824644554, 'D5': 160.60606060606062, 'E5': 483.19088319088326, 'F5': 208.25147347740665, 'G5': 106.53266331658293, 'H5': 248.8262910798122, 'A8': 41.897233201581024, 'B8': 34.78260869565217, 'C8': 21.687979539641944, 'D8': 286.4864864864865, 'E8': 410.0580270793036, 'F8': 77.23132969034609, 'G8': 26.801517067003793, 'H8': 28.571428571428573, 'A11': 145.70446735395188, 'B11': 146.71280276816609, 'C11': 773.6842105263156, 'D11': 313.6094674556213, 'E11': 135.31914893617022, 'F11': 24.118316268486915, 'G11': 69.6223316912972, 'H11': 62.9547141796585}
    # dict3 = {'A3': None, 'B3': None, 'C3': 67.379140553911, 'D3': None, 'E3': 112.86745668638694, 'F3': 25.783657431394744, 'G3': None, 'H3': None, 'A6': None, 'B6': None, 'C6': None, 'D6': None, 'E6': None, 'F6': None, 'G6': None, 'H6': None, 'A9': None, 'B9': None, 'C9': None, 'D9': None, 'E9': None, 'F9': None, 'G9': None, 'H9': None, 'A12': None, 'B12': None, 'C12': None, 'D12': None, 'E12': None, 'F12': None, 'G12': None, 'H12': None}
    dict1 = json.loads(dil_json_1)
    print("TEST")
    dict2 = json.loads(dil_json_2)
    dict3 = json.loads(dil_json_3)

    map_dil_wells = {
        well_set[0]: {
            well_set[0]: dict1[extract_well_name(well_set[0])],
            well_set[1]: dict2[extract_well_name(well_set[1])],
            well_set[2]: dict3[extract_well_name(well_set[2])]
        }
        for well_set in [
            row[i*3:(i+1)*3] for i in range(4) for row in dw_plate.rows()]
    }

    final_locations = []
    for key, dict in map_dil_wells.items():
        final_well = None
        for well, vol in dict.items():
            if vol:
                final_well = well
        final_locations.append(final_well)

    # pre-add diluent
    pickup_p300('multi')
    for col in dw_plate.rows()[0]:
        p300.transfer(800, diluent, col, new_tip='never')
    p300.drop_tip()

    # prompt user to transfer neat sample
    sample_str = '\n'.join([
        f'Transfer {vol}uL to well {well} of plate on slot 5.'
        for well, vol in dict1.items()])
    ctx.pause(msg=sample_str)

    # perform dilutions
    for set in map_dil_wells.values():
        for i, (well, vol) in enumerate(set.items()):
            if i > 0 and vol:  # neat is manually added
                if vol <= 200:
                    pip = p300
                    pickup_p300('single')
                else:
                    pip = p1000
                    p1000.pick_up_tip()
                custom_transfer(vol, list(set.keys())[i-1], well, pip)
                pip.mix(5, 100, well)
                pip.drop_tip()

    # final transfer
    final_targets = [
        well for plate in final_dilution_plates for well in plate.rows()[0]]

    for source, dest in zip(final_locations, final_targets):
        p1000.transfer(800, source, dest)
