from reflective import Reflective


def test_representations():
    """Test that the value reference representations match the underlying value representations."""

    source = {
        "str": "My Test String",
        "int": 123,
        "float": 123.456,
        "complex": 123+456j,
        "bool": True,
        "none": None,
        "dict": {"a": 1, "b": 2, "c": 3, "d": 4},
        "list": [1, 2, 3, 4],
        "tuple": (1, 2, 3, 4),
    }

    r = Reflective(source.copy())

    for q in source.keys():
        src = source[q].__repr__()
        assert src == getattr(r, q).__repr__()
        assert src == r[q].__repr__()
        assert src == r(q).__repr__()
