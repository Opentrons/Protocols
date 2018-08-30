import os

PROTOCOL_DIR = 'protocols'
RELEASES_DIR = 'releases'
PROTOCOLS_BUILD_DIR = os.path.join(RELEASES_DIR, 'proto-builds')


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


prepare_dirs(PROTOCOLS_BUILD_DIR, RELEASES_DIR, PROTOCOL_DIR)
