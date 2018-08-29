import os
import tempfile

PROTOCOL_PATH = os.path.join(
    os.path.expanduser("~"), 'Protocols/protocols/')
PROTOCOLS_BUILD_DIR = os.path.join(tempfile.gettempdir(), 'proto-builds')
LIBRARY_PATH = os.path.join(tempfile.gettempdir(), 'proto-releases')


def prepare_dirs(
    protocols_build_dir, protocols_release_dir, library_input_path
):
    try:
        os.mkdir(protocols_build_dir)
    except FileExistsError:
        pass

    try:
        os.mkdir(protocols_release_dir)
    except FileExistsError:
        pass

    if not os.path.exists(library_input_path):
        raise SystemExit('Protocol Library path does not exist')


prepare_dirs(PROTOCOLS_BUILD_DIR, LIBRARY_PATH, PROTOCOL_PATH)
