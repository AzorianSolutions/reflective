from reflective.types.base import RSimple


class RNumeric(RSimple):
    pass


class RInt(RNumeric, int):

    def __new__(cls, ref: any, *args, **kwargs):
        from reflective.util import RUtil
        return int.__new__(cls, RUtil.get_reference(ref), *args, **kwargs)


class RFloat(RNumeric, float):

    def __new__(cls, ref: any):
        from reflective.util import RUtil
        return float.__new__(cls, RUtil.get_reference(ref))


class RComplex(RNumeric, complex):

    def __new__(cls, ref: any, *args, **kwargs):
        from reflective.util import RUtil
        return complex.__new__(cls, RUtil.get_reference(ref), *args, **kwargs)
