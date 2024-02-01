from reflective import Reflective


def test_slices():
    r = Reflective({'str': 'value'})

    assert r.str[0:3] == 'val'
