import os
import json


def search_directory(protocol_dir, file_type, build_dir):
    for root, dirs, files in os.walk(protocol_dir):
        for directory in dirs:
            try:
                os.mkdir(os.path.join(build_dir, directory))
            except FileExistsError:
                pass
        directory = root.split('protocols/')[-1]
        builds_path = os.path.join(build_dir, directory)
        print("BUILD PATH {}".format(builds_path))
        protocols = []
        for f in files:
            if not f.startswith('test_'):
                if file_type in f.split('.'):
                    protocols.append(f)
        for val, protocol_name in enumerate(protocols):
            protocol = os.path.join(
                path, directory, protocol_name)
            file_path = os.path.join(
                builds_path,
                '{}_{}.json'.format(file_type, val))
            with open(file_path, 'w') as fh:
                json.dump(
                    {**parser.parse(protocol)}, fh)
