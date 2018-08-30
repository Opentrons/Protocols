import os
import json
from protolib2.traversals import RELEASES_DIR


def merge_protocols(path):
    # Create generator object of protocol object(s) found
    # in the /protocols directory
    release_path = os.path.join(RELEASES_DIR, 'output.json')
    # with open(release_path, 'a') as final_file:
    for root, dirs, files in os.walk(path):
        print(root)
        for f in files:
            print(f)
            # if 'metadata' in f.split('.'):
            #     print(os.path.join(root, f))
            #     fh = open(os.path.join(root, f), 'r')
            #     print("File Obj", fh)
            #     data = json.load(fh)
            #     status = data['status']
            #     ignore = data['flags']['ignore']
            #     if status != 'empty' and not ignore:
            #         print(data)
            #         json.dump(data, final_file)
            #     else:
            #         pass
            #
            # fh = open(os.path.join(root, f), 'r')
            # data = json.load(fh)
            # json.dump(data, final_file)

            return "Success"
