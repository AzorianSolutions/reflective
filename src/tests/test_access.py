from reflective import Reflective


def test_object_access():
    source = {
        "str": "string",
        "int": 123,
        "float": 123.456,
        "complex": 123 + 456j,
        "bool": True,
        "none": None,
        "dict": {"a": 1, "b": 2, "c": 3, "d": 4},
        "list": [1, 2, 3, 4],
        "tuple": (1, 2, 3, 4),
    }

    r = Reflective(source)

    assert r.str == "string"
    assert r.int == 123
    assert r.float == 123.456
    assert r.complex == 123 + 456j
    assert r.bool().ref is True
    assert r.none().ref is None
    assert r.dict == {"a": 1, "b": 2, "c": 3, "d": 4}
    assert r.list == [1, 2, 3, 4]
    assert r.tuple == (1, 2, 3, 4)


def test_dict_access():
    source = {
        "str": "string",
        "int": 123,
        "float": 123.456,
        "complex": 123 + 456j,
        "bool": True,
        "none": None,
        "dict": {"a": 1, "b": 2, "c": 3, "d": 4},
        "list": [1, 2, 3, 4],
        "tuple": (1, 2, 3, 4),
    }

    r = Reflective(source)

    assert r[''] == source
    assert r[:] == source
    assert r['str'] == "string"
    assert r['int'] == 123
    assert r['float'] == 123.456
    assert r['complex'] == 123 + 456j
    assert r['bool']().ref is True
    assert r['none']().ref is None
    assert r['dict'] == {"a": 1, "b": 2, "c": 3, "d": 4}
    assert r['dict']['a'] == 1
    assert r['dict']['b'] == 2
    assert r['dict']['c'] == 3
    assert r['dict']['d'] == 4
    assert r['list'] == [1, 2, 3, 4]
    assert r['tuple'] == (1, 2, 3, 4)


def test_list_access():
    source = [1, 2, 3, [1, 2, 3, 4]]

    r = Reflective(source)

    assert r[:] == source
    assert r[0] == 1
    assert r[1] == 2
    assert r[2] == 3
    assert r[3] == [1, 2, 3, 4]
    assert r[3][0] == 1
    assert r[3][1] == 2
    assert r[3][2] == 3
    assert r[3][3] == 4


def test_tuple_access():
    source = (1, 2, 3, (1, 2, 3, 4))

    r = Reflective(source)

    assert r[:] == source
    assert r[0] == 1
    assert r[1] == 2
    assert r[2] == 3
    assert r[3] == (1, 2, 3, 4)
    assert r[3][0] == 1
    assert r[3][1] == 2
    assert r[3][2] == 3
    assert r[3][3] == 4


def test_callable_access():
    source = {"a": 1, "b": 2, "c": 3, "d": [1, 2, 3, 4]}

    r = Reflective(source)

    assert r('') == source
    assert r('a') == 1
    assert r('b') == 2
    assert r('c') == 3
    assert r('d') == [1, 2, 3, 4]
    assert r('d')(0) == 1
    assert r('d')(1) == 2
    assert r('d')(2) == 3
    assert r('d')(3) == 4
