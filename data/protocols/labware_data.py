import pandas as pd
import os
import json
import numpy as np

protobuilds_path = '/Users/nickdiehl/Protocols/protoBuilds/'

protocol_data = []


def map_lw_to_type(lw):
    if 'tiprack' in lw:
        return lw
    elif 'tuberack' in lw:
        return 'tuberack'
    elif 'plate' in lw:
        return 'plate'
    elif 'reservoir' in lw:
        return 'reservoir'
    elif 'trash' in lw:
        return 'trash'
    else:
        return 'other'


def transform_category(cat, subcat):
    total_cat = cat + subcat
    if 'ngs' in total_cat or 'library prep' in total_cat:
        return 'ngs'
    elif 'extraction' in total_cat or 'purification' in total_cat:
        return 'extraction'
    elif 'pcr' in total_cat:
        return 'pcr'
    elif 'protein' in total_cat:
        return 'protein'
    elif 'normalization' in total_cat or 'cherrypicking' in total_cat:
        return 'cherrypicking'
    elif 'dilution' in total_cat:
        return 'dilution'
    elif 'sample prep' in total_cat:
        return 'sample prep'
    else:
        return 'other'


tuberack_vols = []
for folder in os.listdir(protobuilds_path):
    folder_path = protobuilds_path + folder
    prtcl_data = {}
    lw_data = {}
    pip_data = {}
    mod_data = {}
    for file in os.listdir(folder_path):
        if '.py.json' in file:
            file_path = folder_path + '/' + file
            with open(file_path) as json_file:
                data = json.load(json_file)
                lw_data['raw'] = data['labware']
                pip_data['raw'] = data['instruments']
                mod_data['raw'] = data['modules']
        if 'README.json' in file:
            rm_file_path = folder_path + '/' + file
            with open(rm_file_path) as rm_file:
                data = json.load(rm_file)
                prtcl_data['category'] = [
                    key for key in data['categories'].keys()][0].lower()
                subcat = [val for val in data['categories'].values()][0]
                if subcat:
                    prtcl_data['subcategory'] = subcat[0].lower()
                else:
                    prtcl_data['subcategory'] = [
                        key for key in data['categories'].keys()][1].lower()
    lw_data['counts'] = {
        'tuberack': 0,
        'plate': 0,
        'reservoir': 0,
        'trash': 0,
        'other': 0,
        'opentrons_96_tiprack_10ul': 0,
        'opentrons_96_tiprack_20ul': 0,
        'opentrons_96_tiprack_300ul': 0,
        'opentrons_96_tiprack_1000ul': 0,
        'opentrons_96_filtertiprack_10ul': 0,
        'opentrons_96_filtertiprack_20ul': 0,
        'opentrons_96_filtertiprack_200ul': 0,
        'opentrons_96_filtertiprack_1000ul': 0
    }
    for lw in lw_data['raw']:
        lw_type = map_lw_to_type(lw['type'])
        # if lw_type == 'tuberack':
        #     print(lw)
        if lw_type in lw_data['counts'].keys():
            lw_data['counts'][lw_type] += 1
        else:
            lw_data['counts']['other'] += 1
    pip_data['counts'] = {
        'p10_single': 0,
        'p10_multi': 0,
        'p20_single_gen2': 0,
        'p20_multi_gen2': 0,
        'p50_single': 0,
        'p50_multi': 0,
        'p300_single': 0,
        'p300_multi': 0,
        'p300_single_gen2': 0,
        'p300_multi_gen2': 0,
        'p1000_single': 0,
        'p1000_single_gen2': 0,
    }
    for pip in pip_data['raw']:
        pip_data['counts'][pip['name']] += 1
    prtcl_data['labware'] = lw_data
    prtcl_data['pipettes'] = pip_data
    # prtcl_data['modules'] = mod_data
    prtcl_data['id'] = folder
    protocol_data.append(prtcl_data)

