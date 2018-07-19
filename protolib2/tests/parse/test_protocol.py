import os

from protolib2.parse import parseOT1 as OT1_parser

data_path = os.path.join(os.path.dirname(__file__), '../data')


def test_protocol_parse():
    res = OT1_parser.parse(os.path.join(data_path, 'test.py'))
    expected = {
        'containers': [
            {
                'name': "tiprack-10ul",
                'type': "tiprack-10ul",
                'slot': "C2"
            },
            {
                'name': "tiprack-200ul",
                'type': "tiprack-200ul",
                'slot': "A1"
            },
            {
                'name': "trough",
                'type': "trough-12row",
                'slot': "E1"
            },
            {
                'name': "plate",
                'type': "96-PCR-flat",
                'slot': "C1"
            },
            {
                'name': "trash",
                'type': "point",
                'slot': "B2"
            }
        ],
        'instruments': [
            {
                'name': 'p200',
                'type': 'pipette',
                'channels': 8,
                'axis': 'a',
                'max_volume': 200,
                'min_volume': 20
            },
            {
                'name': 'p10',
                'type': 'pipette',
                'channels': 1,
                'axis': 'b',
                'max_volume': 10,
                'min_volume': 1
            }
        ],
        'parameters': []
    }
    assert res == expected
