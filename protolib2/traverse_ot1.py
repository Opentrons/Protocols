# import logging
import os
import json
import opentrons
from traversals import PROTOCOLS_BUILD_DIR, PROTOCOL_DIR, \
    ARGS, search_directory
from parse import parseOT1 as parser


def write_ot1_to_file(path):
    """
    Recursively scan through root returning the list of protocol
    dictionary items searching for ot1 files only.
    """
    print('Opentrons verson: ', opentrons.__version__)
    print('Parsing OT1. Files in {}'.format(path))
    for proto_dir in search_directory(path, '.ot1'):
        root = proto_dir['root'].split('/')[-1]
        build_path = os.path.join(PROTOCOLS_BUILD_DIR, root)
        if not os.path.exists(build_path):
            os.mkdir(build_path)

        for protocol_name in proto_dir['files']:
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
        write_ot1_to_file(arg)
else:
    write_ot1_to_file(PROTOCOL_DIR)
