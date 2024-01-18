import re
from typing import Union
from reflective.query import QueryResult, QueryManager

DEFAULT_NAMESPACE: str = 'r_'
""" The default namespace used for the Reflective core in the object dictionary. """

NAMESPACE_KEY: str = '__reflective_namespace'
""" The key used to store the dynamic namespace in the object dictionary. """

PATH_DELIMITERS: list = ['//', '/', '__', '.']
""" The list of separators used to split keys into segments. """

DEFAULT_DELIMITER: str = '/'
""" The default separator used to join keys into paths. """


class RContext(object):
    """ A class that provides a context reference object for Reflective instances. """

    _cache: dict = {}
    """ A dictionary of cached values. """

    _ref: any = None
    """ A reference to the instance value. """

    _root: 'Reflective' or None = None
    """ A reference to the root Reflective instance. """

    _path: str = None
    """ A reference path to the instance value, relative from the root Reflective instance. """

    @property
    def cache(self) -> dict:
        """Returns the cache dictionary."""
        return self._cache

    @cache.setter
    def cache(self, value: dict):
        """Sets the cache dictionary."""
        self._cache = value

    @property
    def ref(self) -> any:
        """Returns the instance value."""
        return self._ref

    @ref.setter
    def ref(self, value: any):
        """Sets the instance value reference."""
        self._ref = value

    @property
    def root(self) -> 'Reflective' or None:
        """Returns the root Reflective instance of the configuration reference."""
        return self._root

    @property
    def path(self) -> str or None:
        """Returns the path (as a delimited string), to the current configuration reference,
        relative to the root Reflective instance, or None if this context is for the root instance."""
        return self._path

    @property
    def is_root(self) -> bool:
        """Returns whether this context is for the root Reflective instance."""
        return self._root is None

    def __init__(self, ref: any, root: 'Reflective' = None, path: str = None):
        self._cache = {}
        self._ref = ref
        self._root = root
        self._path = path


