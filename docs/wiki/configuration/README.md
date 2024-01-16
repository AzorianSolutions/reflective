# Reflective

## Configuration Guide

### Table of Contents

- [Path Delimiter Configuration](#delimiter-configuration)
- [Namespace Configuration](#namespace-configuration)
- [Dynamic Reference Configuration](#dynamic-reference-configuration)

### Path Delimiter Configuration

By default, Reflective uses the `/` character as the path delimiter. This can be changed if this character is not
suitable for your use case. The default value is defined in `reflective.core.DEFAULT_DELIMITER`.

### Namespace Configuration

By default, Reflective uses the `__reflective_namespace` key to store a reference in the instance dictionary
to the RCore instance associated with the object. This can be changed if this value is not suitable
for your use case. The default value is defined in `reflective.core.NAMESPACE_KEY`

### Dynamic Reference Configuration

By default, Reflective enables parsing of dynamic references. This can be disabled if this feature is not suitable for
your use case.

```python
from reflective import Reflective

r = Reflective({})
r().parse = False
```
