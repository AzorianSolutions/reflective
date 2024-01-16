# Reflective

## Library Features

The purpose of this document is to provide an in-depth look at the features of the library. This document is intended
to be used as a reference for the library's features.

### Table of Contents

- [Data Access](#data-access)
- [Data Manipulation](#data-manipulation)
- [Data Serialization](#data-serialization)
- [Data Typing](#data-typing)
- [Dynamic References](#dynamic-references)

### Data Access

Reflective provides a simple interface for accessing data in a data structure. At the most simple form, you can access
data in a data structure by using the `Reflective` class:

```python
from reflective import Reflective

data = {
    'key': 'value'
}

r = Reflective(data)

print( r.key )  # value
print( r['key'] )  # value
print( r('key') )  # value
```

Given that Reflective objects mimic their underlying data types, you can access data in a composite value using the
typical accessors of the underlying data type as well as leverage new avenues of access through the use of properties
and methods:

```python
from reflective import Reflective

data = {
    'str': 'value',
    'dict': {
        'key': 'value'
    },
    'list': [1, 2, 3, 4]
}

r = Reflective(data)

print( r.str[0:3] ) # val
print( r.dict.key )  # value
print( r['dict']['key'] )  # value
print( r('dict')('key') )  # value
print( r.list[0] )  # 1
print( r.list(0) ) # 1
```

Another useful feature of the access interface is that you can access data by relative or root path:

```python
from reflective import Reflective

data = {
    'app': {
        'name': 'My App',
        'tags': ['tag1', 'tag2'],
        'authors': [
            {
                'name': 'John Doe',
                'email': 'john.doe@whereswaldo.com',
            },
            {
                'name': 'Jane Doe',
                'email': 'jane.doe@whereswaldo.com',
            }
        ]
    }   
}

r = Reflective(data)

print( r('app/name') )  # My App
print( r('app/tags/0') )  # tag1
print( r('app/authors/0') )  # {'name': 'John Doe', 'email': 'john.doe@whereswaldo.com'}

print( r['app/authors/0/name'] )  # John Doe
print( r('app/authors')[1].name )  # Jane Doe
print( r('app/authors')(1)('email') )  # jane.doe@whereswaldo.com
print( r.app.authors[0]('/app/tags/0') )  # tag1
```

### Data Manipulation

Updating composite data structures can be a pain with dictionaries and lists in some cases. Reflective makes updating
composite data structures just as easy as it makes reading them. You can update data in a data structure by using the
native syntax already available to the associated data types. Additionally, just as you can access data by object
properties, you can also update data by object properties:

```python
from reflective import Reflective

data = {
    'str': 'value',
    'dict': {
        'key': 'value'
    },
    'list': [1, 2, 3, 4]
}

r = Reflective(data)

r.str = 'new value'
r.dict.key = 'new value'
r.list[0] = 5

print( r.str )  # new value
print( r.dict.key )  # new value
print( r.list[0] )  # 5
```

In a **future release**, you will also be able to update data by relative or root path:

```python
from reflective import Reflective

data = {
    'app': {
        'name': 'My App',
        'tags': ['tag1', 'tag2'],
        'authors': [
            {
                'name': 'John Doe',
                'email': 'john.doe@whereswaldo.com',
            },
            {
                'name': 'Jane Doe',
                'email': 'jane.doe@whereswaldo.com',
            }
        ]
    }
}

r = Reflective(data)

r['app/name'] = 'My New App'
r('app/name', 'My New App')

r['app/tags/0'] = 'new tag'
r('app/tags/0', 'new tag')

r['app/authors/0/email'] = 'john.doe@gmail.com'
r('app/authors/0/email', 'john.doe@gmail.com')

r('app/authors')(1)('email', 'jane.doe@gmail.com')

r.app.authors[0]['/app/tags/0'] = 'new tag'
r.app.authors[0]('/app/tags/0', 'new tag')

print( r('app/name') )  # My New App
print( r('app/tags/0') )  # new tag
print( r('app/authors/0/email') )  # john.doe@gmail.com
print( r('app/authors')(1)('email') )  # jane.doe@gmail.com
print( r.app.authors[0]('/app/tags/0') )  # new tag
```

### Data Serialization

Reflective provides a simple interface for serializing data structures to and from JSON and YAML. The `RCore`
class provides the `to_json` and `to_yaml` methods for serializing data structures to JSON and YAML respectively.
The `RCore` class also provides the `json` and `yaml` properties for accessing the serialized
JSON and YAML representations of the underlying data structure using the `to_json` and `to_yaml` methods respectively.

```python
from reflective import Reflective

data = {
    'key': 'value'
}

r = Reflective(data)

print( r().to_json(flatten=True) ) # {"key": "value"}
print( r().to_yaml() ) # key: value

print( r().json ) # {"key": "value"}
print( r().yaml ) # key: value
```

### Data Typing

Reflective achieves a number of it's key features ultimately through the use of subclassed data types. So for each data
type that Reflective supports, there will be a corresponding subclassed data type available in the `reflective.types`
package.

The `Reflective` class will automatically detect the data type of the input value and instantiate the
corresponding subclassed data type. These subclassed data types provide full compatibility with the native data types
which they override.

This means that you can use the subclassed data types in place of the native data types and everything will
work as expected.

```python
from reflective import Reflective

data = {
    'str': 'My Test String',
    'int': 123,
    'float': 123.456,
    'complex': 123+456j,
    'bool': True,
    'none': None,
    'dict': {'a': 1, 'b': 2, 'c': 3, 'd': 4},
    'list': [1, 2, 3, 4],
    'tuple': (1, 2, 3, 4),
}

r = Reflective(data)

print( type(r.str) ) # <class 'reflective.types.string.RString'>
print( type(r.int) ) # <class 'reflective.types.numeric.RInt'>
print( type(r.float) ) # <class 'reflective.types.numeric.RFloat'>
print( type(r.complex) ) # <class 'reflective.types.numeric.RComplex'>
print( type(r.bool) ) # <class 'reflective.types.simple.RBool'>
print( type(r.none) ) # <class 'reflective.types.simple.RNone'>
print( type(r.dict) ) # <class 'reflective.types.dict.RDict'>
print( type(r.list) ) # <class 'reflective.types.list.RList'>
print( type(r.tuple) ) # <class 'reflective.types.tuple.RTuple'>

assert isinstance(r.str, str) # True
assert isinstance(r.int, int) # True
assert isinstance(r.float, float) # True
assert isinstance(r.complex, complex) # True
assert isinstance(r.bool, bool) # True
assert isinstance(r.none, type(None)) # True
assert isinstance(r.dict, dict) # True
assert isinstance(r.list, list) # True
assert isinstance(r.tuple, tuple) # True
```

If you ever need to access the underlying value reference for direct testing, you can use the `ref` property of the
associated `RCore` instance:

```python
from reflective import Reflective

data = {
    'key': 'value'
}

r = Reflective(data)

print( r().ref ) # {'key': 'value'}
print( r.key().ref ) # value
```

This is especially useful because bool and None values are essentially singletons in Python. This means that for
cases where the value reference is to a bool or None value, the `ref` property will have to be used to perform direct
comparison using the `is` and `is not` operators.

```python
from reflective import Reflective

data = {
    'bool': True,
    'none': None,
}

r = Reflective(data)

print( r.bool is True ) # False
print( r.bool().ref is True ) # True
print( r.none is None ) # False
print( r.none().ref is None ) # True
```

**Notice!** You should make sure to read about the [Dynamic References](#dynamic-references) feature before using the
`ref` property. The `ref` property is a dynamic reference and will change as the underlying reference value changes.
If you need to access the raw value of the underlying value reference, you should use the `raw` property of the
associated `RCore` instance to avoid the use of dynamic references.

```python
from reflective import Reflective

data = {
    'int': 123,
    'reference': '$r{int}',
}

r = Reflective(data)

print( r.reference().raw ) # $r{int}
print( type(r.reference().raw) ) # <class 'str'>
```

### Dynamic References

Reflective provides the ability to use special reference syntax to dynamically reference other values in the data
structure. This is useful for a plethora of reasons which I will not go into here.

The dynamic reference feature currently supports two types of references:

- **Value References** - These references are used to reference the value of another path in the composite structure.
- **Environment Variable References** - These references are used to reference the value of an environment variable.

#### Value References

The syntax for referencing other
values in the data structure is `$r{path}`. The `path` is relative in the data structure to the value which the path
is applied through.

The `path` can be made relative to the root of the data structure by prefixing the path with the configured delimiter.
For more information on this setting, please see the [Configuration Guide](../configuration/README.md).

```python
from reflective import Reflective

data = {
    'dict': {'a': 1, 'b': '$r{d/key}', 'c': 3, 'd': {'key': 123.456}},
    'reference': '$r{/dict/a}',
}

r = Reflective(data)

print( r.reference() ) # 1
print( type(r.reference()) ) # <class 'int'>

print( r.reference().raw ) # $r{/dict/a}
print( type(r.reference().raw) ) # <class 'str'>

print( r.dict('a') ) # 1
print( r.dict.b ) # 123.456
print( type(r.dict.b) ) # <class 'reflective.types.numeric.RFloat'>
print( r.dict.a('/reference') ) # 1
print( r.dict.a('/reference').raw ) # $r{/dict/a}
```

#### Environment Variable References

The syntax for referencing environment variables is `$e{VAR_NAME}`. The `VAR_NAME` is the name of the environment
variable to reference.

```python
from reflective import Reflective

data = {
    'shell': '$e{SHELL}',
}

r = Reflective(data)

print( r.shell ) # /bin/bash
```
