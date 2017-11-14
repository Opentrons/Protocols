import glob
import os
import sys
import tempfile
import zipfile
import json

from protolib import cli


def test_configure_parser():
    parser = cli.configure_parser()
    parsed_input = parser.parse_args([os.getcwd(), 'foo'])
    assert parsed_input.library_input_path == os.getcwd()
    assert parsed_input.library_output_path == 'foo'

    parsed_input = parser.parse_args([os.getcwd(), 'foo', '--fake'])
    assert parsed_input.library_input_path == os.getcwd()
    assert parsed_input.library_output_path == 'foo'
    assert parsed_input.fake
    assert parsed_input.amt == 200


def test_build_protocol_library():
    dir_to_scan = os.path.join(os.path.dirname(__file__), 'data')
    output_dir = tempfile.mkdtemp()

    sys.argv = ['cli', dir_to_scan, output_dir]
    cli.build_protocol_library()

    found_artifacts = glob.glob(os.path.join(output_dir, 'PL-data*'))

    assert len(found_artifacts) == 1
    assert found_artifacts[0].endswith('.zip')
    z = zipfile.ZipFile(found_artifacts[0])
    assert z
    assert len(z.namelist()) == 1
    pl_data = json.loads(z.open(z.namelist()[0]).read().decode())
    assert 'protocols' in pl_data.keys()
    assert 'categories' in pl_data.keys()
