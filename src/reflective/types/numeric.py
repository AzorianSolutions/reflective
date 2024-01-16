from reflective.core import RCore
from reflective.types.base import RSimple


class RNumeric(RSimple):
    pass


class RInt(RNumeric, int):

    def __new__(cls, ref: any, *args, **kwargs):
        return int.__new__(cls, RCore.get_reference(ref), *args, **kwargs)


class RFloat(RNumeric, float):

    def __new__(cls, ref: any):
        return float.__new__(cls, RCore.get_reference(ref))


class RComplex(RNumeric, complex):

    def __new__(cls, ref: any, *args, **kwargs):
        return complex.__new__(cls, RCore.get_reference(ref), *args, **kwargs)
