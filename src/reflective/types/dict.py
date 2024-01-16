from collections import UserDict
from reflective.types.base import RComposite


class RDict(RComposite, UserDict, dict):

    def __init__(self, ref: any = None, **kwargs):
        from reflective.core import RCore
        value = RCore.get_reference(ref)
        self.__dict__['data'] = value
        super().__init__(ref)
        if value is not None:
            self.update(value)
        if kwargs:
            self.update(kwargs)

    def __iter__(self):
        return iter(self.__dict__['data'])

    # Modify __contains__ to work correctly when __missing__ is present
    def __contains__(self, key):
        return key in self.__dict__['data']

    def __or__(self, other):
        if isinstance(other, UserDict):
            return self.__class__(self.__dict__['data'] | other.data)
        if isinstance(other, dict):
            return self.__class__(self.__dict__['data'] | other)
        return NotImplemented

    def __ror__(self, other):
        if isinstance(other, UserDict):
            return self.__class__(other.data | self.__dict__['data'])
        if isinstance(other, dict):
            return self.__class__(other | self.__dict__['data'])
        return NotImplemented

    def __ior__(self, other):
        if isinstance(other, UserDict):
            self.__dict__['data'] |= other.data
        else:
            self.__dict__['data'] |= other
        return self

    def __copy__(self):
        inst = self.__class__.__new__(self.__class__, self().context.ref)
        inst.__dict__.update(self.__dict__)
        # Create a copy and avoid triggering descriptors
        inst.__dict__["data"] = self.__dict__["data"].copy()
        return inst

    def copy(self):
        if self.__class__ is UserDict:
            return UserDict(self.__dict__['data'].copy())
        import copy
        data = self.__dict__['data']
        try:
            self.__dict__['data'] = {}
            c = copy.copy(self)
        finally:
            self.__dict__['data'] = data
        c.update(self)
        return c
