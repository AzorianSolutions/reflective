from reflective import Reflective


def test_logic():
    r = Reflective({'check': True})

    if r.check:
        assert True

    if not r.check:
        assert False

    assert r.check
