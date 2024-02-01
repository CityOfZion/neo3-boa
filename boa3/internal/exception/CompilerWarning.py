from abc import ABC
from typing import Iterable, Optional, Union


class CompilerWarning(ABC, BaseException):
    def __init__(self, line: int, col: int):
        self.line: int = line
        self.col: int = col
        self.filepath: Optional[str] = None

    @property
    def message(self) -> str:
        message = '' if self._warning_message is None else ' - ' + self._warning_message
        if isinstance(self.filepath, str):
            message += f'\t <{self.filepath}>'
        return '{0}:{1}{2}'.format(self.line, self.col, message)

    @property
    def _warning_message(self) -> Optional[str]:
        return None

    def __str__(self) -> str:
        return self.message

    def __eq__(self, other) -> bool:
        if not isinstance(other, type(self)):
            return False
        return self.message == other.message


class DeprecatedSymbol(CompilerWarning):
    """
    A warning raised when a deprecated symbol is used.
    """

    def __init__(self, line: int, col: int, symbol_id: str):
        self.symbol_id: str = symbol_id
        super().__init__(line, col)

    @property
    def _warning_message(self) -> Optional[str]:
        if self.symbol_id is not None:
            return f'Using deprecated feature: {self.symbol_id}'


class InvalidArgument(CompilerWarning):
    """
    An warning raised when an attempt of method evaluation fails during optimization because an argument is invalid.
    """

    def __init__(self, line: int, col: int, custom_error_message: str = None):
        self.custom_error_message = custom_error_message
        super().__init__(line, col)

    @property
    def _warning_message(self) -> Optional[str]:
        message = "One or more arguments are invalid values"
        if self.custom_error_message is not None:
            message += f": {self.custom_error_message}"
        return message


class NameShadowing(CompilerWarning):
    """
    A warning raised when a name from an outer scope symbol is used as the name of an inner scope symbol
    """
    from boa3.internal.model.symbol import ISymbol

    def __init__(self, line: int, col: int, outer_symbol: ISymbol, symbol_id: str):
        self.symbol_id: str = symbol_id
        self.existing_symbol = outer_symbol
        super().__init__(line, col)

    @property
    def _warning_message(self) -> Optional[str]:
        if self.symbol_id is not None:
            return "Shadowing {0} name '{1}'".format(self.existing_symbol.shadowing_name, self.symbol_id)


class RedeclaredSymbol(CompilerWarning):
    """
    A warning raised when a name from the same scope is used to identify multiple symbols
    """

    def __init__(self, line: int, col: int, symbol_id: str):
        self.symbol_id: str = symbol_id
        super().__init__(line, col)

    @property
    def _warning_message(self) -> Optional[str]:
        if self.symbol_id is not None:
            return "Redeclared '{0}' defined above".format(self.symbol_id)


class TypeCasting(CompilerWarning):
    """
    A warning raised when a type castings is used.
    """

    def __init__(self, line: int, col: int, origin_type_id: Union[str, Iterable[str]],
                 cast_type_id: Union[str, Iterable[str]]):
        if isinstance(origin_type_id, str):
            origin_type_id = [origin_type_id]
        if isinstance(cast_type_id, str):
            cast_type_id = [cast_type_id]

        self.origin_types = origin_type_id
        self.cast_types = cast_type_id
        super().__init__(line, col)

    @property
    def _warning_message(self) -> Optional[str]:
        origin_types = join_args(self.origin_types)
        cast_types = join_args(self.cast_types)
        return ("Casting {0} to {1}. Be aware that casting types may lead to runtime errors."
                .format(origin_types, cast_types)
                )


class UnreachableCode(CompilerWarning):
    """
    A warning raised when a block of code is detected as unreachable
    """

    def __init__(self, line: int, col: int):
        super().__init__(line, col)

    @property
    def _warning_message(self) -> Optional[str]:
        return "Unreachable code"


class UsingSpecificException(CompilerWarning):
    """
    A warning raised when a specific exception is used.
    """

    def __init__(self, line: int, col: int, exception_id: str):
        self._exception_id: str = exception_id
        super().__init__(line, col)

    @property
    def _warning_message(self) -> Optional[str]:
        return "{0} will be interpreted as BaseException when running in the blockchain".format(self._exception_id)


def join_args(iterable: Iterable[str]) -> str:
    return str.join("', '", iterable)