class RCore:
    """ A class that provides the internal core functionality for Reflective instances. """

    _instance: 'Reflective'
    """ A reference to the Reflective instance for this RCore object. """

    _ref_pattern = re.compile(r'\$(r|e){([a-z0-9_/.]+)}', re.IGNORECASE)
    """ The regular expression pattern used to match variable references in values. """

    _delimiter: str = DEFAULT_DELIMITER
    """ The delimiter used to join keys into paths. """

    _parse: bool = True
    """ Whether to parse values for variable references. """

    _context: RContext or None = None
    """ A reference to the ReflectiveContext object for this Reflective instance. """

    _config: dict = {}
    """ A reference to the ReflectiveConfig object for this Reflective instance. """

    _query_manager: QueryManager
    """ A reference to the QueryManager object for this Reflective instance. """

    _valid: bool = True
    """ Tracks whether this instance is a valid representation of the underlying data. """

    @property
    def instance(self) -> 'Reflective':
        """Returns a reference to the Reflective instance for this RCore object."""
        return self._instance

    @property
    def context(self) -> RContext or None:
        """Returns the ReflectiveContext object for this Reflective instance."""
        return self._context

    @property
    def config(self) -> dict:
        """Returns the ReflectiveConfig object for this Reflective instance."""
        return self._config

    @property
    def qm(self) -> QueryManager:
        """Returns the QueryManager object for this Reflective instance."""
        return self._query_manager

    @property
    def cache(self) -> dict:
        """Returns the cache dictionary."""
        return self._context.cache

    @cache.setter
    def cache(self, value: dict):
        """Sets the cache dictionary."""
        self._context.cache = value

    @property
    def root(self) -> 'Reflective' or None:
        """Returns the root Reflective instance of the object."""
        if 'root' in self.cache:
            return self.cache['root']
        ref = self._instance
        while ref().context.root:
            ref = ref().context.root
        self.cache['root'] = ref
        return ref

    @property
    def ref(self) -> any:
        """ Returns the instance value, parsed for references if enabled, and as the appropriate Reflective type if a
        sole reference is found. """
        if self.parse:
            return self.follow(self.context.ref)
        return self.context.ref

    @property
    def raw(self) -> any:
        """ Returns the raw instance value, without parsing for references. """
        return self.context.ref

    @property
    def cache_key(self) -> int:
        """Returns the cache key (as a hash of the path key), for the current configuration reference,
        relative to the root object."""
        if 'cache_key' not in self.context.cache:
            import hashlib
            import json
            self.context.cache['cache_key'] = hashlib.md5(json.dumps(self.context.path).encode('utf-8')).hexdigest()
        return self.context.cache['cache_key']

    @property
    def path(self) -> str:
        """Returns the path (as a delimited string), to the current configuration reference,
        relative to the root object."""
        return self.context.path

    @property
    def path_list(self) -> list:
        """Returns the path (as a list), to the current configuration reference, relative to the root object."""
        if 'path_list' not in self.context.cache:
            self.context.cache['path_list'] = self.context.path.split(self._delimiter) if self.context.path else []
        return self.context.cache['path_list']

    @property
    def delimiter(self) -> str:
        """Returns the delimiter used to join keys into paths."""
        return self._delimiter

    @property
    def parse(self) -> bool:
        """Returns whether to parse values for variable references."""
        return self._parse

    @parse.setter
    def parse(self, value: bool):
        """Sets whether to parse values for variable references."""
        self._parse = value

    @property
    def valid(self) -> bool:
        """Returns whether this instance is a valid representation of the underlying data."""
        return self._valid

    @property
    def json(self) -> str:
        """ Returns the JSON representation of the reference value. """
        return self.to_json()

    @property
    def yaml(self) -> str:
        """ Returns the YAML representation of the reference value. """
        return self.to_yaml()

    def __init__(self, instance: 'Reflective', context: RContext, config: dict = None):
        self._instance = instance
        self._context = context
        self._config = config
        self._query_manager = QueryManager(self._instance)

    def to_json(self, ref: any = None, flat: bool = True) -> str:
        """ Returns the JSON representation of the given reference, with the option to format the output. """
        import json
        return json.dumps(ref or self.ref, indent=None if flat else 4)

    def to_yaml(self, ref: any = None) -> str:
        """ Returns the YAML representation of the given reference. """
        import yaml
        return yaml.dump(ref or self.ref, indent=4)

    def query(self, query: any, default: any = None) -> 'Reflective':
        from functools import reduce

        is_slice = isinstance(query, slice)
        is_empty_slice = is_slice and query.start is None and query.stop is None and query.step is None
        key = query

        if is_slice:
            key = f'{query.start}:{query.stop}:{query.step}'

        cache_key = self.cache_key_plus(key)

        if cache_key in self.cache:
            return self.cache[cache_key]

        if is_slice or isinstance(query, int):
            ref = self.context.ref

            if isinstance(ref, str) or isinstance(ref, list) or isinstance(ref, tuple):
                ref = self.context.ref[query]
            elif is_slice and is_empty_slice:
                ref = self.context.ref

            # Create and return a new Reflective instance of the appropriate type based on the reduced reference.
            return Reflective(RContext(
                ref,
                root=self.root,
                path=self.path_plus(key)
            ))

        if isinstance(query, str):
            ref = self.context.ref
            path = self.path_plus(query)

            # Change to the root context if the query starts with the delimiter.
            if query.startswith(self.delimiter):
                query = query[1:]
                ref = self.root().context.ref
                path = query

            # Split the query into segments.
            segments = query.split(self.delimiter)

            try:
                # Reduce the reference based on the query segments.
                ref = reduce(RCore.util_get_item, segments, ref)

                # Create and return a new Reflective instance of the appropriate type based on the reduced reference.
                return Reflective(RContext(
                    ref,
                    root=self.root,
                    path=path,
                ))

            except (KeyError, TypeError):
                # Could not find a matching reference, so continue on to the default handling
                pass

        results = []

        if results:
            self.cache[cache_key] = Reflective(results)
            return self.cache[cache_key]
        else:
            self.cache[cache_key] = Reflective(default)

        return self.cache[cache_key]

    def extract(self, value: str) -> list:
        """ Extracts the Reflective reference strings from the given string and returns them as a list of strings."""

        references: list = []

        # Process $(r|e){...} references
        matches = self._ref_pattern.findall(value)

        for match in matches:
            # Handles instances of $(r){...} references
            if str(match[0]).lower() == 'r':
                # Capture the Reflective query string
                references.append(match[1])

        return references

    def follow(self, value: any, default: any = None) -> any:
        """ Parses the given value for Reflective references, updating the references with values from the root context,
        and returning the updated value reference. """
        import os

        if isinstance(value, dict):
            return {k: self.follow(v, default) for k, v in value.copy().items()}

        elif isinstance(value, list):
            return [self.follow(item, default) for item in value.copy()]

        elif isinstance(value, tuple):
            return tuple([self.follow(item, default) for item in value])

        if not isinstance(value, str):
            return value

        # Process $(r|e){...} references
        matches = self._ref_pattern.findall(value)

        for match in matches:
            # The part that comes after the "$" and before the "{"
            method = str(match[0]).lower()

            # Handles instances of $(r){...} references
            if method == 'r':
                # The Reflective query string
                query = match[1]
                query_value = self.root().query(query, default)
                query_pattern = f'${match[0]}{{{query}}}'

                # Provide typed references when sole references are found
                if value.replace(query_pattern, '').strip() == '':
                    return query_value

                # Update the string value with the query value
                value = value.replace(query_pattern, str(query_value))

            # Handles instances of $(e){...} references
            elif method == 'e':
                # The environment variable name
                query = match[1]
                query_value = os.getenv(query)
                value = value.replace(f'${match[0]}{{{query}}}', str(query_value))

        return value

    def path_plus(self, key: str) -> str:
        """ Returns a new path string with the given key appended. """
        return self._delimiter.join([self.path, str(key)]) if self.path else str(key)

    def cache_key_plus(self, key: str) -> int:
        """ Returns a new cache key with the given key appended. """
        return hash(self.path_plus(key))

    def invalidate(self):
        """ Invalidates the current instance and all cached instances. """
        self._valid = False

    def enforce_validation(self):
        from reflective.exceptions import RInvalidReference
        """ Enforces a proper validation state by raising an RInvalidReference exception if the instance is invalid. """
        if not self.valid:
            raise RInvalidReference(f'Reference Invalidated: {self.path}')

    @staticmethod
    def is_list_index(item: str or int or slice) -> bool:
        """ Determines if the given item is a list index reference. """
        if isinstance(item, int) or isinstance(item, slice):
            return True
        try:
            int(item.replace('-', '').replace(':', ''))
            return True
        except ValueError:
            return False

    @staticmethod
    def get_reference(value: any):
        if isinstance(value, RContext):
            value = value.ref

        if isinstance(value, RCore):
            value = value.context.ref

        if isinstance(value, Reflective):
            value = value().context.ref

        return value

    @staticmethod
    def update_reference(ref: any, value: any):
        if isinstance(ref, Reflective):
            ref().context.ref = value

        elif isinstance(ref, RCore):
            ref.context.ref = value

        elif isinstance(ref, RContext):
            ref.ref = value

    @staticmethod
    def get_type_class(value: any):
        """ Returns the appropriate Reflective type class for the given value. """
        from reflective.types import RDict, RList, RTuple, RBool, RInt, RFloat, RComplex, RString, RNone

        if isinstance(value, dict) or value == {}:
            return RDict

        if isinstance(value, list) or value == []:
            return RList

        if isinstance(value, tuple):
            return RTuple

        if isinstance(value, bool):
            return RBool

        if isinstance(value, int):
            return RInt

        if isinstance(value, float):
            return RFloat

        if isinstance(value, complex):
            return RComplex

        if isinstance(value, str):
            return RString

        if value is None:
            return RNone

        return Reflective

    @staticmethod
    def get_list_value(value: any) -> list:
        """ Returns the appropriate list value for the given value. """
        from collections import UserList
        if value is None:
            raise ValueError('Cannot convert None to list.')
        if type(value) is type([]):
            return value
        elif isinstance(value, UserList):
            return value.data[:]
        return list(value)

    @staticmethod
    def get_string_value(value: any) -> str:
        """ Returns the appropriate string value for the given value. """
        from collections import UserString
        if isinstance(value, str):
            return value
        if isinstance(value, UserString):
            return value.data[:]
        return str(value)

    @staticmethod
    def util_get_item(c, k) -> any:
        """ Reduces the given reference based on the given key, safely handling numerical index references. """
        if isinstance(k, int) or str(k).isnumeric():
            return c[int(k)]
        return c[k]


