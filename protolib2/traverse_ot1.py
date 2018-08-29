# import logging
import os
import json
import opentrons
from traversals import PROTOCOL_PATH, PROTOCOLS_BUILD_DIR
from parse import parseOT1 as parser


def write_ot1_to_file(path):
    """
    Recursively scan through root returning the list of protocol
    dictionary items searching for ot1 files only.
    """
    print('Opentrons verson: ', opentrons.__version__)
    print('Parsing OT1. Files in {}:'.format(path))
    for root, dirs, files in os.walk(path):
        for directory in dirs:
            try:
                os.mkdir(os.path.join(PROTOCOLS_BUILD_DIR, directory))
            except FileExistsError:
                pass
        try:
            directory = root.split('protocols/')[-1]
            builds_path = os.path.join(PROTOCOLS_BUILD_DIR, directory)
            print(builds_path)
            protocols = []
            for f in files:
                if not f.startswith('test_'):
                    if 'ot1' in f.split('.'):
                        protocols.append(f)
            for val, protocol_name in enumerate(protocols):
                protocol = os.path.join(
                    path, directory, protocol_name)
                file_path = os.path.join(
                    builds_path,
                    '{}/ot1_{}.json'.format(directory, val))
                with open(file_path, 'w') as fh:
                    json.dump(
                        {**parser.parse(protocol)}, fh)
        except Exception:
            pass


write_ot1_to_file(PROTOCOL_PATH)
