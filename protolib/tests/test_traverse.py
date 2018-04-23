import os
import os.path

from protolib import traverse

data_path = os.path.join(os.path.dirname(__file__), 'data/library')


def test_traverse():
    res = [t
           for t in traverse.scan(data_path)
           if t['status'] == 'ok' and not t['flags']['ignore']]

    del res[0]['containers']
    del res[0]['instruments']

    expected = [
        {
            'slug': 'protocol1',
            'path': os.path.join(data_path, 'protocol1'),
            'files': {
                'OT 1 protocol': 'protocol.ot1.py',
                'OT 2 protocol': None,
                'description': 'README.md'
            },
            'detected-files': {
                'OT 1 protocol': ['protocol.ot1.py'],
                'OT 2 protocol': [],
                'description': ['README.md']
            },
            'flags': {
                'ignore': False,
                'skip-tests': False,
                'feature': True,
                'embedded-app': False
            },
            'status': 'ok',
            'errors': [],
            'markdown': {},
            'parameters': []
        }
    ]

    assert res == expected


def test_tree():
    data = [
        {
            'categories': ['a'],
            'subcategories': ['b']
        },
        {
            'categories': ['a', 'c', 'd'],
            'subcategories': ['e']
        }
    ]

    data = [
        {'categories': {'a': ['b']}},
        {'categories': {'a': ['e']}},
        {'categories': {'c': []}},
        {'categories': {'d': ['e']}}
    ]

    assert traverse.tree(data) == {
        'a': ['b', 'e'],
        'c': [],
        'd': ['e']
    }


def test_protocol_ignore():
    res = [
        p
        for p in traverse.scan_for_protocols(data_path)
        if p['flags']['ignore']
    ]

    expected = [
        {
            'slug': 'protocol3',
            'path': os.path.join(data_path, 'protocol3'),
            'detected-files': {
                'OT 1 protocol': [],
                'OT 2 protocol': ['protocol.ot2.py'],
                'description': ['README.md'],
            },
            'flags': {
                'ignore': True,
                'feature': False,
                'skip-tests': False,
                'embedded-app': False
            },
        }
    ]
    assert res == expected

    found_protocols = [p for p in traverse.scan(data_path)]
    slugs = [p['slug'] for p in found_protocols]
    assert not any(['protocol3' in s for s in slugs])


def test_protocol_feature_flag():
    res = [
        p
        for p in traverse.scan_for_protocols(data_path)
        if p['flags']['feature']
    ]

    expected = [
        {
            'slug': 'protocol1',
            'path': os.path.join(data_path, 'protocol1'),
            'detected-files': {
                'OT 1 protocol': ['protocol.ot1.py'],
                'OT 2 protocol': [],
                'description': ['README.md'],
            },
            'flags': {
                'ignore': False,
                'feature': True,
                'skip-tests': False,
                'embedded-app': False
            },
        }
    ]

    assert res == expected

    found_protocols = [p for p in traverse.scan(data_path)]
    slugs = [p['slug'] for p in found_protocols]
    assert any(['protocol1' in s for s in slugs])


def test_embedded_app_flag():
    res = [
        p
        for p in traverse.scan_for_protocols(data_path)
        if p['flags'] and p['flags']['embedded-app']
    ]

    expected = [
        {
            'slug': 'protocolApp',
            'path': os.path.join(data_path, 'protocolApp'),
            'detected-files': {
                'OT 1 protocol': [],
                'OT 2 protocol': [],
                'description': ['README.md'],
            },
            'flags': {
                'ignore': False,
                'feature': False,
                'skip-tests': False,
                'embedded-app': 'http://blah.aws.s3/something/app.html'
            },
        }
    ]

    assert res == expected


def test_missing_py():
    res = [
        t for t in
        traverse.scan(data_path)
        if (t['status'] == 'error' and
            t['errors'] == ['Found 0 protocol files required 1'])
    ]

    expected = [
        {
            'slug': 'category1/protocol1',
            'path': os.path.join(data_path, 'category1/protocol1'),
            'status': 'error',
            'files': {
                'description': 'README.md',
                'OT 1 protocol': None,
                'OT 2 protocol': None},
            'detected-files': {
                'description': ['README.md'],
                'OT 1 protocol': [],
                'OT 2 protocol': []},
            'flags': {
                'ignore': False,
                'skip-tests': False,
                'feature': False,
                'embedded-app': False
            },
            'errors': ['Found 0 protocol files required 1'],
            'markdown': {}
        }
    ]

    assert res == expected


def test_missing_md():
    res = [
        t for t in
        traverse.scan(data_path)
        if (t['status'] == 'error' and
            t['errors'][0] == 'Found 0 description files required 1')
    ]
    del res[0]['containers']
    del res[0]['instruments']

    expected = [
        {
            'slug': 'category1/protocol2',
            'path': os.path.join(data_path, 'category1/protocol2'),
            'status': 'error',
            'files': {
                'description': None,
                'OT 1 protocol': 'protocol.ot1.py',
                'OT 2 protocol': 'protocol.ot2.py'},
            'detected-files': {
                'description': [],
                'OT 1 protocol': ['protocol.ot1.py'],
                'OT 2 protocol': ['protocol.ot2.py']},
            'flags': {
                'ignore': False,
                'skip-tests': False,
                'feature': False,
                'embedded-app': False
            },
            'errors': ['Found 0 description files required 1'],
            'parameters': []
        }
    ]

    assert res == expected
