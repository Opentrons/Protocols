import glob
# import logging
import os
import json
from traversals import PROTOCOLS_BUILD_DIR, PROTOCOL_DIR, \
    ARGS, search_directory
# file handler keys
OT_1_PROTOCOL = 'OT 1 protocol'
OT_2_PROTOCOL = 'OT 2 protocol'
DESCRIPTION = 'description'

file_handlers = {
    DESCRIPTION: '*.md',
    OT_1_PROTOCOL: '*ot1.py',
    OT_2_PROTOCOL: '*ot2*.py'
}


def get_file_content(protocol_root, filename):
    with open(os.path.join(protocol_root, filename), 'r') as appfile:
        return appfile.read().strip()


def generate_metadata(root, path, files):
    return {
        'slug': root.split('/')[-1],
        'path': os.path.join(path, root),
        'flags': {
            'feature': '.feature' in files,
            'skip-tests': '.notests' in files,
            'embedded-app':
                get_file_content(os.path.join(path, root), '.embedded-app')
                if '.embedded-app' in files else False
        },
        'files': {
            file_type: [
                f.split('/')[-1]
                for f in glob.glob(os.path.join(path, root, file_glob))]
            for file_type, file_glob in file_handlers.items()
        }
    }


def get_errors(file_data):
    msg = []
    protocol_keys = [
        OT_1_PROTOCOL,
        OT_2_PROTOCOL
    ]

    protocol_file_counts = [
        len(file_data.get(key, []))
        for key in protocol_keys
    ]
    print(file_data.get(OT_1_PROTOCOL))
    print(file_data.get(OT_2_PROTOCOL))
    if sum(protocol_file_counts) == 0:
        raise ValueError('Found 0 protocol files required at least 1')

    else:
        for key, num_files in zip(protocol_keys, protocol_file_counts):
            if num_files > 1:
                raise ValueError('Found {} {} files required \
                                  no more than 1'.format(num_files, key))

    description_files = len(file_data.get(DESCRIPTION, []))
    if description_files != 1:
        raise ValueError('Found {} description files required 1'.format(
            description_files))

    return msg


def get_status(file_data):
    errors = None
    if not file_data['flags']['embedded-app']:
        errors = get_errors(file_data['files'])
    if not sum(file_data['files'].values(), []):
        return 'empty'
    return 'error' if errors else 'ok'


def write_metadata_to_file(path):
    """
    Function to write metadata to the relative path
    'protocol_dir/metadata.json'.
    """
    for proto_dir in search_directory(path, None):
        root = proto_dir['root'].split('/')[-1]
        files = proto_dir['files']
        build_path = os.path.join(PROTOCOLS_BUILD_DIR, root)
        if not os.path.exists(build_path):
            os.mkdir(build_path)
        file_path = os.path.join(
            build_path,
            'metadata.json')
        with open(file_path, 'w') as fh:
            metadata = generate_metadata(root, path, files)
            print(metadata)
            json.dump({**metadata,
                       'status': get_status(metadata)}, fh)
            print("Creating metadata")


if ARGS:
    for arg in ARGS:
        write_metadata_to_file(arg)
else:
    write_metadata_to_file(PROTOCOL_DIR)
