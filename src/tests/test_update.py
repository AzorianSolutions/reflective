from reflective import Reflective


def test_object_update():
    """Test that we can update by object-oriented methods."""
    pass


def test_property_update():
    """Test that we can update by property access."""
    
    source = {
        'str': 'string',
        'int': 123,
        'float': 123.456,
        'complex': 123 + 456j,
        'bool': True,
        'none': None,
        'dict': {'a': 1, 'b': 2, 'c': 3, 'd': 4},
        'list': [1, 2, 3, 4],
        'tuple': (1, 2, 3, 4),
    }
    
    r = Reflective(source.copy())
    
    r.str = 'different'
    assert r.str == 'different'

    r.int = 456
    assert r.int == 456

    r.float = 456.789
    assert r.float == 456.789

    r.complex = 456 + 789j
    assert r.complex == 456 + 789j

    r.bool = False
    assert r.bool().raw is False
    r.bool = True
    assert r.bool().raw is True

    r.none = 'not none'
    assert r.none == 'not none'
    r.none = None
    assert r.none().raw is None

    r.dict = {'e': 5, 'f': 6, 'g': 7, 'h': 8}
    assert r.dict == {'e': 5, 'f': 6, 'g': 7, 'h': 8}

    r.list = [5, 6, 7, 8]
    assert r.list == [5, 6, 7, 8]

    r.tuple = (5, 6, 7, 8)
    assert r.tuple == (5, 6, 7, 8)


def test_dict_update():
    """Test that we can update by dictionary reference."""

    source = {
        'str': 'string',
        'int': 123,
        'float': 123.456,
        'complex': 123 + 456j,
        'bool': True,
        'none': None,
        'dict': {'a': 1, 'b': 2, 'c': 3, 'd': 4},
        'list': [1, 2, 3, 4],
        'tuple': (1, 2, 3, 4),
    }

    r = Reflective(source.copy())

    r['str'] = 'different'
    assert r['str'] == 'different'

    r['int'] = 456
    assert r['int'] == 456

    r['float'] = 456.789
    assert r['float'] == 456.789

    r['complex'] = 456 + 789j
    assert r['complex'] == 456 + 789j

    r['bool'] = False
    assert r['bool']().raw is False
    r['bool'] = True
    assert r['bool']().raw is True

    r['none'] = 'not none'
    assert r['none'] == 'not none'
    r['none'] = None
    assert r['none']().raw is None

    r['dict'] = {'e': 5, 'f': 6, 'g': 7, 'h': 8}
    assert r['dict'] == {'e': 5, 'f': 6, 'g': 7, 'h': 8}

    r['list'] = [5, 6, 7, 8]
    assert r['list'] == [5, 6, 7, 8]

    r['tuple'] = (5, 6, 7, 8)
    assert r['tuple'] == (5, 6, 7, 8)


def test_list_update():
    """Test that we can update by list item reference."""

    source = [
        {'key': 'value1'},
        {'key': 'value2'},
        {'key': 'value3'},
        {'key': 'value4'},
    ]

    r = Reflective(source.copy())

    r[0] = {'key': 'value5'}
    assert r[0] == {'key': 'value5'}

    r[1] = {'key': 'value6'}
    assert r[1] == {'key': 'value6'}

    r[2] = {'key': 'value7'}
    assert r[2] == {'key': 'value7'}

    r[3] = {'key': 'value8'}
    assert r[3] == {'key': 'value8'}
