# import logging
import os
import json
from protolib2.parse import parseOT2 as parser
from traversals import PROTOCOL_PATH, PROTOCOLS_BUILD_DIR


def write_ot2_to_file(path):
    """
    Recursively scan through root returning the list of protocol
    dictionary items searching for ot2 files only.
    """

    for root, dirs, files in os.walk(path):
        for directory in dirs:
            try:
                os.mkdir(os.path.join(PROTOCOLS_BUILD_DIR, directory))
            except FileExistsError:
                pass
        try:
            directory = root.split('protocols/')[1]
            builds_path = os.path.join(PROTOCOLS_BUILD_DIR, directory)
            for f in files:
                protocols = []
                if not f.startswith('test_'):
                    if 'ot2' in f.split('.'):
                        protocols.append(f)
            for val, protocol_name in enumerate(protocols):
                protocol = os.path.join(
                    PROTOCOL_PATH, directory, protocol_name)
                file_path = os.path.join(
                    builds_path,
                    '{}/ot2_{}.json'.format(directory, val))
                with open(file_path, 'w') as fh:
                    json.dumps(
                        {**parser.parse(protocol)}, fh)
        except Exception:
            pass


write_ot2_to_file(PROTOCOL_PATH)
