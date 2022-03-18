import math
import json
import csv

fields_path = 'data/data/fields.json'
with open(fields_path) as fields_file:
    fields = json.load(fields_file)

grouped = {}


def check_double_searches(searches):
    valid_searches = []
    for search in searches:
        valid = True
        for check in searches:
            if search in check and search != check:
                valid = False
                break
        if valid:
            valid_searches.append(search)
    return valid_searches


def group(searches, mapped=None):
    # take only valid searches
    valid_searches = check_double_searches(searches)
    for search in valid_searches:
        if mapped:
            grouped_key = mapped
        else:
            grouped_key = search
        for key in fields.keys():
            if search.lower() in key:  # basic check for containing text
                if grouped_key not in grouped:
                    grouped[grouped_key] = {}
                    grouped[grouped_key]['count'] = fields[key]['count']
                    grouped[grouped_key]['protocols'] = fields[
                        key]['protocols']
                else:
                    grouped[grouped_key]['count'] += fields[key]['count']
                    for prtcl in fields[key]['protocols']:
                        grouped[grouped_key]['protocols'].append(prtcl)


total_fields = sum([val['count'] for val in fields.values()])

# group_searches = ['height', 'samples']
# for search in group_searches:
group(['numsamps', 'sample_number', 'num_samp', 'num_samples'], 'sample number')
group(['mount'], 'pipette mount')
group(['vol'], 'volume')
group(['csv', 'file'], 'file')
group(['height', 'clearance'], 'height')
group(['seconds', 'time'], 'time')
group(['_rate'], 'flow rate')
group(['ratio'], 'ratio')
group(['start'], 'start')
group(['col'], 'column')
group(['row'], 'row')

out_file_csv_path = 'data/data/grouped.csv'
out_file_json_path = 'data/data/grouped.json'

with open(out_file_csv_path, 'w') as out_csv:
    for key in grouped:
        out_csv.write(f"{key},{grouped[key]['count']}\n")

with open(out_file_json_path, 'w') as out_json:
    json.dump(grouped, out_json, indent=4, sort_keys=True)