class Reflective:
    """ A class that provides an advanced interface for working with data structures. """

    def __new__(cls, ref: any):
        """ Creates a new Reflective instance of the appropriate type, using the given reference as the value. """

        # Pass-through instantiations that are not for the core Reflective class.
        if f'{cls.__module__}.{cls.__name__}' != 'reflective.core.Reflective':
            return super().__new__(cls)

        # Specifically handle instantiations of the core Reflective class to ensure the correct type is returned.
        type_class = RCore.get_type_class(ref)
        type_value = RCore.get_reference(ref)

        return type_class.__new__(type_class, type_value)

    def __init__(self, ref: any, namespace: str = DEFAULT_NAMESPACE):
        # Set the namespace of the Reflective core
        self.__dict__[NAMESPACE_KEY] = namespace

        # Allow instances of the Reflective to be passed in as the ref argument.
        if isinstance(ref, Reflective):
            ref_ns = ref.__dict__[NAMESPACE_KEY]
            self.__dict__[namespace] = RCore(self, ref.__dict__[ref_ns])
            return

        # Allow instances of the RCore to be passed in as the ref argument.
        if isinstance(ref, RCore):
            self.__dict__[namespace] = ref
            return

        # Allow instances of the ReflectiveContext to be passed in as the ref argument.
        if isinstance(ref, RContext):
            self.__dict__[namespace] = RCore(self, ref)
            return

        # Handle direct references to data values.
        self.__dict__[namespace] = RCore(self, RContext(ref))

    def __enter__(self) -> 'Reflective':
        """ Returns a new Reflective instance of the appropriate type, using the current instance context. """
        self().enforce_validation()
        return Reflective(self())

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def __call__(self, *args, **kwargs) -> Union['Reflective', 'RCore', QueryResult, any]:
        namespace = self.__dict__[NAMESPACE_KEY]
        core = self.__dict__[namespace]
        core.enforce_validation()

        # Return the reference to the RCore instance if no arguments are passed in.
        if not len(args):
            return core

        # Return the underlying value reference if a single empty string is passed in.
        if len(args) == 1 and str(args[0]).strip() == '':
            return core.context.ref

        qr: QueryResult = core.qm(args[0])

        if len(qr) == 1:
            return qr[0]

        return qr

    def __getattr__(self, key: str) -> 'Reflective':
        from reflective.types import RString

        self().enforce_validation()

        cache_key = self().cache_key_plus(key)

        # Handle scenarios where the item is already cached.
        if cache_key in self().cache:
            cache_item = self().cache[self().cache_key_plus(key)]

            # Provide pass-through reference typing where the cached item value is a sole Reflective reference
            if type(cache_item) is RString:
                refs = self().extract(cache_item().context.ref)
                if len(refs) == 1:
                    return self().query(refs[0])

            return cache_item

        # Handle scenarios where the instance is a dictionary and the item is in the relative context.
        if isinstance(self().context.ref, dict) and key in self().context.ref:
            self().cache[cache_key] = Reflective(RContext(
                self().context.ref[key],
                root=self().root,
                path=self().path_plus(key)
            ))
            return self().cache[cache_key]

        raise AttributeError(f'<{self.__class__.__name__}> Attribute "{key}" does not exist.')

    def __setattr__(self, key, value) -> None:
        self().enforce_validation()

        # Update the underlying value reference.
        self().context.ref[key] = value

        # Update the reference value for existing cached instances, or invalidate them on type change.
        cache_key = self().cache_key_plus(key)

        if cache_key in self().cache:
            cache_item = self().cache[cache_key]
            cache_core = cache_item.__dict__[cache_item.__dict__[NAMESPACE_KEY]]

            # Check if the data type has changed for the cached item and invalidate if necessary.
            cache_type = cache_core.get_type_class(cache_item)
            value_type = cache_core.get_type_class(value)

            # Invalidate the cache item if it's type doesn't match the type that would be used for the new value.
            if cache_type != value_type:
                cache_core.invalidate()
                del self().cache[cache_key]

            # Update the invalidated cache item either way to ensure its reference is up-to-date.
            cache_core.context.ref = value

    def __delattr__(self, key: str) -> None:
        self().enforce_validation()

        # Invalidate the reference value for existing cached instances.
        cache_key = self().cache_key_plus(key)

        if cache_key in self().cache:
            cache_item = self().cache[cache_key]
            cache_core = cache_item.__dict__[cache_item.__dict__[NAMESPACE_KEY]]
            cache_core.invalidate()
            del self().cache[cache_key]

        del self().context.ref[key]

    def __getitem__(self, item: str or int or slice) -> Union['Reflective', QueryResult]:
        from reflective.types import RString

        self().enforce_validation()

        if isinstance(item, str) and item.strip() == '':
            return self().context.ref

        item_type = type(item)
        cache_item = item

        if item_type is slice:
            cache_item = f'{item.start}:{item.stop}:{item.step}'

        cache_key = self().cache_key_plus(cache_item)

        # Handle scenarios where the item is already cached.
        if cache_key in self().cache:
            cache_ref = self().cache[cache_key]

            # Provide pass-through reference typing where the cached item value is a sole Reflective reference
            if type(cache_ref) is RString:
                refs = self().extract(cache_ref().context.ref)
                if len(refs) == 1:
                    return self().query(refs[0])

            return cache_ref

        # Handle scenarios where the instance is a dictionary and the item is in the relative context.
        if item_type is not slice and isinstance(self().context.ref, dict) and item in self().context.ref:
            self().cache[cache_key] = Reflective(RContext(
                self().context.ref[item],
                root=self().root,
                path=self().path_plus(item)
            ))
            return self().cache[cache_key]

        # Handle scenarios where the instance is a list and the item meets the criteria of a list index.
        if (isinstance(self().context.ref, list) or isinstance(self().context.ref, tuple)) \
                and RCore.is_list_index(item):
            self().cache[cache_key] = Reflective(RContext(
                self().context.ref[item],
                root=self().root,
                path=self().path_plus(item)
            ))
            return self().cache[cache_key]

        # No other scenarios matched, so query with the item.
        self().cache[cache_key] = self().query(item)

        return self().cache[cache_key]

    def __setitem__(self, item, value) -> None:
        # Pass-through assignments for internal storage
        if item == NAMESPACE_KEY or (NAMESPACE_KEY in self.__dict__ and item == self.__dict__[NAMESPACE_KEY]):
            self.__dict__[item] = value
            return

        self().enforce_validation()

        # Update the underlying value reference.
        self().context.ref[item] = value

        # Update the reference value for existing cached instances, or invalidate them on type change.
        cache_key = self().cache_key_plus(item)

        if cache_key in self().cache:
            cache_item = self().cache[cache_key]
            cache_core = cache_item.__dict__[cache_item.__dict__[NAMESPACE_KEY]]

            # Check if the data type has changed for the cached item and invalidate if necessary.
            cache_type = cache_core.get_type_class(cache_item)
            value_type = cache_core.get_type_class(value)

            # Invalidate the cache item if it's type doesn't match the type that would be used for the new value.
            if cache_type != value_type:
                cache_core.invalidate()
                del self().cache[cache_key]

            # Update the invalidated cache item either way to ensure its reference is up-to-date.
            cache_core.context.ref = value

    def __delitem__(self, item: Union[str, int, slice]) -> None:
        self().enforce_validation()

        item_type = type(item)
        cache_item = item

        if item_type is slice:
            cache_item = f'{item.start}:{item.stop}:{item.step}'

        # Invalidate the reference value for existing cached instances.
        cache_key = self().cache_key_plus(cache_item)

        if cache_key in self().cache:
            cache_item = self().cache[cache_key]
            cache_core = cache_item.__dict__[cache_item.__dict__[NAMESPACE_KEY]]
            cache_core.invalidate()
            del self().cache[cache_key]

        del self().context.ref[item]

    def __repr__(self) -> str:
        self().enforce_validation()
        return self().ref.__repr__()

    def __str__(self) -> str:
        self().enforce_validation()
        return str(self().ref)

    def __instancecheck__(self, instance):
        self().enforce_validation()
        return isinstance(self().context.ref, instance)

    def __eq__(self, other: any) -> bool:
        self().enforce_validation()
        if isinstance(other, Reflective):
            return self().ref == other().ref
        return self().ref == other

    def __ne__(self, other: any) -> bool:
        self().enforce_validation()
        if isinstance(other, Reflective):
            return self().ref != other().ref
        return self().ref != other

    def __len__(self) -> int:
        self().enforce_validation()
        return len(self().ref)
