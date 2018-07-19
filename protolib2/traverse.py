import glob
# import logging
import os
import os.path

from protolib import categories
from protolib2.parse import (
    parseOT1 as OT1_parser,
    parseOT2 as OT2_parser,
    markdown as markdown_parser
)

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
    for root, dirs, files in os.walk(path):
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
        msg.append('Found 0 protocol files required at least 1')

    else:
        for key, num_files in zip(protocol_keys, protocol_file_counts):
            if num_files > 1:
                msg.append(
                    'Found {} {} files required no more than 1'.format(
                        num_files, key))

    description_files = len(file_data.get(DESCRIPTION, []))
    if description_files != 1:
        msg.append(
            'Found {} description files required 1'.format(
                description_files))

    return msg


def get_status(file_data):

    errors = get_errors(file_data)

    if not sum(file_data.values(), []):
        return 'empty'
    return 'error' if errors else 'ok'


def get_valid_protocols(path):
    return [
        {
            **protocol,
            'status': get_status(protocol['detected-files']),
            'errors': get_errors(protocol['detected-files']),
            'files': {
                file_type: files[0] if files else None
                for file_type, files
                in protocol['detected-files'].items()
            }
        }
        for protocol in scan_for_protocols(path)
    ]


def get_protocol_pyfile(protocol: dict):
    """Returns path to python entry script for a protocl dir.
    Ignores python files that start with "test_"
    """
    pyfilesOT1 = protocol['detected-files'].get(OT_1_PROTOCOL)
    pyfilesOT2 = protocol['detected-files'].get(OT_2_PROTOCOL)
    if pyfilesOT1:
        pyfiles = pyfilesOT1
    else:
        pyfiles = pyfilesOT2
    pyfiles = filter(lambda f: not f.startswith('test_'), pyfiles)
    pyfiles = list(pyfiles)
    if not pyfiles:
        return
    return os.path.join(protocol['path'], pyfiles[0])


def get_protocol_mdfile(protocol: dict):
    """Returns path to python entry script for a protocl dir.
    Ignores python files that start with "test_"
    """
    mdfiles = protocol['detected-files'][DESCRIPTION]
    if not mdfiles:
        return
    mdfile = protocol['detected-files'][DESCRIPTION][0]
    return os.path.join(protocol['path'], mdfile)


def scan(root):
    """
    Recursively scan through root returning the list of protocol
    dictionary items.
    """
    # # Empty list that will hold parsed python file dictionaries
    # protocols = []
    # for protocol in get_valid_protocols(root):
    #     if protocol['status'] != 'empty' and
    #     protocol['slug'] != '.' and not protocol['flags']['ignore']:
    #         # Parse the file using OT 1 parser if present
    #             protocols.append({**protocol,
    #                               **OT1_parser.parse(
    #                                   get_protocol_pyfile(protocol)),
    #                               **markdown_parser.parse(
    #                                   get_protocol_mdfile(protocol))})
    #         # Parse the file using OT 2 parser if present

    protocols = [
        {
            **protocol,
            **OT1_parser.parse(get_protocol_pyfile(protocol)),
            **markdown_parser.parse(get_protocol_mdfile(protocol))
        }
        if protocol['status'] != 'empty' and
        # Skipping root dir
        protocol['slug'] != '.' and not protocol['flags']['ignore'] and
        protocol['detected-files'].get(OT_1_PROTOCOL) else
        {
            **protocol,
            **OT2_parser.parse(get_protocol_pyfile(protocol)),
            **markdown_parser.parse(get_protocol_mdfile(protocol))
        }
        for protocol in get_valid_protocols(root)
    ]

    return protocols


def tree(protocols):
    return categories.tree([
        i.get('categories')
        for i in protocols
    ])
