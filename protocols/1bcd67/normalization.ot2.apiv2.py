import os
import json
import math

metadata = {
    'protocolName': 'Normalization',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Protocol Library',
    'apiLevel': '2.10'
}


def run(ctx):

    [input_csv, p1000_mount, m300_mount, sample_vol,
     tip_track] = get_values(  # noqa: F821
        'input_csv', 'p1000_mount', 'm300_mount', 'sample_vol', 'tip_track')

    # labware
    int_dilution_plates = [
        ctx.load_labware('thermofisherabgene_96_wellplate_2200ul', slot,
                         f'dilution plate {i+1}')
        for i, slot in enumerate(['4', '5'])]
    final_dilution_plates = [
        ctx.load_labware('thermofisherabgene_96_wellplate_2200ul', slot,
                         f'dilution plate {i+3}')
        for i, slot in enumerate(['1', '2'])]
    diluent = ctx.load_labware('thermofishernalgene_1_reservoir_300000ul',
                               '3', 'diluent').wells()[0]
    tipracks1000 = [
        ctx.load_labware('opentrons_96_tiprack_1000ul', slot)
        for slot in ['6', '9']]
    tipracks300 = [
        ctx.load_labware('opentrons_96_tiprack_300ul', slot)
        for slot in ['7', '8', '10', '11']]

    # pipettes
    if p1000_mount == m300_mount:
        raise Exception('Pipette mounts cannot match.')
    p1000 = ctx.load_instrument('p1000_single_gen2', p1000_mount,
                                tip_racks=tipracks1000)
    m300 = ctx.load_instrument('p300_multi_gen2', m300_mount,
                               tip_racks=tipracks300)

    tip_log = {val: {} for val in ctx.loaded_instruments.values()}

    folder_path = '/data/tip_track'
    tip_file_path = folder_path + '/tip_log.json'
    if tip_track and not ctx.is_simulating():
        if os.path.isfile(tip_file_path):
            with open(tip_file_path) as json_file:
                data = json.load(json_file)
                for pip in tip_log:
                    if pip.name in data:
                        tip_log[pip]['count'] = data[pip.name]
                    else:
                        tip_log[pip]['count'] = 0
        else:
            for pip in tip_log:
                tip_log[pip]['count'] = 0
    else:
        for pip in tip_log:
            tip_log[pip]['count'] = 0

    for pip in tip_log:
        if pip.type == 'multi':
            tip_log[pip]['tips'] = [tip for rack in pip.tip_racks
                                    for tip in rack.rows()[0]]
        else:
            tip_log[pip]['tips'] = [tip for rack in pip.tip_racks
                                    for tip in rack.wells()]
        tip_log[pip]['max'] = len(tip_log[pip]['tips'])

    def _pick_up(pip, loc=None):
        if tip_log[pip]['count'] == tip_log[pip]['max'] and not loc:
            ctx.pause('Replace ' + str(pip.max_volume) + 'µl tipracks before \
resuming.')
            pip.reset_tipracks()
            tip_log[pip]['count'] = 0
        if loc:
            pip.pick_up_tip(loc)
        else:
            pip.pick_up_tip(tip_log[pip]['tips'][tip_log[pip]['count']])
            tip_log[pip]['count'] += 1

    all_int_dil_s = [
        well for plate in int_dilution_plates for well in plate.wells()]
    all_final_dil_s = [
        well for plate in final_dilution_plates for well in plate.wells()]

    # parse .csv
    data = [
        [val.strip().lower() for val in line.split(',')]
        for line in input_csv.splitlines()
        if line and line.split(',')[2].strip()][1:]
    num_cols = math.ceil(len(data)/8)
    data_chunks = [
        data[i*8:i*8+8] if i < num_cols - 1 else data[i*8:]
        for i in range(num_cols)]
    max_well_vol = 1600
    max_factor_1_dil = max_well_vol/sample_vol

    def map_well_to_column(well):
        slot = int(well.parent.parent)
        column = well.display_name.split(' ')[0][1:]
        return ctx.loaded_labwares[slot].columns_by_name()[column][0]

    def dilute(chunk_dils, mode='intermediate_wells'):
        # no common dilutions if some wells don't receive diluent
        len_intermediate_wells = len(
            chunk_dils['intermediate_wells']['wells'].keys())
        len_final_wells = len(
            chunk_dils['final_wells']['wells'].keys())
        if mode == 'final_wells' and len_final_wells < len_intermediate_wells:
            lcd = 0
        else:
            lcd = min(
                [chunk_dils[mode]['wells'][val]['dilution_volume']
                 for val in chunk_dils[mode]['wells'].keys()])
        col_well = [
            key for key in chunk_dils[mode]['wells'].keys()][0]
        multi_well = map_well_to_column(col_well)
        for well in chunk_dils[mode]['wells'].keys():
            remainder = chunk_dils[mode]['wells'][well][
                'dilution_volume'] - lcd
            if remainder < 100 and remainder > 0:
                lcd -= (100-remainder)  # reassign lcd if necessary
        if not m300.has_tip:
            _pick_up(m300)
        m300.transfer(lcd, diluent, multi_well, new_tip='never')
        for well in chunk_dils[mode]['wells'].keys():
            if not p1000.has_tip:
                _pick_up(p1000)
            remainder = chunk_dils[mode]['wells'][well][
                'dilution_volume'] - lcd
            p1000.transfer(remainder, diluent, well, new_tip='never')
        return min(
            [chunk_dils[mode]['wells'][val]['dilution_volume']
             for val in chunk_dils[mode]['wells'].keys()])

    def custom_mix(chunk, mode='intermediate_wells'):
        # translate mix height (1/2 liquid level)
        first_well = [key for key in chunk[mode]['wells'].keys()][0]
        mix_well = map_well_to_column(first_well)
        mix_height = chunk[mode][
            'mix_volume_limit']/mix_well.max_volume*mix_well.depth/2
        if chunk[mode]['mix_volume_limit'] < 400:
            mix_vol = 0.75*chunk[mode]['mix_volume_limit']
        else:
            mix_vol = 300
        for h in [1, mix_height]:
            m300.mix(3, mix_vol, mix_well.bottom(h))

    p1000_tip = tip_log[p1000]['tips'][tip_log[p1000]['count']]
    p1000_tip_slot = p1000_tip.parent.parent
    p1000_tip_name = p1000_tip.display_name.split(' ')[0]
    m300_tip = tip_log[m300]['tips'][tip_log[m300]['count']]
    m300_tip_slot = m300_tip.parent.parent
    m300_tip_name = m300_tip.display_name.split(' ')[0]
    ctx.comment(f'''
        P1000 single pipette beginning at tip {p1000_tip_name} on slot \
{p1000_tip_slot}
        P300 multi pipette beginning at tip {m300_tip_name} on slot \
{m300_tip_slot}''')

    # perform dilutions
    chunks = []
    for i, chunk in enumerate(data_chunks):
        # chunk_ind = i
        # int_chunk_dil = all_int_dil_m[chunk_ind]
        # final_chunk_dil = all_final_dil_m[chunk_ind]
        # valid_1_dil = True
        chunk_data = {
            'intermediate_wells': {},
            'final_wells': {}}
        chunk_data['intermediate_wells']['wells'] = {}
        chunk_data['final_wells']['wells'] = {}
        for j, line in enumerate(chunk):
            sample_ind = i*8+j
            sample_id = line[1]
            int_dil = all_int_dil_s[sample_ind]
            final_dil = all_final_dil_s[sample_ind]
            init_conc = float(line[2])
            final_conc = float(line[3])
            dil_factor = init_conc/final_conc
            if dil_factor > max_factor_1_dil:
                dil_factor = math.sqrt(dil_factor)
                total_vol1 = sample_vol*dil_factor
                total_vol2 = 20*dil_factor  # for final plate
                dil_vol1 = total_vol1 - sample_vol
                dil_vol2 = total_vol2 - 20
                chunk_data['intermediate_wells']['wells'][int_dil] = {}
                chunk_data['intermediate_wells']['wells'][int_dil][
                    'dilution_volume'] = dil_vol1
                chunk_data['intermediate_wells'][
                    'wells'][int_dil]['sample_id'] = sample_id
                chunk_data['final_wells']['wells'][final_dil] = {}
                chunk_data['final_wells']['wells'][final_dil][
                    'dilution_volume'] = dil_vol2
                chunk_data[
                    'final_wells']['wells'][final_dil]['sample_id'] = sample_id
            else:
                total_vol = sample_vol*dil_factor
                dil_vol = total_vol - sample_vol
                chunk_data['intermediate_wells']['wells'][int_dil] = {}
                chunk_data['intermediate_wells']['wells'][int_dil][
                    'dilution_volume'] = dil_vol
                chunk_data['intermediate_wells']['wells'][
                    int_dil]['sample_id'] = sample_id
        mix_vol_limit_i = dilute(chunk_data, mode='intermediate_wells')
        chunk_data[
            'intermediate_wells']['mix_volume_limit'] = mix_vol_limit_i
        if chunk_data['final_wells']['wells']:
            mix_vol_limit_f = dilute(chunk_data, mode='final_wells')
            chunk_data['final_wells']['mix_volume_limit'] = mix_vol_limit_f
        chunks.append(chunk_data)
    if m300.has_tip:
        m300.drop_tip()
    if p1000.has_tip:
        p1000.drop_tip()

    for chunk in chunks:
        first_well_int_temp = [
            key for key in chunk['intermediate_wells']['wells'].keys()][0]
        first_well_int = map_well_to_column(first_well_int_temp)
        col = first_well_int.display_name.split(' ')[0][1:]
        plate_name = first_well_int.parent.name.split(' on ')[0]
        plate_slot = first_well_int.parent.parent

        ctx.pause(f'Load {sample_vol}µl of each sample into {plate_name} \
column {col} and replace on slot {plate_slot} before resuming.')

        # mix
        _pick_up(m300)
        # translate mix height (1/2 liquid level)
        custom_mix(chunk, mode='intermediate_wells')
        if chunk['final_wells']['wells']:
            first_well_final_temp = [
                key for key in chunk['final_wells']['wells'].keys()][0]
            first_well_final = map_well_to_column(first_well_final_temp)
            m300.transfer(20, first_well_int, first_well_final,
                          new_tip='never')
            # custom_mix(chunk, mode='final_wells')
        m300.drop_tip()

    # track final used tip
    if tip_track and not ctx.is_simulating():
        if not os.path.isdir(folder_path):
            os.mkdir(folder_path)
        data = {pip.name: tip_log[pip]['count'] for pip in tip_log}
        with open(tip_file_path, 'w') as outfile:
            json.dump(data, outfile)
