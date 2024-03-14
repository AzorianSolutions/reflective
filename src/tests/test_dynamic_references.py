from reflective import Reflective
from reflective.types import RString, RInt, RFloat, RComplex, RBool, RNone, RDict, RList, RTuple


def test_references():
    """Test that value references receive value updates."""

    r = Reflective({'str': 'Test String'})

    reference = r.str
    original_value = f'{reference}'
    changed_value = 'Change 1'

    assert reference == original_value
    assert reference != changed_value

    r.str = f'{changed_value}'

    assert reference != original_value
    assert reference == changed_value


def test_replacements():
    """Test that value replacements function."""

    r = Reflective({'var1': 'Test String 1', 'var2': 'Test String 2', 'var3': 'My $r{var1}', 'var4': '$r{var2}-1'})

    print(r.var3)
    print(r.var4)

    assert r.var3 == 'My Test String 1'
    assert r.var4 == 'Test String 2-1'


def test_reference_types():
    """Test that the value types of the returned references are correct."""

    source = {
        "str": "string",
        "int": 123,
        "float": 123.456,
        "complex": 123 + 456j,
        "bool": True,
        "none": None,
        "dict": {"key": "value"},
        "list": [1, 2, 3, 4],
        "tuple": (1, 2, 3, 4),
    }

    r = Reflective(source)

    r.test = '$r{str}'
    assert type(r.test) is RString
    assert type(r.str().raw) is type(source['str'])

    r.test = '$r{int}'
    assert type(r.test) is RInt
    assert type(r.int().raw) is type(source['int'])

    r.test = '$r{float}'
    assert type(r.test) is RFloat
    assert type(r.float().raw) is type(source['float'])

    r.test = '$r{complex}'
    assert type(r.test) is RComplex
    assert type(r.complex().raw) is type(source['complex'])

    r.test = '$r{bool}'
    assert type(r.test) is RBool
    assert type(r.bool().raw) is type(source['bool'])

    r.test = '$r{none}'
    assert type(r.test) is RNone
    assert type(r.none().raw) is type(source['none'])

    r.test = '$r{dict}'
    assert type(r.test) is RDict
    assert type(r.dict().raw) is type(source['dict'])

    r.test = '$r{list}'
    assert type(r.test) is RList
    assert type(r.list().raw) is type(source['list'])

    r.test = '$r{tuple}'
    assert type(r.test) is RTuple
    assert type(r.tuple().raw) is type(source['tuple'])
