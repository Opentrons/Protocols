# import logging
import os
import json
from parse import parseOT2 as parser
from traversals import PROTOCOLS_BUILD_DIR, PROTOCOL_DIR, \
    ARGS, search_directory


def write_ot2_to_file(path):
    """
    Recursively scan through root returning the list of protocol
    dictionary items searching for ot2 files only.
    """
    for proto_dir in search_directory(path, '.ot2'):
        root = proto_dir['root'].split('/')[-1]
        build_path = os.path.join(PROTOCOLS_BUILD_DIR, root)
        if not os.path.exists(build_path):
            os.mkdir(build_path)

        for protocol_name in proto_dir['files']:
            print(protocol_name)
            protocol = os.path.join(
                path, root, protocol_name)
            file_path = os.path.join(
                build_path,
                '{}.json'.format(protocol_name))
            with open(file_path, 'w') as fh:
                json.dump(
                    {**parser.parse(protocol)}, fh)


if ARGS:
    for arg in ARGS:
        write_ot2_to_file(arg)
else:
    write_ot2_to_file(PROTOCOL_DIR)
