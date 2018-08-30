import glob
# import logging
import os
import json
from traversals import PROTOCOL_DIR, PROTOCOLS_BUILD_DIR
# file handler keys
OT_1_PROTOCOL = 'OT 1 protocol'
OT_2_PROTOCOL = 'OT 2 protocol'
DESCRIPTION = 'description'

file_handlers = {
    DESCRIPTION: '*.md',
    OT_1_PROTOCOL: '*ot1.py',
    OT_2_PROTOCOL: '*ot2.py'
}


def get_file_content(protocol_root, filename):
    with open(os.path.join(protocol_root, filename), 'r') as appfile:
        return appfile.read().strip()


def scan_for_protocols(path):
    # Create generator object of protocol object(s) found
    # in the /protocols directory
    for root, dirs, files in os.walk(path):
        print(root)
        print(dirs)
        print(files)
        if os.path.relpath(root, start=path) != '.':
            yield {
                'slug': os.path.relpath(root, start=path),
                'path': root,
                'flags': {
                    'ignore': '.ignore' in files,
                    'feature': '.feature' in files,
                    'skip-tests': '.notests' in files,
                    'embedded-app':
                        get_file_content(root, '.embedded-app')
                        if '.embedded-app' in files else False
                },
                'detected-files': {
                    file_type: [
                        os.path.relpath(f, start=root)
                        for f in glob.glob(os.path.join(root, file_glob))]
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
    if not file_data['flags']['ignore'] and not file_data['flags']['embedded-app']:
        errors = get_errors(file_data['detected-files'])
    if not sum(file_data['detected-files'].values(), []):
        return 'empty'
    return 'error' if errors else 'ok'


def write_metadata_to_file(path):
    """
    Function to write metadata to the relative path
    'protocol_dir/metadata.json'.
    """
    print("In function!")
    for protocol in scan_for_protocols(path):
        try:
            file_path = os.path.join(
                PROTOCOLS_BUILD_DIR,
                '{}/metadata.json'.format(protocol['slug'].split('/')[-1]))
            print(file_path)
            with open(file_path, 'w') as fh:
                json.dump({**protocol,
                           'status': get_status(protocol),
                           'files': {
                                file_type: files[0] if files else None
                                for file_type, files
                                in protocol['detected-files'].items()
                            }}, fh)
                print("Creating metadata")
        except IndexError:
            pass


write_metadata_to_file(PROTOCOL_DIR)
