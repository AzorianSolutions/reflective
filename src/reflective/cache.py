from __future__ import annotations
from collections import UserDict


class CacheManager(UserDict):
    """ This class provides a cache management interface for Reflective instances. """

    _core: 'RCore'
    """ The parent RCore instance of this instance. """

    @property
    def core(self) -> 'RCore':
        """ Returns the parent RCore instance of this instance. """
        return self._core

    @property
    def context(self) -> 'ContextManager':
        """ Returns the context manager instance associated with the parent RCore instance. """
        return self.core.context

    def __init__(self, core: 'RCore'):
        """ Initializes a new CacheManager object associated with the given core. """
        self._core = core
        super().__init__()
