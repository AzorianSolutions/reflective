from reflective.core import RCore
from reflective.types.base import RComposite


class RTuple(RComposite, tuple):

    def __new__(cls, ref: any):
        return tuple.__new__(cls, RCore.get_reference(ref))
