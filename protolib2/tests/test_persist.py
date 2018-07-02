import json
import os
import tempfile

from protolib import persist


def test_write_json_to_file():
    data = [{'a': 1}, {'b': 2}]
    tmp_loc = os.path.join(tempfile.gettempdir(), 'foo.json')
    persist.write_json_to_file(data, tmp_loc)

    assert os.path.exists(tmp_loc)

    persisted_data = None
    with open(tmp_loc) as f:
        persisted_data = json.load(f)

    assert persisted_data == data
    os.remove(tmp_loc)
