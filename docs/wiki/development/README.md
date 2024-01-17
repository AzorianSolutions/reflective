# Reflective

## Development Guide

Eventually a more in-depth development guide of the library will be here but this will have to do for now.

### Design

The way the Reflective library works, is that it subclasses the core Python data types and adds an `RCore` instance
to each of them. From there, the relevant dunder methods such as `__new__` and `__init__` are overridden by the
core `Reflective` class / data type subclass, and proxied through to the `RCore` instance. The `RCore` class keeps
track of an object's underlying value reference, as well as it's place in the object graph. Additionally, it provides
the actual functionality for traversing and manipulating the object graph.

So essentially, each value reference from an instantiated `Reflective` object is an instance
of `reflective.core.Reflective` which is the super type of all the data type subclasses in `reflective.types`.
This is how the library allows the user to interact with the object graph in a natural way, while still maintaining
the ability to perform custom operations against the context of each reference. Instances of the `Reflective` class
are callable, which provides the ability to access the associated `RCore` instance of any value reference just by
calling it without any arguments.

Take the following example:

```python
from reflective import Reflective

r = Reflective({'test': 'value'})

r()  # Returns the associated RCore instance for the top-level dictionary
r.test() # Returns the associated RCore instance for the 'test' key in the top-level dictionary
```

### Environment Set Up

To set up your environment to perform changes to the Reflective code-base, run the following commands in your terminal:

```bash
python3 -m pip install --upgrade git+
git clone https://github.com/AzorianSolutions/reflective.git
cd reflective
git checkout dev
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -e .
```
