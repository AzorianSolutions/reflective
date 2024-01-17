from reflective import Reflective


def test_object_delete():
    """Test that we can delete by object-oriented methods."""
    pass


def test_property_delete():
    """Test that we can delete by property access."""
    
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

    assert hasattr(r, 'str')
    del r.str
    assert not hasattr(r, 'str')

    assert hasattr(r, 'int')
    del r.int
    assert not hasattr(r, 'int')

    assert hasattr(r, 'float')
    del r.float
    assert not hasattr(r, 'float')

    assert hasattr(r, 'complex')
    del r.complex
    assert not hasattr(r, 'complex')

    assert hasattr(r, 'bool')
    del r.bool
    assert not hasattr(r, 'bool')

    assert hasattr(r, 'none')
    del r.none
    assert not hasattr(r, 'none')

    assert hasattr(r, 'dict')
    del r.dict
    assert not hasattr(r, 'dict')

    assert hasattr(r, 'list')
    del r.list
    assert not hasattr(r, 'list')

    assert hasattr(r, 'tuple')
    del r.tuple
    assert not hasattr(r, 'tuple')


def test_dict_delete():
    """Test that we can delete by dictionary reference."""

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

    assert hasattr(r, 'str')
    del r['str']
    assert not hasattr(r, 'str')

    assert hasattr(r, 'int')
    del r['int']
    assert not hasattr(r, 'int')

    assert hasattr(r, 'float')
    del r['float']
    assert not hasattr(r, 'float')

    assert hasattr(r, 'complex')
    del r['complex']
    assert not hasattr(r, 'complex')

    assert hasattr(r, 'bool')
    del r['bool']
    assert not hasattr(r, 'bool')

    assert hasattr(r, 'none')
    del r['none']
    assert not hasattr(r, 'none')

    assert hasattr(r, 'dict')
    del r['dict']
    assert not hasattr(r, 'dict')

    assert hasattr(r, 'list')
    del r['list']
    assert not hasattr(r, 'list')

    assert hasattr(r, 'tuple')
    del r['tuple']
    assert not hasattr(r, 'tuple')


def test_list_delete():
    """Test that we can update by delete item reference."""

    source = [
        'item1',
        'item2',
        'item3',
        'item4',
    ]

    r = Reflective(source.copy())

    assert 'item4' in r
    del r[-1]
    assert 'item4' not in r

    assert 'item3' in r
    del r[-1]
    assert 'item3' not in r

    assert 'item2' in r
    del r[-1]
    assert 'item2' not in r

    assert 'item1' in r
    del r[-1]
    assert 'item1' not in r
