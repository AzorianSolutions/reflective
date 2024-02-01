from __future__ import annotations
from typing import Union

DEFAULT_DELIMITER: str = '/'
""" The default separator used to join path components into paths. """


class RCore:
    """ This class provides the internal functionality for Reflective instances."""

    _instance: 'Reflective'
    """ The Reflective instance that this RCore instance is associated with. """

    _root: 'Reflective'
    """ The root Reflective instance that this RCore instance is a descendent of. """

    _cache: 'CacheManager'
    """ The cache manager instance associated with the Reflective instance. """

    _context: 'ContextManager'
    """ The context manager instance associated with the Reflective instance. """

    _query: 'QueryManager'
    """ The query manager instance associated with the Reflective instance. """

    _delimiter: str
    """ The delimiter used to join path components into paths. """

    _invalid: bool
    """ A flag to indicate whether the instance is invalid. """

    @property
    def instance(self) -> 'Reflective':
        """ Returns the Reflective instance that this RCore instance is associated with. """
        return self._instance

    @instance.setter
    def instance(self, value: 'Reflective') -> None:
        """ Sets the Reflective instance that this RCore instance is associated with. """
        self._instance = value

    @property
    def root(self) -> 'Reflective':
        """ Returns the root Reflective instance that this RCore instance is a descendent of. """
        return self._root

    @root.setter
    def root(self, value: 'Reflective') -> None:
        """ Sets the root Reflective instance that this RCore instance is a descendent of. """
        self._root = value

    @property
    def cache(self) -> 'CacheManager':
        """ Returns the cache manager instance associated with the Reflective instance. """
        return self._cache

    @property
    def context(self) -> 'ContextManager':
        """ Returns the context manager instance associated with the Reflective instance. """
        return self._context

    @context.setter
    def context(self, value: 'ContextManager') -> None:
        """ Sets the context manager instance associated with the Reflective instance. """
        self._context = value

    @property
    def query(self) -> 'QueryManager':
        """ Returns the query manager instance associated with the Reflective instance. """
        return self._query

    @property
    def delimiter(self) -> str:
        """ Returns the delimiter used to join path components into paths. """
        return self._delimiter

    @property
    def path(self) -> list:
        """ Returns the path components of the associated context. This should be empty for the root instance. """
        return self.context.path

    @property
    def ref(self) -> any:
        """ Returns a reference to the parsed value of the associated context. """
        return self.context.ref

    @property
    def raw(self) -> any:
        """ Returns a reference to the unparsed value of the associated context. """
        return self.context.raw

    @property
    def json(self) -> str:
        """ Returns the JSON representation of the reference value. """
        return self.to_json()

    @property
    def yaml(self) -> str:
        """ Returns the YAML representation of the reference value. """
        return self.to_yaml()

    def __init__(self, instance: 'Reflective' = None, context: 'ContextManager' = None, root: 'Reflective' = None,
                 delimiter: Union[str, None] = None):
        """ Initializes a new ContextManager object associated with the given core. """
        from reflective.cache import CacheManager
        from reflective.query import QueryManager
        self._instance = instance
        self._context = context
        self._root = root if root is not None else instance
        self._delimiter = delimiter if delimiter is not None else DEFAULT_DELIMITER
        self._invalid = False

        # Initialize the other managers that aren't provided through instantiation.
        self._cache = CacheManager(self) if root is None else root().cache
        self._query = QueryManager(self, delimiter)

    def to_json(self, ref: any = None, flat: bool = True) -> str:
        """ Returns the JSON representation of the given reference, with the option to format the output. """
        import json
        return json.dumps(ref or self.ref, indent=None if flat else 4)

    def to_yaml(self, ref: any = None) -> str:
        """ Returns the YAML representation of the given reference. """
        import yaml
        return yaml.dump(ref or self.ref, indent=4)

    def invalidate(self) -> None:
        """ Invalidates the instance. """
        self._invalid = True

    def enforce_validation(self) -> None:
        """ Enforces validation of the instance. """
        from reflective.exceptions import RInvalidReference
        if self._invalid:
            raise RInvalidReference('This reference is now invalid due to a value type change in the parsed value.')

    @staticmethod
    def hash_value(value: str) -> str:
        """ Builds a hash for the given value. """
        import hashlib
        import json
        return hashlib.md5(json.dumps(str(value)).encode('utf-8')).hexdigest()
