from reflective import Reflective


def test_json():
    r = Reflective({'key': 'value'})

    assert r().to_json(flat=True) == '{"key": "value"}'
    assert r().json == '{"key": "value"}'


def test_yaml():
    r = Reflective({'key': 'value'})

    assert r().to_yaml() == 'key: value\n'
    assert r().yaml == 'key: value\n'
