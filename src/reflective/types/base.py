from reflective.core import Reflective


class RType(Reflective):
    pass


class RComposite(RType):
    pass


class RSimple(RType):

    def __setattr__(self, key: str, value: any) -> None:
        raise AttributeError(f'<{self.__class__.__name__}> This object does not support assignment of the "{key}" '
                             + 'attribute.')
