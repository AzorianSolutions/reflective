from reflective import Reflective


def test_dict_paths():
    """Test that we can access by dictionary reference."""

    source = {
        "test": {
            "str": "My Test String",
            "int": 123,
            "float": 123.456,
            "complex": 123 + 456j,
            "bool": True,
            "none": None,
            "dict": {"a": [1, 2, 3, 4]},
            "list": [1, 2, 3, 4],
            "tuple": (1, 2, 3, 4),
        }
    }

    r = Reflective(source.copy())

    assert r['test/str'] == source['test']['str']
    assert r['test/int'] == source['test']['int']
    assert r['test/float'] == source['test']['float']
    assert r['test/bool'] == source['test']['bool']
    assert r['test/none'] == source['test']['none']
    assert r['test/dict'] == source['test']['dict']
    assert r['test/list'] == source['test']['list']
    assert r['test/tuple'] == source['test']['tuple']

    assert r['test/dict/a/0'] == source['test']['dict']['a'][0]
    assert r['test/dict/a/1'] == source['test']['dict']['a'][1]
    assert r['test/dict/a/2'] == source['test']['dict']['a'][2]
    assert r['test/dict/a/3'] == source['test']['dict']['a'][3]


def test_list_paths():
    """Test that we can access list items by path."""

    source = {
        "dict": {"a": [1, 2, 3, 4]},
        "list": [1, 2, 3, 4],
    }
    
    r = Reflective(source.copy())

    assert r('list/0') == source['list'][0]
    assert r('list/1') == source['list'][1]
    assert r('list/2') == source['list'][2]
    assert r('list/3') == source['list'][3]

    assert r('dict/a/0') == source['dict']['a'][0]
    assert r('dict/a/1') == source['dict']['a'][1]
    assert r('dict/a/2') == source['dict']['a'][2]
    assert r('dict/a/3') == source['dict']['a'][3]

    # assert r('list/-1') == source['list'][-1]


def test_list_path_slices():
    """Test that we can access list slices by path."""

    # assert r('list/:') == source['list']
    # assert r('list/0:1') == source['list'][0:1]
    # assert r('list/0:') == source['list'][0:]
    # assert r('list/-1:') == source['list'][-1:]
    # assert r('list/:0') == source['list'][:0]
    # assert r('list/:-1') == source['list'][:-1]

    pass


def test_tuple_paths():
    """Test that we can access tuple items by path."""

    source = {
        "dict": {"a": (1, 2, 3, 4)},
        "tuple": (1, 2, 3, 4),
    }

    r = Reflective(source.copy())
    
    assert r('tuple/0') == source['tuple'][0]
    assert r('tuple/1') == source['tuple'][1]
    assert r('tuple/2') == source['tuple'][2]
    assert r('tuple/3') == source['tuple'][3]

    assert r('dict/a/0') == source['dict']['a'][0]
    assert r('dict/a/1') == source['dict']['a'][1]
    assert r('dict/a/2') == source['dict']['a'][2]
    assert r('dict/a/3') == source['dict']['a'][3]

    # assert r('tuple/-1') == source['composite']['tuple'][-1]


def test_tuple_path_slices():
    """Test that we can access tuple slices by path."""

    # assert r('tuple/:') == source['composite']['tuple']
    # assert r('tuple/0:1') == source['composite']['tuple'][0:1]
    # assert r('tuple/0:') == source['composite']['tuple'][0:]
    # assert r('tuple/-1:') == source['composite']['tuple'][-1:]
    # assert r('tuple/:0') == source['composite']['tuple'][:0]
    # assert r('tuple/:-1') == source['composite']['tuple'][:-1]

    pass
