from typing import Union
from reflective.tcore import RCore
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
        from reflective.tcore import RCore
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
        namespace = self.__dict__[NAMESPACE_KEY]
        core = self.__dict__[namespace]

        # Return the reference to the RCore instance if no arguments are passed in.
        if not len(args):
            return core

        # Return the underlying value reference if a single empty string is passed in.
        if len(args) == 1 and str(args[0]).strip() == '':
            return core.context.ref

        qr: QueryResult = core.query(args[0])

        if len(qr) == 1:
            return qr[0]

        return qr

    def __enter__(self) -> 'Reflective':
        """ Returns a reference to the RCore instance bound to this Reflective instance. """
        return self()

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def __repr__(self) -> str:
        return self().ref.__repr__()

    def __str__(self) -> str:
        return str(self().ref)

    def __instancecheck__(self, instance):
        return isinstance(self().context.ref, instance)

    def __eq__(self, other: any) -> bool:
        if isinstance(other, Reflective):
            return self().ref == other().ref
        return self().ref == other

    def __ne__(self, other: any) -> bool:
        if isinstance(other, Reflective):
            return self().ref != other().ref
        return self().ref != other

    def __len__(self) -> int:
        return len(self().ref)


class RType(Reflective):
    pass


class RComposite(RType):
    pass


class RSimple(RType):

    def __setattr__(self, key: str, value: any) -> None:
        raise AttributeError(f'<{self.__class__.__name__}> This object does not support assignment of the "{key}" '
                             + 'attribute.')
