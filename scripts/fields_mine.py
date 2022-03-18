import json
import os
import csv

protocols_path = 'protocols/'
all_fields = {}


def mine_fields():
    for folder in os.listdir(protocols_path):
        prtcl_path = f'{protocols_path}/{folder}'
        if os.path.isdir(prtcl_path):
            if 'fields.json' in os.listdir(prtcl_path):
                with open(f'{prtcl_path}/fields.json') as fields_file:
                    fields = json.load(fields_file)
                    for field in fields:
                        name = field['name'].lower()
                        if name not in all_fields.keys():
                            all_fields[name] = {}
                            all_fields[name]['count'] = 1
                            all_fields[name]['protocols'] = [folder]
                        else:
                            all_fields[name]['count'] += 1
                            all_fields[name]['protocols'].append(folder)

    out_path = 'data/data/fields.csv'
    out_path_js = 'data/data/fields.json'
    with open(out_path, 'w') as out_file:
        field_writer = csv.writer(out_file)
        field_writer.writerows(
            [[key, val] for key, val in sorted(all_fields.items())])
    with open(out_path_js, 'w') as out_file_js:
        json.dump(all_fields, out_file_js)


if __name__ == '__main__':
    mine_fields()
