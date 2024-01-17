from reflective.query import Query


def test_query_class():
    q = Query('test')
    assert q.query == 'test'
    assert q.type is str
    assert q.path == ['test']
    assert q.is_path is False
    assert q.is_relative is True

    q = Query('/test')
    assert q.query == 'test'
    assert q.type is str
    assert q.path == ['test']
    assert q.is_path is True
    assert q.is_relative is False

    q = Query('test/test')
    assert q.query == 'test/test'
    assert q.type is str
    assert q.path == ['test', 'test']
    assert q.is_path is True
    assert q.is_relative is True

    q = Query('/test/test')
    assert q.query == 'test/test'
    assert q.type is str
    assert q.path == ['test', 'test']
    assert q.is_path is True
    assert q.is_relative is False

    q = Query('1')
    assert q.query == '1'
    assert q.type is str
    assert q.path == [1]
    assert q.is_path is False
    assert q.is_relative is True

    q = Query('/1')
    assert q.query == '1'
    assert q.type is str
    assert q.path == [1]
    assert q.is_path is True
    assert q.is_relative is False

    q = Query('-1')
    assert q.query == '-1'
    assert q.type is str
    assert q.path == [-1]
    assert q.is_path is False
    assert q.is_relative is True

    q = Query('/-1')
    assert q.query == '-1'
    assert q.type is str
    assert q.path == [-1]
    assert q.is_path is True
    assert q.is_relative is False

    q = Query('test/test/1')
    assert q.query == 'test/test/1'
    assert q.type is str
    assert q.path == ['test', 'test', 1]
    assert q.is_path is True
    assert q.is_relative is True

    q = Query('/test/test/-1')
    assert q.query == 'test/test/-1'
    assert q.type is str
    assert q.path == ['test', 'test', -1]
    assert q.is_path is True
    assert q.is_relative is False

    q = Query('0:1')
    assert q.query == '0:1'
    assert q.type is str
    assert q.path == [slice(0, 1)]
    assert q.is_path is False
    assert q.is_relative is True

    q = Query('0:10:2')
    assert q.query == '0:10:2'
    assert q.type is str
    assert q.path == [slice(0, 10, 2)]
    assert q.is_path is False
    assert q.is_relative is True

    q = Query(':1')
    assert q.query == ':1'
    assert q.type is str
    assert q.path == [slice(None, 1)]
    assert q.is_path is False
    assert q.is_relative is True

    q = Query('1:')
    assert q.query == '1:'
    assert q.type is str
    assert q.path == [slice(1, None)]
    assert q.is_path is False
    assert q.is_relative is True

    q = Query('1::')
    assert q.query == '1::'
    assert q.type is str
    assert q.path == [slice(1, None)]
    assert q.is_path is False
    assert q.is_relative is True

    q = Query(':1:')
    assert q.query == ':1:'
    assert q.type is str
    assert q.path == [slice(None, 1)]
    assert q.is_path is False
    assert q.is_relative is True

    q = Query('::1')
    assert q.query == '::1'
    assert q.type is str
    assert q.path == [slice(None, None, 1)]
    assert q.is_path is False
    assert q.is_relative is True

    q = Query(':10:2')
    assert q.query == ':10:2'
    assert q.type is str
    assert q.path == [slice(None, 10, 2)]
    assert q.is_path is False
    assert q.is_relative is True

    q = Query('10:2:')
    assert q.query == '10:2:'
    assert q.type is str
    assert q.path == [slice(10, 2)]
    assert q.is_path is False
    assert q.is_relative is True

    q = Query('test/test/1:')
    assert q.query == 'test/test/1:'
    assert q.type is str
    assert q.path == ['test', 'test', slice(1, None)]
    assert q.is_path is True
    assert q.is_relative is True

    q = Query('test/test/:1')
    assert q.query == 'test/test/:1'
    assert q.type is str
    assert q.path == ['test', 'test', slice(None, 1)]
    assert q.is_path is True
    assert q.is_relative is True

    q = Query('test/test/::1')
    assert q.query == 'test/test/::1'
    assert q.type is str
    assert q.path == ['test', 'test', slice(None, None, 1)]
    assert q.is_path is True
    assert q.is_relative is True

    q = Query('test/test/0:2')
    assert q.query == 'test/test/0:2'
    assert q.type is str
    assert q.path == ['test', 'test', slice(0, 2)]
    assert q.is_path is True
    assert q.is_relative is True

    q = Query('test/test/0:2:')
    assert q.query == 'test/test/0:2:'
    assert q.type is str
    assert q.path == ['test', 'test', slice(0, 2)]
    assert q.is_path is True
    assert q.is_relative is True

    q = Query('test/test/0:10:2')
    assert q.query == 'test/test/0:10:2'
    assert q.type is str
    assert q.path == ['test', 'test', slice(0, 10, 2)]
    assert q.is_path is True
    assert q.is_relative is True

    q = Query('/test/test/1:')
    assert q.query == 'test/test/1:'
    assert q.type is str
    assert q.path == ['test', 'test', slice(1, None)]
    assert q.is_path is True
    assert q.is_relative is False

    q = Query('/test/test/:1')
    assert q.query == 'test/test/:1'
    assert q.type is str
    assert q.path == ['test', 'test', slice(None, 1)]
    assert q.is_path is True
    assert q.is_relative is False

    q = Query('/test/test/::1')
    assert q.query == 'test/test/::1'
    assert q.type is str
    assert q.path == ['test', 'test', slice(None, None, 1)]
    assert q.is_path is True
    assert q.is_relative is False

    q = Query('/test/test/0:2')
    assert q.query == 'test/test/0:2'
    assert q.type is str
    assert q.path == ['test', 'test', slice(0, 2)]
    assert q.is_path is True
    assert q.is_relative is False

    q = Query('/test/test/0:2:')
    assert q.query == 'test/test/0:2:'
    assert q.type is str
    assert q.path == ['test', 'test', slice(0, 2)]
    assert q.is_path is True
    assert q.is_relative is False

    q = Query('/test/test/0:10:2')
    assert q.query == 'test/test/0:10:2'
    assert q.type is str
    assert q.path == ['test', 'test', slice(0, 10, 2)]
    assert q.is_path is True
    assert q.is_relative is False