fields = ['id', 'category', 'subcategory', 'transformed category'] + [
    key for dict in [protocol_data[0]['labware']['counts'],
                     protocol_data[0]['pipettes']['counts']]
    for key in dict.keys()]

df_dict = {
    field: []
    for field in fields
}
for p_d in protocol_data:
    df_dict['id'].append(p_d['id'])
    df_dict['category'].append(p_d['category'])
    df_dict['subcategory'].append(p_d['subcategory'])
    df_dict['transformed category'].append(
        transform_category(p_d['category'], p_d['subcategory']))
    for dict in [p_d['labware']['counts'],
                 p_d['pipettes']['counts']]:
        for field, count in dict.items():
            df_dict[field].append(count)

df = pd.DataFrame(df_dict)
tiprack_types = [
    'opentrons_96_tiprack_10ul', 'opentrons_96_tiprack_20ul',
    'opentrons_96_tiprack_300ul', 'opentrons_96_tiprack_1000ul',
    'opentrons_96_filtertiprack_10ul', 'opentrons_96_filtertiprack_20ul',
    'opentrons_96_filtertiprack_200ul',
    'opentrons_96_filtertiprack_1000ul']
df['total tipracks'] = df[tiprack_types].sum(axis=1)
df_by_category = df.groupby(['transformed category'])
averages_consumables = df.mean()[[
    'tuberack', 'plate', 'reservoir', 'total tipracks']].round(2)
avg_outfile = averages_consumables.to_csv('/Users/nicholasdiehl/Desktop/Opentrons Internal/data/protocol_data_averages.csv')
averages_by_category_consumables = df_by_category.mean()[[
    'tuberack', 'plate', 'reservoir', 'total tipracks']].round(2)
    # 'opentrons_96_tiprack_10ul', 'opentrons_96_tiprack_20ul',
    # 'opentrons_96_tiprack_300ul', 'opentrons_96_tiprack_1000ul',
    # 'opentrons_96_filtertiprack_10ul', 'opentrons_96_filtertiprack_20ul',
    # 'opentrons_96_filtertiprack_200ul',
    # 'opentrons_96_filtertiprack_1000ul']].round(2)
avg_by_cat_outfile = averages_by_category_consumables.to_csv('/Users/nicholasdiehl/Desktop/Opentrons Internal/data/protocol_data_averages_by_cat.csv')
pip_types = [
    'p10_single', 'p10_multi', 'p20_single_gen2', 'p20_multi_gen2',
    'p50_single', 'p50_multi', 'p300_single', 'p300_multi', 'p300_single_gen2',
    'p300_multi_gen2', 'p1000_single', 'p1000_single_gen2']
pipettes_avg = df.mean()[pip_types].round(2)
pip_outfile = pipettes_avg.to_csv('/Users/nicholasdiehl/Desktop/Opentrons Internal/data/pipettes.csv')
tipracks_avg = df.mean()[tiprack_types].round(3)
tipracks_outfile = tipracks_avg.to_csv('/Users/nicholasdiehl/Desktop/Opentrons Internal/data/tipracks.csv')
pipettes_by_category = df_by_category.mean()[pip_types].round(2)
pip_outfile_cat = pipettes_by_category.to_csv('/Users/nicholasdiehl/Desktop/Opentrons Internal/data/pipettes_by_cat.csv')
# print(dir(math))
# for pip_type in pip_types:
#     mean = np.mean(ngs_df[pip_type])
#     std = np.std(ngs_df[pip_type])
#     confidence_95 = [
#         mean - 1.958*std/np.sqrt(len(ngs_df[pip_type])),
#         mean + 1.958*std/np.sqrt(len(ngs_df[pip_type]))]
#     print(f'{pip_type}: {mean}\n')
outfile = df.to_csv('/Users/nicholasdiehl/Desktop/Opentrons Internal/data/protocol_data.csv')
# 7/3/2021: more granular on tipracks on tuberacks (volumes/formats)
