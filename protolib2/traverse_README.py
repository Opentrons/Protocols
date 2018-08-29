import os
import json
from parse import markdown as parser
from traversals import PROTOCOL_PATH, PROTOCOLS_BUILD_DIR


def write_README_to_json(path):
    """
    Recursively scan through root returning the list of protocol
    dictionary items.
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
            README = ''
            for f in files:
                if 'md' in f.split('.'):
                    README = f
            file_path = os.path.join(
                builds_path,
                '{}/README.json'.format(directory))
            README = os.path.join(path, directory, README)
            with open(file_path, 'w') as fh:
                json.dumps(
                    {**parser.parse(README)}, fh)
        except Exception:
            pass


write_README_to_json(PROTOCOL_PATH)
