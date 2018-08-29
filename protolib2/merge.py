import os
import json
from traversals import LIBRARY_PATH


def merge_protocols(path):
    # Create generator object of protocol object(s) found
    # in the /protocols directory
    release_path = os.path.join(LIBRARY_PATH, 'output.json')
    with open(release_path, 'a') as final_file:
        for root, dirs, files in os.walk(path, topdown=False):
            for f in files:
                add_protocols = True
                if 'metadata' in f.split('.'):
                    fh = open(os.path.join(root, f), 'r')
                    data = json.load(fh)
                    status = data['status']
                    slug = data['slug']
                    ignore = data['flags']['ignore']
                    if status != 'empty' and slug != '.' and not ignore:
                        json.dumps(data, final_file)
                    else:
                        add_protocols = False

                if add_protocols:
                    fh = open(os.path.join(root, f), 'r')
                    data = json.load(fh)
                    json.dumps(data, final_file)

            return "Success"
