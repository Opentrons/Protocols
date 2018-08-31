import os
import json
from parse import markdown as parser
from traversals import PROTOCOLS_BUILD_DIR, PROTOCOL_DIR, \
    ARGS, search_directory


def write_README_to_json(path):
    """
    Recursively scan through root returning the list of protocol
    dictionary items.
    """
    for proto_dir in search_directory(path, '.md'):
        root = proto_dir['root'].split('/')[-1]
        build_path = os.path.join(PROTOCOLS_BUILD_DIR, root)
        if not os.path.exists(build_path):
            os.mkdir(build_path)

        for val, protocol_name in enumerate(proto_dir['files']):
            protocol = os.path.join(
                path, root, protocol_name)
            file_path = os.path.join(
                build_path,
                'README.json')
            with open(file_path, 'w') as fh:
                json.dump(
                    {**parser.parse(protocol)}, fh)

if ARGS:
    for arg in ARGS:
        write_README_to_json(arg)
else:
    write_README_to_json(PROTOCOL_DIR)
