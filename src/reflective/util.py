import re


class RUtil:
    """ This class provides utility methods for the Reflective library components. """

    ref_pattern = re.compile(r'\$(r|e){([a-z0-9_/.]+)}', re.IGNORECASE)
    """ The regular expression pattern used to match variable references in values. """

    @staticmethod
    def get_reference(value: any):
        from reflective.core import RCore
        from reflective.context import ContextManager
        from reflective.types import Reflective

        if isinstance(value, Reflective):
            value = value().context.ref

        if isinstance(value, RCore):
            value = value.context.ref

        if isinstance(value, ContextManager):
            value = value.ref

        return value

    @staticmethod
    def update_reference(ref: any, value: any):
        from reflective.core import RCore
        from reflective.context import ContextManager
        from reflective.types import Reflective

        if isinstance(ref, Reflective):
            ref().context.raw = value

        elif isinstance(ref, RCore):
            ref.context.raw = value

        elif isinstance(ref, ContextManager):
            ref.raw = value

    @staticmethod
    def get_type_class(value: any):
        """ Returns the appropriate Reflective type class for the given value. """
        from reflective.types import Reflective, RDict, RList, RTuple, RBool, RInt, RFloat, RComplex, RString, RNone

        if isinstance(value, dict) or value == {}:
            return RDict

        if isinstance(value, list) or value == []:
            return RList

        if isinstance(value, tuple):
            return RTuple

        if isinstance(value, bool):
            return RBool

        if isinstance(value, int):
            return RInt

        if isinstance(value, float):
            return RFloat

        if isinstance(value, complex):
            return RComplex

        if isinstance(value, str):
            return RString

        if value is None:
            return RNone

        return Reflective

    @staticmethod
    def get_list_value(value: any) -> list:
        """ Returns the appropriate list value for the given value. """
        from collections import UserList
        if value is None:
            raise ValueError('Cannot convert None to list.')
        if type(value) is type([]):
            return value
        elif isinstance(value, UserList):
            return value.data[:]
        return list(value)

    @staticmethod
    def get_string_value(value: any) -> str:
        """ Returns the appropriate string value for the given value. """
        from collections import UserString
        if isinstance(value, str):
            return value
        if isinstance(value, UserString):
            return value.data[:]
        return str(value)

    @staticmethod
    def extract(value: str) -> list:
        """ Extracts the Reflective reference strings from the given string and returns them as a list of strings."""

        references: list = []

        # Process $(r|e){...} references
        matches = RUtil.ref_pattern.findall(value)

        for match in matches:
            # Handles instances of $(r){...} references
            if str(match[0]).lower() == 'r':
                # Capture the Reflective query string
                references.append(match[1])

        return references

    @staticmethod
    def update(source: str, ref: str, value: any) -> any:
        """
        Updates the given source string with the given value for matching Reflective reference strings.
        Additionally, pass-through typing support is provided for source strings that contain single references.
        """
        from reflective.query import QueryResult

        ref_pattern = f'$r{{{ref}}}'

        # Provide typed references when sole references are found
        if source.replace(ref_pattern, '').strip() == '':
            if isinstance(value, QueryResult) and len(value) == 1:
                return value[0]
            return value

        # Update the string value with the query value
        if isinstance(value, QueryResult) and len(value) == 1:
            value = value[0]

        source = source.replace(ref_pattern, str(value))

        return source

