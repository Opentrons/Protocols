import glob
# import logging
import os
import os.path

from protolib import categories
from protolib.parse import (
    protocol as protocol_parser,
    markdown as markdown_parser
)


# log = logging.getLogger(__name__)


file_handlers = {
    'description': '*.md',
    'OT 1 protocol': '*ot1.py',
    'OT 2 protocol': '*ot2.py'
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
    protocol_found = False
    msg = []
    for field, files in file_data.items():
        if not protocol_found:
            if field != 'description':
                protocol_found = True
                field = 'protocol'
            if len(files) != 1:
                msg.append(
                    'Found {} {} files required 1'.format(len(files), field))

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
    pyfiles = protocol['detected-files'].get('OT 1 protocol')

    if not pyfiles:

        pyfiles = protocol['detected-files'].get('OT 2 protocol')

    pyfiles = filter(lambda f: not f.startswith('test_'), pyfiles)
    pyfiles = list(pyfiles)
    if not pyfiles:
        return
    return os.path.join(protocol['path'], pyfiles[0])


def get_protocol_mdfile(protocol: dict):
    """Returns path to python entry script for a protocl dir.
    Ignores python files that start with "test_"
    """
    mdfiles = protocol['detected-files']['description']
    if not mdfiles:
        return
    mdfile = protocol['detected-files']['description'][0]
    return os.path.join(protocol['path'], mdfile)


def scan(root):
    """
    Recursively scan through root returning the list of protocol
    dictionary items.
    """

    protocols = [
        {
            **protocol,
            **protocol_parser.parse(get_protocol_pyfile(protocol)),
            **markdown_parser.parse(get_protocol_mdfile(protocol))
        }
        for protocol in get_valid_protocols(root)
        if protocol['status'] != 'empty' and
        # Skipping root dir
        protocol['slug'] != '.' and not protocol['flags']['ignore']
    ]

    return protocols


def tree(protocols):
    return categories.tree([
        i.get('categories')
        for i in protocols
    ])
