from typing import Union

DEFAULT_DELIMITER = '/'


class Query:
    """ This class provides a data object to represent arbitrary queries to Reflective instances. """

    _query: any
    """ The raw query value that the Query object represents. """

    _query_type: type
    """ The type of the raw query value. """

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
                slice_match = re.fullmatch(r'^(\-?[0-9])?\:(\-?[0-9])?(?:\:(\-?[0-9])?)?$', component)

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


class QueryResult:
    pass


class QueryManager:
    pass
