from __future__ import annotations
from typing import Union

DEFAULT_DELIMITER: str = '/'
""" The default separator used to join path components into paths. """


class ContextManager:
    """ This class provides a context management interface for Reflective instances. """

    _core: 'RCore'
    """ The parent RCore instance of this instance. """

    _root: any
    """ The reference to the value of the root Reflective instance."""

    _path: list
    """ The path components of the current context. This should be empty for the root instance. """

    _delimiter: str
    """ The delimiter used to join path components into paths. """

    @property
    def core(self) -> 'RCore':
        """ Returns the parent RCore instance of this instance. """
        return self._core

    @core.setter
    def core(self, value: 'RCore') -> None:
        """ Sets the parent RCore instance of this instance. """
        self._core = value

    @property
    def cache(self) -> 'CacheManager':
        """ Returns the cache manager instance associated with the parent RCore instance. """
        return self.core.cache

    @property
    def root(self) -> any:
        """ Returns the reference to the value of the root Reflective instance."""
        return self._root

    @root.setter
    def root(self, value: any) -> None:
        """ Sets the reference to the value of the root Reflective instance."""
        self._root = value

    @property
    def path(self) -> list:
        """ Returns the path components of the current context. This should be empty for the root instance. """
        return self._path

    @path.setter
    def path(self, value: list) -> None:
        """ Sets the path components of the current context. This should be empty for the root instance. """
        self._path = value

    @property
    def ref(self) -> any:
        """ Returns a reference to the parsed value of this context. """
        return self.parse(self.raw)

    @property
    def raw(self) -> any:
        """ Returns a reference to the unparsed value of this context. """
        from functools import reduce
        return reduce(lambda c, k: c[k], self.path, self.root)

    @raw.setter
    def raw(self, value: any) -> None:
        """ Sets the unparsed value of this context. """
        from functools import reduce
        if len(self.path):
            parent = reduce(lambda c, k: c[k], self.path[:-1], self.root)
            original_type = type(parent[self.path[-1]])
            parent[self.path[-1]] = value
        else:
            original_type = type(self.root)
            self.root = value

        # Check if the parsed value type is different then the previous, and invalidate existing cached instance if so
        if type(self.ref) is not original_type and self.cache_key in self.cache:
            self.cache[self.cache_key]().invalidate()
            del self.cache[self.cache_key]

    @property
    def delimiter(self) -> str:
        """ Returns the delimiter used to join path components into paths. """
        return self._delimiter

    @property
    def cache_key(self) -> str:
        """ Builds a cache key for this context instance based on the context path. """
        from reflective.core import RCore

        # Build the hash source value from path components
        source = self.delimiter.join(str(c) for c in self.path)

        # Generate the hash
        return RCore.hash_value(source)

    def __init__(self, core: 'RCore' = None, root: any = None, path: list = None, delimiter: Union[str, None] = None):
        """ Initializes a new ContextManager object associated with the given core. """
        self._core = core
        self._root = root
        self._path = list(path) if path is not None else []
        self._delimiter = delimiter if delimiter is not None else DEFAULT_DELIMITER

    def get(self, path: list) -> 'Reflective':
        """ Returns a singular Reflective instance for the given path, relative to this context. """
        from reflective.core import RCore
        from reflective.types import Reflective

        full_path = self.path + path
        path_key: str = self.delimiter.join(str(c) for c in full_path)
        cache_key: str = RCore.hash_value(path_key)

        # Check if the path is already cached
        if cache_key in self.cache:
            return self.cache[cache_key]

        # Create a new instance and cache a reference to it
        cm = ContextManager(root=self.root, path=full_path)
        cm.core = RCore(context=cm, root=self.core.root, delimiter=self.delimiter)
        self.cache[cache_key] = Reflective(cm.core)

        return self.cache[cache_key]

    def delete(self, path: list = None) -> None:
        """ Deletes the value at the given path, relative to this context. """
        from functools import reduce
        path = self.path + path if isinstance(path, list) else self.path
        reduce(lambda c, k: c[k], path[:-1], self.root).pop(path[-1])
        parent_path = path[:-1]
        parent_core = self.get(path[:-1])() if len(parent_path) else self.core.root()
        cache_key = self.cache_key
        if cache_key in parent_core.cache:
            del parent_core.cache[cache_key]

    def parse(self, value: any, default: any = None) -> any:
        """ Parses the given value for Reflective references, updating the references with values from the root context,
        and returning the updated value reference. """
        import os
        from reflective.util import RUtil

        if isinstance(value, dict):
            return {k: self.parse(v, default) for k, v in value.copy().items()}

        elif isinstance(value, list):
            return [self.parse(item, default) for item in value.copy()]

        elif isinstance(value, tuple):
            return tuple([self.parse(item, default) for item in value])

        if not isinstance(value, str):
            return value

        # Process $(r|e){...} references
        matches = RUtil.ref_pattern.findall(value)

        for match in matches:
            # The part that comes after the "$" and before the "{"
            method = str(match[0]).lower()

            # Handles instances of $(r){...} references
            if method == 'r':
                from reflective.query import QueryResult
                from reflective.types import Reflective
                from reflective.util import RUtil

                # The Reflective query string
                query = match[1]

                qr = self.core.root().query(query)

                if isinstance(qr, QueryResult) and len(qr) or isinstance(qr, Reflective):
                    value = RUtil.update(value, query, qr)

            # Handles instances of $(e){...} references
            elif method == 'e':
                # The environment variable name
                query = match[1]
                query_value = os.getenv(query)
                value = value.replace(f'${match[0]}{{{query}}}', str(query_value))

        return value
