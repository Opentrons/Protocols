import os
import json
from pathlib import Path
from protolib.parse import markdown as parser
from traversals import PROTOCOLS_BUILD_DIR, PROTOCOL_DIR
from protolib import traverse_README


def get_protobuild(protocol_code):
    protobuild_folder = Path(PROTOCOLS_BUILD_DIR) / protocol_code
    if protobuild_folder.is_dir():
        for file in protobuild_folder.iterdir():
            if '.ot2.apiv2.py.json' in file.name:
                return json.load(file)
    return None


# def check_protobuilds_and_readme():
#

def get_module_content(protobuild_data):
    pass


def generate_readme_content(protocol_path):
    """
    Scan protoBuilds directory
    """
    for proto_dir in Path(protocol_path).iterdir():
        if not proto_dir.is_dir():
            # maybe it's a .DS_Store or something
            print(f'DEBUG: Not a directory: "{proto_dir}"')
        else:
            root = proto_dir.name
            hex = root.split('/')[-1]
            files = list(proto_dir.iterdir())
            readme_files = [f for f in files if f.name == 'README.md']
            if len(readme_files) == 0:  # no README exists
                build_path = Path(PROTOCOLS_BUILD_DIR) / root
                readme_path = Path(proto_dir) / 'README.md'
                protobuild_data = get_protobuild(hex)
                readme_content_ = {
                    'author': {
                        'header': '### Author',
                        'content': '[Opentrons](https://opentrons.com/)'
                    },
                    'catgories': {
                        'header': '## Categories',
                        'content': '* \n    * '
                    },
                    'description': {
                        'header': '## Description',
                        'content': 'This protocol performs ...'
                    },
                    'modules': {
                        'header': '### Modules',
                        'content': get_module_content(protobuild_data)
                    }
                }
                if protobuild_data:
                    pass

                # with open(output_path, 'w') as output_file:
                #     json.dump(
                #         {**parser.parse(readme_files[0])}, output_file,
                #         indent=4, sort_keys=True)


def markdown_from_json():
    pass


if __name__ == '__main__':
    generate_readme_content(PROTOCOL_DIR)
