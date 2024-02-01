from __future__ import annotations
from collections import UserList
from typing import Union

DEFAULT_DELIMITER: str = '/'
""" The default separator used to join path components into paths. """


class Query:
    """ This class provides a data object to represent arbitrary queries to Reflective instances. """

    _query: any
    """ The raw query value that the Query object represents. """

    _query_type: type
    """ The type of the raw query value. """

    _query_length: int
    """ The total number of path components in the query. """

    _delimiter: str
    """ The delimiter used to separate query path components. """

    _path: list
    """ The path components of the query. """

    _is_path: bool
    """ Whether the query is a path. """

    _is_relative: bool
    """ Whether the query is relative to the current context. """

    @property
    def query(self) -> any:
        """ Returns the raw query value that the Query object represents. """
        return self._query

    @property
    def type(self) -> type:
        """ Returns the type of the raw query value. """
        return self._query_type

    @property
    def delimiter(self) -> str:
        """ Returns the delimiter used to separate query path components. """
        return self._delimiter

    @property
    def path(self) -> list:
        """ Returns the path components of the query. """
        return self._path

    @property
    def is_path(self) -> bool:
        """ Returns whether the query is a path reference. """
        return self._is_path

    @property
    def is_relative(self) -> bool:
        """ Returns whether the query is relative to the current context. """
        return self._is_relative

    def __init__(self, query: Union[str, int, slice], delimiter: Union[str, None] = None):
        """ Initializes a new Query object, optionally with a delimiter override. """
        import re

        self._query = query
        self._query_type = type(query)
        self._delimiter = delimiter if delimiter is not None else DEFAULT_DELIMITER
        self._is_path = False
        self._is_relative = True
        self._path = []

        if self._query_type in [slice, int]:
            self._is_relative = True
            self._path.append(self._query)
            self._query_length = 1

        if self._query_type is str:
            self._query = self._query.strip()

            # Check if the query is a root path reference
            if self._query.startswith(self._delimiter):
                self._query = self._query[1:]
                self._is_path = True
                self._is_relative = False

            elif self._delimiter in self._query:
                self._is_path = True

            # Break down the query into path components
            self._path = self._query.split(self._delimiter)

            # Analyze and possibly convert the path components into their appropriate types
            for i, component in enumerate(self._path):

                # Convert numerical references to integers
                if component.replace('-', '').isdigit():
                    self._path[i] = int(component)
                    continue

                # Convert slice references to slice objects
                slice_match = re.fullmatch(r'^(-?[0-9]+)?:(-?[0-9]+)?(?::(-?[0-9]+)?)?$', component)

                if slice_match is not None:
                    start = slice_match.group(1)
                    stop = slice_match.group(2)
                    step = slice_match.group(3)

                    if start is not None:
                        start = int(start)

                    if stop is not None:
                        stop = int(stop)

                    if step is not None:
                        step = int(step)

                    self._path[i] = slice(start, stop, step)
                    continue

    def __str__(self):
        """ Returns the string representation of the Query object. """
        return str(self._query)


class QueryResult(UserList):
    """ This class provides a data object to represent the result of a query. It inherently mimics the behavior of
     a list. """

    _query: Query
    """ The query that was executed. """

    @property
    def query(self) -> Query:
        """ Returns the query that was executed. """
        return self._query

    def __init__(self, query: Query, data: list):
        """ Initializes a new QueryResult object. """
        self._query = query
        super().__init__(data)


class QueryManager:
    """ This class provides an interface for executing queries on Reflective instances. """

    _core: 'RCore'
    """ The parent RCore instance of this instance. """

    _delimiter: str
    """ The delimiter used to join path components into paths. """

    @property
    def core(self) -> 'RCore':
        """ Returns the parent RCore instance of this instance. """
        return self._core

    @property
    def cache(self) -> 'CacheManager':
        """ Returns the cache manager instance associated with the parent RCore instance. """
        return self.core.cache

    @property
    def context(self) -> 'ContextManager':
        """ Returns the context manager instance associated with the parent RCore instance. """
        return self.core.context

    @property
    def delimiter(self) -> str:
        """ Returns the delimiter used to join path components into paths. """
        return self._delimiter

    def __init__(self, core: 'RCore', delimiter: Union[str, None] = None):
        """ Initializes a new QueryManager object associated with the given core. """
        self._core = core
        self._delimiter = delimiter if delimiter is not None else DEFAULT_DELIMITER

    def __call__(self, query: Union[str, int, slice, Query], use_cache: bool = False) -> QueryResult:
        """ Executes a query on the bound Reflective instance. """
        return self.query(query, use_cache)

    def query(self, query: Union[str, int, slice, Query], use_cache: bool = False) -> QueryResult:
        """ Executes a query on the bound Reflective instance. """
        from functools import reduce
        from reflective.types import Reflective, RString

        # Convert the query to a Query object if it isn't already
        if type(query) is not Query:
            query = Query(query)

        cache_key = self.build_cache_key(query)

        # If caching is enabled, check if the query is already cached assuming it doesn't end with a slice type
        if use_cache and not type(query.path[-1]) is slice:
            if cache_key in self.cache:
                return self.cache[cache_key]

        if query.type is slice and isinstance(self.context.ref, str):
            return QueryResult(query, [self.context.ref[query.query]])

        results: list = []
        ref: Union['Reflective', None] = None
        found: bool = True
        context = self.core.root().context
        root = context.raw

        if query.is_relative and len(self.core.path):
            root = reduce(lambda c, k: c[k], self.core.path, root)

        try:
            # Reduce the reference based on the query path components.
            ref = reduce(lambda c, k: c[k], query.path, root)
        except (KeyError, TypeError):
            # Could not find a matching reference
            found = False

        if found:
            if type(query.path[-1]) is slice and isinstance(ref, list):
                for item in ref:
                    results.append(item)
            else:
                path = self.core.path + query.path if query.is_relative else query.path
                lookup = context.get(path)
                results.append(lookup)

        if use_cache:
            self.cache[cache_key] = QueryResult(query, results)
            return self.cache[cache_key]

        return QueryResult(query, results)

    def build_cache_key(self, query: Union[str, int, slice, Query]) -> str:
        """ Builds a cache key for the given query. """

        # Convert the query to a Query object if it isn't already
        if type(query) is not Query:
            query = Query(query)

        path = query.path.copy() if query.is_relative else self.context.path + query.path

        for i, component in enumerate(path):
            if type(component) is slice:
                start = component.start if component.start is not None else ''
                stop = component.stop if component.stop is not None else ''
                step = component.step if component.step is not None else ''
                path[i] = f'{start}:{stop}:{step}'

        # Build the cache key base
        source = self.delimiter.join(str(c) for c in path)

        return self.core.hash_value(source)
