from pathlib import Path
import json
import csv

path_protobuilds = Path('protoBuilds/')
sorted_protocols = {
    'pcr': [],
    'nucleic-acid-purification': [],
    'ngs': [],
    'protein': [],
    'dilution': [],
    'other': []
}


def sort_category(cat_major, cat_minor, id):
    cat_total = cat_major + cat_minor
    if 'ngs' in cat_total:
        sorted_protocols['ngs'].append(id)
    elif 'nucleic acid' in cat_total:
        sorted_protocols['nucleic-acid-purification'].append(id)
    elif 'pcr' in cat_total:
        sorted_protocols['pcr'].append(id)
    elif 'protein' in cat_total:
        sorted_protocols['protein'].append(id)
    elif 'dilution' in cat_total:
        sorted_protocols['dilution'].append(id)
    else:
        sorted_protocols['other'].append(id)


for p in path_protobuilds.iterdir():
    folder_pb = Path(p)
    id = folder_pb.parts[-1]
    path_rm = [
        f for f in folder_pb.iterdir()
        if 'README.json' in str(f.parts[-1])][0]
    with open(path_rm) as f_pb:
        data = json.load(f_pb)
        category_data = data['categories']
        cat_major = [k for k in category_data.keys()][0]
        if category_data[cat_major]:
            cat_minor = category_data[cat_major][0]
        else:
            cat_minor = ''
        sort_category(cat_major.lower(), cat_minor.lower(), id)

output_file_path = 'scripts/llm/categories.csv'
with open(output_file_path, 'w') as output_file:
    writer = csv.writer(output_file)
    writer.writerow(['category', 'hexcodes'])
    for key, vals in sorted_protocols.items():
        writer.writerow([key] + vals)
