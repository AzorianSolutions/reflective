import sys as _sys
from collections import UserString
from reflective.types.base import RSimple


class RString(RSimple, UserString, str):

    def __init__(self, ref: str):
        from reflective.util import RUtil
        value = RUtil.get_reference(ref)
        value = RUtil.get_string_value(value)
        RUtil.update_reference(ref, value)
        self.__dict__['data'] = value
        super().__init__(ref)

    def __int__(self):
        # Ensure that this reference is valid
        self().enforce_validation()
        return int(self.__dict__['data'])

    def __float__(self):
        # Ensure that this reference is valid
        self().enforce_validation()
        return float(self.__dict__['data'])

    def __complex__(self):
        # Ensure that this reference is valid
        self().enforce_validation()
        return complex(self.__dict__['data'])

    def __hash__(self):
        # Ensure that this reference is valid
        self().enforce_validation()
        return hash(self.__dict__['data'])

    def __getnewargs__(self):
        # Ensure that this reference is valid
        self().enforce_validation()
        return (self.__dict__['data'][:],)

    def __lt__(self, string):
        # Ensure that this reference is valid
        self().enforce_validation()
        if isinstance(string, UserString):
            return self.__dict__['data'] < string.__dict__['data']
        return self.__dict__['data'] < string

    def __le__(self, string):
        # Ensure that this reference is valid
        self().enforce_validation()
        if isinstance(string, UserString):
            return self.__dict__['data'] <= string.__dict__['data']
        return self.__dict__['data'] <= string

    def __gt__(self, string):
        # Ensure that this reference is valid
        self().enforce_validation()
        if isinstance(string, UserString):
            return self.__dict__['data'] > string.__dict__['data']
        return self.__dict__['data'] > string

    def __ge__(self, string):
        # Ensure that this reference is valid
        self().enforce_validation()
        if isinstance(string, UserString):
            return self.__dict__['data'] >= string.__dict__['data']
        return self.__dict__['data'] >= string

    def __contains__(self, char):
        # Ensure that this reference is valid
        self().enforce_validation()
        if isinstance(char, UserString):
            char = char.__dict__['data']
        return char in self.__dict__['data']

    def __add__(self, other):
        # Ensure that this reference is valid
        self().enforce_validation()
        if isinstance(other, UserString):
            return self.__class__(self.__dict__['data'] + other.__dict__['data'])
        elif isinstance(other, str):
            return self.__class__(self.__dict__['data'] + other)
        return self.__class__(self.__dict__['data'] + str(other))

    def __radd__(self, other):
        # Ensure that this reference is valid
        self().enforce_validation()
        if isinstance(other, str):
            return self.__class__(other + self.__dict__['data'])
        return self.__class__(str(other) + self.__dict__['data'])

    def __mul__(self, n):
        # Ensure that this reference is valid
        self().enforce_validation()
        return self.__class__(self.__dict__['data'] * n)

    __rmul__ = __mul__

    def __mod__(self, args):
        # Ensure that this reference is valid
        self().enforce_validation()
        return self.__class__(self.__dict__['data'] % args)

    def __rmod__(self, template):
        # Ensure that this reference is valid
        self().enforce_validation()
        return self.__class__(str(template) % self)

    # the following methods are defined in alphabetical order:
    def capitalize(self):
        # Ensure that this reference is valid
        self().enforce_validation()
        return self.__class__(self.__dict__['data'].capitalize())

    def casefold(self):
        # Ensure that this reference is valid
        self().enforce_validation()
        return self.__class__(self.__dict__['data'].casefold())

    def center(self, width, *args):
        # Ensure that this reference is valid
        self().enforce_validation()
        return self.__class__(self.__dict__['data'].center(width, *args))

    def count(self, sub, start=0, end=_sys.maxsize):
        # Ensure that this reference is valid
        self().enforce_validation()
        if isinstance(sub, UserString):
            sub = sub.__dict__['data']
        return self.__dict__['data'].count(sub, start, end)

    def removeprefix(self, prefix):
        # Ensure that this reference is valid
        self().enforce_validation()
        if isinstance(prefix, UserString):
            prefix = prefix.__dict__['data']
        return self.__class__(self.__dict__['data'].removeprefix(prefix))

    def removesuffix(self, suffix):
        # Ensure that this reference is valid
        self().enforce_validation()
        if isinstance(suffix, UserString):
            suffix = suffix.__dict__['data']
        return self.__class__(self.__dict__['data'].removesuffix(suffix))

    def encode(self, encoding='utf-8', errors='strict'):
        # Ensure that this reference is valid
        self().enforce_validation()
        encoding = 'utf-8' if encoding is None else encoding
        errors = 'strict' if errors is None else errors
        return self.__dict__['data'].encode(encoding, errors)

    def endswith(self, suffix, start=0, end=_sys.maxsize):
        # Ensure that this reference is valid
        self().enforce_validation()
        return self.__dict__['data'].endswith(suffix, start, end)

    def expandtabs(self, tabsize=8):
        # Ensure that this reference is valid
        self().enforce_validation()
        return self.__class__(self.__dict__['data'].expandtabs(tabsize))

    def find(self, sub, start=0, end=_sys.maxsize):
        # Ensure that this reference is valid
        self().enforce_validation()
        if isinstance(sub, UserString):
            sub = sub.__dict__['data']
        return self.__dict__['data'].find(sub, start, end)

    def format(self, /, *args, **kwds):
        # Ensure that this reference is valid
        self().enforce_validation()
        return self.__dict__['data'].format(*args, **kwds)

    def format_map(self, mapping):
        # Ensure that this reference is valid
        self().enforce_validation()
        return self.__dict__['data'].format_map(mapping)

    def index(self, sub, start=0, end=_sys.maxsize):
        # Ensure that this reference is valid
        self().enforce_validation()
        return self.__dict__['data'].index(sub, start, end)

    def isalpha(self):
        # Ensure that this reference is valid
        self().enforce_validation()
        return self.__dict__['data'].isalpha()

    def isalnum(self):
        # Ensure that this reference is valid
        self().enforce_validation()
        return self.__dict__['data'].isalnum()

    def isascii(self):
        # Ensure that this reference is valid
        self().enforce_validation()
        return self.__dict__['data'].isascii()

    def isdecimal(self):
        # Ensure that this reference is valid
        self().enforce_validation()
        return self.__dict__['data'].isdecimal()

    def isdigit(self):
        # Ensure that this reference is valid
        self().enforce_validation()
        return self.__dict__['data'].isdigit()

    def isidentifier(self):
        # Ensure that this reference is valid
        self().enforce_validation()
        return self.__dict__['data'].isidentifier()

    def islower(self):
        # Ensure that this reference is valid
        self().enforce_validation()
        return self.__dict__['data'].islower()

    def isnumeric(self):
        # Ensure that this reference is valid
        self().enforce_validation()
        return self.__dict__['data'].isnumeric()

    def isprintable(self):
        # Ensure that this reference is valid
        self().enforce_validation()
        return self.__dict__['data'].isprintable()

    def isspace(self):
        # Ensure that this reference is valid
        self().enforce_validation()
        return self.__dict__['data'].isspace()

    def istitle(self):
        # Ensure that this reference is valid
        self().enforce_validation()
        return self.__dict__['data'].istitle()

    def isupper(self):
        # Ensure that this reference is valid
        self().enforce_validation()
        return self.__dict__['data'].isupper()

    def join(self, seq):
        # Ensure that this reference is valid
        self().enforce_validation()
        return self.__dict__['data'].join(seq)

    def ljust(self, width, *args):
        # Ensure that this reference is valid
        self().enforce_validation()
        return self.__class__(self.__dict__['data'].ljust(width, *args))

    def lower(self):
        # Ensure that this reference is valid
        self().enforce_validation()
        return self.__class__(self.__dict__['data'].lower())

    def lstrip(self, chars=None):
        # Ensure that this reference is valid
        self().enforce_validation()
        return self.__class__(self.__dict__['data'].lstrip(chars))

    maketrans = str.maketrans

    def partition(self, sep):
        # Ensure that this reference is valid
        self().enforce_validation()
        return self.__dict__['data'].partition(sep)

    def replace(self, old, new, maxsplit=-1):
        # Ensure that this reference is valid
        self().enforce_validation()
        if isinstance(old, UserString):
            old = old.__dict__['data']
        if isinstance(new, UserString):
            new = new.__dict__['data']
        return self.__class__(self.__dict__['data'].replace(old, new, maxsplit))

    def rfind(self, sub, start=0, end=_sys.maxsize):
        # Ensure that this reference is valid
        self().enforce_validation()
        if isinstance(sub, UserString):
            sub = sub.__dict__['data']
        return self.__dict__['data'].rfind(sub, start, end)

    def rindex(self, sub, start=0, end=_sys.maxsize):
        # Ensure that this reference is valid
        self().enforce_validation()
        return self.__dict__['data'].rindex(sub, start, end)

    def rjust(self, width, *args):
        # Ensure that this reference is valid
        self().enforce_validation()
        return self.__class__(self.__dict__['data'].rjust(width, *args))

    def rpartition(self, sep):
        # Ensure that this reference is valid
        self().enforce_validation()
        return self.__dict__['data'].rpartition(sep)

    def rstrip(self, chars=None):
        # Ensure that this reference is valid
        self().enforce_validation()
        return self.__class__(self.__dict__['data'].rstrip(chars))

    def split(self, sep=None, maxsplit=-1):
        # Ensure that this reference is valid
        self().enforce_validation()
        return self.__dict__['data'].split(sep, maxsplit)

    def rsplit(self, sep=None, maxsplit=-1):
        # Ensure that this reference is valid
        self().enforce_validation()
        return self.__dict__['data'].rsplit(sep, maxsplit)

    def splitlines(self, keepends=False):
        # Ensure that this reference is valid
        self().enforce_validation()
        return self.__dict__['data'].splitlines(keepends)

    def startswith(self, prefix, start=0, end=_sys.maxsize):
        # Ensure that this reference is valid
        self().enforce_validation()
        return self.__dict__['data'].startswith(prefix, start, end)

    def strip(self, chars=None):
        # Ensure that this reference is valid
        self().enforce_validation()
        return self.__class__(self.__dict__['data'].strip(chars))

    def swapcase(self):
        # Ensure that this reference is valid
        self().enforce_validation()
        return self.__class__(self.__dict__['data'].swapcase())

    def title(self):
        # Ensure that this reference is valid
        self().enforce_validation()
        return self.__class__(self.__dict__['data'].title())

    def translate(self, *args):
        # Ensure that this reference is valid
        self().enforce_validation()
        return self.__class__(self.__dict__['data'].translate(*args))

    def upper(self):
        # Ensure that this reference is valid
        self().enforce_validation()
        return self.__class__(self.__dict__['data'].upper())

    def zfill(self, width):
        # Ensure that this reference is valid
        self().enforce_validation()
        return self.__class__(self.__dict__['data'].zfill(width))
