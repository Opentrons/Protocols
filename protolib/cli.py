print('DEBUG: argparse')
import argparse  # noqa: E402
print('DEBUG: os')
import os  # noqa: E402
import sys  # noqa: E402
print('DEBUG: tempfile')
import tempfile  # noqa: E402

print('DEBUG: generate')
import generate  # noqa: E402
print('DEBUG: persist')
import persist  # noqa: E402  # noqa: E402
print('DEBUG: traverse')
import traverse  # noqa: E402
print('DEBUG: utils')
import utils  # noqa: E402

print('DEBUG: done imports')

script_tag = "[OT Protocol Library build] "
script_tab = "                            "


def configure_parser():
    parser = argparse.ArgumentParser(prog='Protocol Library Data Builder')
    parser.add_argument('library_input_path', help='path to protocol library')
    parser.add_argument(
        'library_output_path',
        help='path to protocol library build output'
    )
    parser.add_argument(
        '--fake',
        action='store_true',
        help='Enable fake mode'
    )
    parser.add_argument(
        '--amt',
        type=int,
        default=200,
        help='Amount of fake protocols to generate if in fake mode'
    )
    return parser


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


def build_protocol_library():
    print('debug: pre-parse args')
    parser = configure_parser()
    parsed_input = parser.parse_args()
    print('debug: get build dir')
    PROTOCOLS_BUILD_DIR = os.path.join(tempfile.gettempdir(), 'proto-builds')
    print('debug: get rel dir')
    PROTOCOLS_RELEASE_DIR = parsed_input.library_output_path

    print('preparing build & release dirs...')
    prepare_dirs(
        PROTOCOLS_BUILD_DIR,
        PROTOCOLS_RELEASE_DIR,
        parsed_input.library_input_path
    )

    build_name = utils.get_build_name()
    build_name = "PL-data-{}".format(build_name)
    print('build_name is:', build_name)

    def get_file_name(name, ext):
        return "{name}{ext}".format(name=name, ext=ext)

    if parsed_input.fake:
        protocols_json_data = list(generate.generate(parsed_input.amt))
    else:
        protocols_json_data = traverse.scan(parsed_input.library_input_path)

    # Persist protocol data
    def persist_data(data, file_name):
        json_path = os.path.join(
            PROTOCOLS_BUILD_DIR,
            get_file_name(file_name, '.json')
        )
        persist.write_json_to_file(data, json_path)
        return json_path

    print('traversing categories...')
    protocols_json_data = {
        'categories': traverse.tree(protocols_json_data),
        'protocols': protocols_json_data
    }
    print('persisting protocol data...')
    protocols_path = persist_data(protocols_json_data, build_name)

    utils.zip_file(
        [protocols_path],
        os.path.join(PROTOCOLS_RELEASE_DIR, get_file_name(build_name, '.zip'))
    )
    print('Successfully built library')


def get_protocols_by_flag(flag, dir_path):
    protocols = list(traverse.scan_for_protocols(dir_path))
    return [
        protocol
        for protocol in protocols
        if flag in protocol['flags'] and
        protocol['flags'][flag] is True
    ]


def list_protocols_by_flag(flag, dir_path):
    print(script_tag + "Listing Protocols w/flag: {}\n".format(flag))
    print(script_tab + "-------------------------------")
    for i, protocol in enumerate(get_protocols_by_flag(flag, dir_path)):
        print(script_tab + '{}: {}'.format(i + 1, protocol['slug']))


def list_featured_protocols():
    list_protocols_by_flag('feature', sys.argv[1])


def list_ignored_protocols():
    list_protocols_by_flag('ignore', sys.argv[1])


if __name__ == '__main__':
    print('debug: initial __main__')
    build_protocol_library()
