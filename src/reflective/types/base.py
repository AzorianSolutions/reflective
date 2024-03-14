from typing import Union
from reflective.core import RCore
from reflective.query import QueryResult

DEFAULT_NAMESPACE: str = 'r_'
""" The default namespace used for the Reflective core in the object dictionary. """

NAMESPACE_KEY: str = '__reflective_namespace'
""" The key used to store the dynamic namespace in the object dictionary. """


class Reflective:
    """ This is the base class for all Reflective value type instances. """

    def __new__(cls, ref: any):
        """ Creates a new Reflective instance of the appropriate type, using the given reference as the value. """
        from reflective.util import RUtil

        # Pass-through instantiations that are not for the core Reflective class.
        if cls is not Reflective:
            return super().__new__(cls)

        # Specifically handle instantiations of the core Reflective type class to ensure the correct type is returned.
        type_value = RUtil.get_reference(ref)
        type_class = RUtil.get_type_class(type_value)

        return type_class.__new__(type_class, type_value)

    def __init__(self, ref: any, namespace: Union[str, None] = None):
        """ Initializes a new Reflective instance of the appropriate type, using the given reference as the value. """
        from reflective.core import RCore
        from reflective.context import ContextManager

        if namespace is None:
            namespace = DEFAULT_NAMESPACE

        # Set the namespace of the Reflective core
        self.__dict__[NAMESPACE_KEY] = namespace

        # Allow instances of the RCore to be passed in as the ref argument.
        if isinstance(ref, RCore):
            ref.instance = self
            self.__dict__[namespace] = ref
            return

        # Allow instances of the ContextManager to be passed in as the ref argument.
        if isinstance(ref, ContextManager):
            self.__dict__[namespace] = RCore(instance=self, context=ref)
            return

        # Handle direct references to data
        inst = RCore(instance=self)
        inst.context = ContextManager(core=inst, root=ref)

        self.__dict__[namespace] = inst

    def __call__(self, *args, **kwargs) -> Union[RCore, 'Reflective', QueryResult, any]:
        from reflective.query import Query

        namespace = self.__dict__[NAMESPACE_KEY]
        core = self.__dict__[namespace]
        total_args = len(args)

        # Ensure that this reference is valid
        core.enforce_validation()

        # Return the reference to the RCore instance if no arguments are passed in.
        if not total_args:
            return core

        query = args[0]

        # Return the underlying value reference if a single empty string is passed in.
        if total_args == 1 and str(query).strip() == '':
            return core.context.ref

        query = Query(query)
        qr: QueryResult = core.query(query)

        # Handle query only scenarios
        if total_args == 1:
            if len(qr) == 1:
                return qr[0]
            return qr

        # Handle query update scenarios
        value = args[1]

        if len(qr):
            for result in qr:
                result().context.raw = value
            return True

        # If the references to be set don't already exist, create them in the parent context
        else:
            parent_path = core.path + query.path[:-1]
            key = query.path[-1]

            # Handle non-root paths
            if len(parent_path):
                parent = core.root().context.get(parent_path)
                parent().context.raw[key] = value

            # Handle root paths
            else:
                core.root().context.raw[key] = value

        return None

    def __getattr__(self, item):
        # Ensure that this reference is valid
        self().enforce_validation()

        qr = self(item)
        if isinstance(qr, Reflective):
            return qr
        if not len(qr):
            raise AttributeError(f'<{self.__class__.__name__}> The attribute "{item}" does not exist.')
        return qr

    def __setattr__(self, key, value):
        # Ensure that this reference is valid
        self().enforce_validation()
        self(key, value)

    def __delattr__(self, item):
        # Ensure that this reference is valid
        self().enforce_validation()
        qr = self(item)
        if isinstance(qr, Reflective):
            qr().context.delete()
            return
        for result in self(item):
            result().context.delete()

    def __getitem__(self, item):
        # Ensure that this reference is valid
        self().enforce_validation()
        return self(item)

    def __setitem__(self, item, value):
        # Ensure that this reference is valid
        self().enforce_validation()
        # Pass-through assignments for internal storage
        if item == NAMESPACE_KEY or (NAMESPACE_KEY in self.__dict__ and item == self.__dict__[NAMESPACE_KEY]):
            self.__dict__[item] = value
            return

        self(item, value)

    def __delitem__(self, item):
        # Ensure that this reference is valid
        self().enforce_validation()
        qr = self(item)
        if isinstance(qr, Reflective):
            qr().context.delete()
            return
        for result in self(item):
            result().context.delete()

    def __enter__(self) -> 'Reflective':
        """ Returns a reference to the RCore instance bound to this Reflective instance. """
        # Ensure that this reference is valid
        self().enforce_validation()
        return self()

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def __repr__(self) -> str:
        # Ensure that this reference is valid
        self().enforce_validation()
        return self().ref.__repr__()

    def __str__(self) -> str:
        # Ensure that this reference is valid
        self().enforce_validation()
        return str(self().ref)

    def __instancecheck__(self, instance):
        # Ensure that this reference is valid
        self().enforce_validation()
        return isinstance(self().context.ref, instance)

    def __eq__(self, other: any) -> bool:
        # Ensure that this reference is valid
        self().enforce_validation()
        if isinstance(other, Reflective):
            return self().ref == other().ref
        return self().ref == other

    def __ne__(self, other: any) -> bool:
        # Ensure that this reference is valid
        self().enforce_validation()
        if isinstance(other, Reflective):
            return self().ref != other().ref
        return self().ref != other

    def __len__(self) -> int:
        # Ensure that this reference is valid
        self().enforce_validation()
        value = self().ref
        if isinstance(value, bool):
            return 1 if value is True else 0
        return len(value)


class RType(Reflective):
    pass


class RComposite(RType):
    pass


class RSimple(RType):

    def __setattr__(self, key: str, value: any) -> None:
        # Ensure that this reference is valid
        self().enforce_validation()
        raise AttributeError(f'<{self.__class__.__name__}> This object does not support assignment of the "{key}" '
                             + 'attribute.')
