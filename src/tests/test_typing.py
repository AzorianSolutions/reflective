from reflective import Reflective
from reflective.types import RString, RInt, RFloat, RComplex, RBool, RNone, RDict, RList, RTuple


def test_object_types():
    r = Reflective({
        "str": "string",
        "int": 123,
        "float": 123.456,
        "complex": 123 + 456j,
        "bool": True,
        "none": None,
        "dict": {"a": 1, "b": 2, "c": 3, "d": 4},
        "list": [1, 2, 3, 4],
        "tuple": (1, 2, 3, 4),
    })

    assert type(r) is RDict
    assert type(r.str) is RString
    assert type(r.int) is RInt
    assert type(r.float) is RFloat
    assert type(r.complex) is RComplex
    assert type(r.bool) is RBool
    assert type(r.none) is RNone
    assert type(r.dict) is RDict
    assert type(r.list) is RList
    assert type(r.tuple) is RTuple

    assert isinstance(r().ref, dict)
    assert isinstance(r.str().ref, str)
    assert isinstance(r.int().ref, int)
    assert isinstance(r.float().ref, float)
    assert isinstance(r.complex().ref, complex)
    assert isinstance(r.bool().ref, bool)
    assert isinstance(r.none().ref, type(None))
    assert isinstance(r.dict().ref, dict)
    assert isinstance(r.list().ref, list)
    assert isinstance(r.tuple().ref, tuple)

    assert isinstance(r().raw, dict)
    assert isinstance(r.str().raw, str)
    assert isinstance(r.int().raw, int)
    assert isinstance(r.float().raw, float)
    assert isinstance(r.complex().raw, complex)
    assert isinstance(r.bool().raw, bool)
    assert isinstance(r.none().raw, type(None))
    assert isinstance(r.dict().raw, dict)
    assert isinstance(r.list().raw, list)
    assert isinstance(r.tuple().raw, tuple)


def test_dict_types():
    r = Reflective({
        "str": "string",
        "int": 123,
        "float": 123.456,
        "complex": 123 + 456j,
        "bool": True,
        "none": None,
        "dict": {"a": 1, "b": 2, "c": 3, "d": 4},
        "list": [1, 2, 3, 4],
        "tuple": (1, 2, 3, 4),
    })

    assert type(r) is RDict
    assert type(r['str']) is RString
    assert type(r['int']) is RInt
    assert type(r['float']) is RFloat
    assert type(r['complex']) is RComplex
    assert type(r['bool']) is RBool
    assert type(r['none']) is RNone
    assert type(r['dict']) is RDict
    assert type(r['list']) is RList
    assert type(r['tuple']) is RTuple

    assert isinstance(r().ref, dict)
    assert isinstance(r['str']().ref, str)
    assert isinstance(r['int']().ref, int)
    assert isinstance(r['float']().ref, float)
    assert isinstance(r['complex']().ref, complex)
    assert isinstance(r['bool']().ref, bool)
    assert isinstance(r['none']().ref, type(None))
    assert isinstance(r['dict']().ref, dict)
    assert isinstance(r['list']().ref, list)
    assert isinstance(r['tuple']().ref, tuple)

    assert isinstance(r().raw, dict)
    assert isinstance(r['str']().raw, str)
    assert isinstance(r['int']().raw, int)
    assert isinstance(r['float']().raw, float)
    assert isinstance(r['complex']().raw, complex)
    assert isinstance(r['bool']().raw, bool)
    assert isinstance(r['none']().raw, type(None))
    assert isinstance(r['dict']().raw, dict)
    assert isinstance(r['list']().raw, list)
    assert isinstance(r['tuple']().raw, tuple)


def test_list_types():
    r = Reflective([
        "string",
        123,
        123.456,
        123 + 456j,
        True,
        None,
        {"key": "value"},
        [1, 2, 3, 4],
        (1, 2, 3, 4),
    ])

    assert type(r) is RList
    assert type(r('0')) is RString
    assert type(r[1]) is RInt
    assert type(r[2]) is RFloat
    assert type(r[3]) is RComplex
    assert type(r[4]) is RBool
    assert type(r[5]) is RNone
    assert type(r[6]) is RDict
    assert type(r[7]) is RList
    assert type(r[8]) is RTuple

    assert isinstance(r().ref, list)
    assert isinstance(r[0]().ref, str)
    assert isinstance(r[1]().ref, int)
    assert isinstance(r[2]().ref, float)
    assert isinstance(r[3]().ref, complex)
    assert isinstance(r[4]().ref, bool)
    assert isinstance(r[5]().ref, type(None))
    assert isinstance(r[6]().ref, dict)
    assert isinstance(r[7]().ref, list)
    assert isinstance(r[8]().ref, tuple)

    assert isinstance(r().raw, list)
    assert isinstance(r[0]().raw, str)
    assert isinstance(r[1]().raw, int)
    assert isinstance(r[2]().raw, float)
    assert isinstance(r[3]().raw, complex)
    assert isinstance(r[4]().raw, bool)
    assert isinstance(r[5]().raw, type(None))
    assert isinstance(r[6]().raw, dict)
    assert isinstance(r[7]().raw, list)
    assert isinstance(r[8]().raw, tuple)


def test_callable_types():
    r = Reflective({
        "str": "string",
        "int": 123,
        "float": 123.456,
        "complex": 123 + 456j,
        "bool": True,
        "none": None,
        "dict": {"a": 1, "b": 2, "c": 3, "d": 4},
        "list": [1, 2, 3, 4],
        "tuple": (1, 2, 3, 4),
    })

    assert type(r) is RDict
    assert type(r('str')) is RString
    assert type(r('int')) is RInt
    assert type(r('float')) is RFloat
    assert type(r('complex')) is RComplex
    assert type(r('bool')) is RBool
    assert type(r('none')) is RNone
    assert type(r('dict')) is RDict
    assert type(r('list')) is RList
    assert type(r('tuple')) is RTuple


def test_reference_type_invalidation():
    from reflective.exceptions import RInvalidReference

    r = Reflective({'key': 'value'})

    passing = True
    ref = r.key
    str(ref)
    r.key = 123

    try:
        str(ref)
        passing = False
    except RInvalidReference:
        pass

    assert passing

    ref = r.key
    str(ref)
    r.key = 123.456

    try:
        str(ref)
        passing = False
    except RInvalidReference:
        pass

    assert passing

    ref = r.key
    str(ref)
    r.key = 123 + 456j

    try:
        str(ref)
        passing = False
    except RInvalidReference:
        pass

    assert passing

    ref = r.key
    str(ref)
    r.key = True

    try:
        str(ref)
        passing = False
    except RInvalidReference:
        pass

    assert passing

    ref = r.key
    str(ref)
    r.key = None

    try:
        str(ref)
        passing = False
    except RInvalidReference:
        pass

    assert passing

    ref = r.key
    str(ref)
    r.key = {'key': 'value'}

    try:
        str(ref)
        passing = False
    except RInvalidReference:
        pass

    assert passing

    ref = r.key
    str(ref)
    r.key = [1, 2, 3, 4]

    try:
        str(ref)
        passing = False
    except RInvalidReference:
        pass

    assert passing

    ref = r.key
    str(ref)
    r.key = (1, 2, 3, 4)

    try:
        str(ref)
        passing = False
    except RInvalidReference:
        pass

    assert passing
