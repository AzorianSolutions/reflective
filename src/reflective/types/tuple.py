from reflective.core import RCore
from reflective.types.base import RComposite


class RTuple(RComposite, tuple):

    def __new__(cls, ref: any):
        from reflective.util import RUtil
        return tuple.__new__(cls, RUtil.get_reference(ref))
