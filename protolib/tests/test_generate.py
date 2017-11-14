from protolib.generate import generate


def test_generate():
    res = list(generate(10))
    assert len(res) == 10
    assert all([{'title', 'author'}.issubset(item.keys()) for item in res])
