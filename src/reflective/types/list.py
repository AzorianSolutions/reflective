from collections import UserList
from reflective.types.base import RComposite


class RList(RComposite, UserList, list):

    def __init__(self, ref: any):
        from reflective.util import RUtil
        value = RUtil.get_reference(ref)
        if value is not None:
            value = RUtil.get_list_value(value)
            RUtil.update_reference(ref, value)
        self.__dict__['data'] = value
        super().__init__(ref)

    def __lt__(self, other):
        # Ensure that this reference is valid
        self().enforce_validation()
        return self.__dict__['data'] < self.__cast(other)

    def __le__(self, other):
        # Ensure that this reference is valid
        self().enforce_validation()
        return self.__dict__['data'] <= self.__cast(other)

    def __gt__(self, other):
        # Ensure that this reference is valid
        self().enforce_validation()
        return self.__dict__['data'] > self.__cast(other)

    def __ge__(self, other):
        # Ensure that this reference is valid
        self().enforce_validation()
        return self.__dict__['data'] >= self.__cast(other)

    def __cast(self, other):
        return other.data if isinstance(other, UserList) else other

    def __contains__(self, item):
        # Ensure that this reference is valid
        self().enforce_validation()
        return item in self.__dict__['data']

    def __add__(self, other):
        # Ensure that this reference is valid
        self().enforce_validation()
        if isinstance(other, UserList):
            return self.__class__(self.__dict__['data'] + other.data)
        elif isinstance(other, type(self.__dict__['data'])):
            return self.__class__(self.__dict__['data'] + other)
        return self.__class__(self.__dict__['data'] + list(other))

    def __radd__(self, other):
        # Ensure that this reference is valid
        self().enforce_validation()
        if isinstance(other, UserList):
            return self.__class__(other.data + self.__dict__['data'])
        elif isinstance(other, list):
            return self.__class__(other + self.__dict__['data'])
        return self.__class__(list(other) + self.__dict__['data'])

    def __iadd__(self, other):
        # Ensure that this reference is valid
        self().enforce_validation()
        if isinstance(other, UserList):
            self.__dict__['data'] += other.data
        elif isinstance(other, type(self.__dict__['data'])):
            self.__dict__['data'] += other
        else:
            self.__dict__['data'] += list(other)
        return self

    def __mul__(self, n):
        # Ensure that this reference is valid
        self().enforce_validation()
        return self.__class__(self.__dict__['data'] * n)

    __rmul__ = __mul__

    def __imul__(self, n):
        # Ensure that this reference is valid
        self().enforce_validation()
        self.__dict__['data'] *= n
        return self

    def __copy__(self):
        # Ensure that this reference is valid
        self().enforce_validation()
        inst = self.__class__.__new__(self.__class__, self().context.ref)
        inst.__dict__.update(self.__dict__)
        # Create a copy and avoid triggering descriptors
        inst.__dict__["data"] = self.__dict__["data"][:]
        return inst

    def append(self, item):
        # Ensure that this reference is valid
        self().enforce_validation()
        self.__dict__['data'].append(item)

    def insert(self, i, item):
        # Ensure that this reference is valid
        self().enforce_validation()
        self.__dict__['data'].insert(i, item)

    def pop(self, i=-1):
        # Ensure that this reference is valid
        self().enforce_validation()
        return self.__dict__['data'].pop(i)

    def remove(self, item):
        # Ensure that this reference is valid
        self().enforce_validation()
        self.__dict__['data'].remove(item)

    def clear(self):
        # Ensure that this reference is valid
        self().enforce_validation()
        self.__dict__['data'].clear()

    def copy(self):
        # Ensure that this reference is valid
        self().enforce_validation()
        return self.__class__(self)

    def count(self, item):
        # Ensure that this reference is valid
        self().enforce_validation()
        return self.__dict__['data'].count(item)

    def index(self, item, *args):
        # Ensure that this reference is valid
        self().enforce_validation()
        return self.__dict__['data'].index(item, *args)

    def reverse(self):
        # Ensure that this reference is valid
        self().enforce_validation()
        self.__dict__['data'].reverse()

    def sort(self, *args, **kwds):
        # Ensure that this reference is valid
        self().enforce_validation()
        self.__dict__['data'].sort(*args, **kwds)

    def extend(self, other):
        # Ensure that this reference is valid
        self().enforce_validation()
        if isinstance(other, UserList):
            self.__dict__['data'].extend(other.data)
        else:
            self.__dict__['data'].extend(other)
