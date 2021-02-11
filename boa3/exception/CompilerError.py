from abc import ABC
from typing import Iterable, Optional, Union


class CompilerError(ABC, BaseException):
    """
    An interface for compilation errors
    """

    def __init__(self, line: int, col: int):
        self.line: int = line
        self.col: int = col

    @property
    def message(self) -> str:
        message = '' if self._error_message is None else ' - ' + self._error_message
        return '{0}:{1}{2}'.format(self.line, self.col, message)

    @property
    def _error_message(self) -> Optional[str]:
        return None

    def __str__(self) -> str:
        return self.message

    def __eq__(self, other) -> bool:
        if not isinstance(other, type(self)):
            return False
        return self.message == other.message


class IncorrectNumberOfOperands(CompilerError):
    """
    An error raised when an operation is used with the wrong number of operands
    """

    def __init__(self, line: int, col: int, expected_count: int, actual_count: int):
        self.expected = expected_count
        self.actual = actual_count
        super().__init__(line, col)

    @property
    def _error_message(self) -> Optional[str]:
        return "Incorrect number of operands: expected '%s', got '%s' instead" % (self.expected, self.actual)


class InvalidType(CompilerError):
    """
    An error raised when a type that is not supported by Neo VM is used
    """

    def __init__(self, line: int, col: int, symbol_id: str = None):
        self.symbol_id = symbol_id
        super().__init__(line, col)

    @property
    def _error_message(self) -> Optional[str]:
        message = "Invalid type"
        if self.symbol_id is not None:
            message += ": '%s'" % self.symbol_id
        return message


class InternalError(CompilerError):
    """
    An error raised when an unexpected exception is raised during the compilation
    """

    def __init__(self, line: int, col: int, raised_exception: BaseException = None):
        self.raised_exception: BaseException = raised_exception
        super().__init__(line, col)

    @property
    def _error_message(self) -> Optional[str]:
        message = "Internal compiler error"
        if self.raised_exception is not None:
            message += ". {0}: {1}".format(type(self.raised_exception).__name__, str(self.raised_exception))
        return message


class MetadataImplementationMissing(CompilerError):
    """
    An error raised when the metadata required functions aren't implemented
    """

    def __init__(self, line: int, col: int, symbol_id: str, metadata_attr_id: str):
        self.symbol_id: str = symbol_id
        self.metadata_attr_id: str = metadata_attr_id
        super().__init__(line, col)

    @property
    def _error_message(self) -> Optional[str]:
        return "'{0}' requires '{1}' implementation".format(self.metadata_attr_id, self.symbol_id)


class MetadataIncorrectImplementation(CompilerError):
    """
    An error raised when a metadata required function is incorrectly implemented
    """
    from boa3.model.symbol import ISymbol

    def __init__(self, line: int, col: int, symbol_id: str, expected_symbol: ISymbol, actual_symbol: ISymbol):
        from boa3.model.symbol import ISymbol

        self.symbol_id: str = symbol_id
        self.expected_symbol: ISymbol = expected_symbol
        self.actual_symbol: ISymbol = actual_symbol
        super().__init__(line, col)

    @property
    def _error_message(self) -> Optional[str]:
        return ("'{0}' is not correctly implemented. Expecting '{1}', got '{2}' instead"
                .format(self.symbol_id, self.expected_symbol, self.actual_symbol))


class MetadataInformationMissing(CompilerError):
    """
    An error raised when the metadata info doesn't match with the functions requirements
    """

    def __init__(self, line: int, col: int, symbol_id: str, metadata_attr_id: str):
        self.symbol_id: str = symbol_id
        self.metadata_attr_id: str = metadata_attr_id
        super().__init__(line, col)

    @property
    def _error_message(self) -> Optional[str]:
        return "'{0}' requires '{1}' attribute, which is missing in the metadata".format(self.symbol_id, self.metadata_attr_id)


class MismatchedTypes(CompilerError):
    """
    An error raised when the evaluated and expected types are not the same
    """

    def __init__(self, line: int, col: int, expected_type_id: Union[str, Iterable[str]], actual_type_id: Union[str, Iterable[str]]):
        if isinstance(expected_type_id, str):
            expected_type_id = [expected_type_id]
        if isinstance(actual_type_id, str):
            actual_type_id = [actual_type_id]

        self.expected_types = expected_type_id
        self.actual_types = actual_type_id
        super().__init__(line, col)

    @property
    def _error_message(self) -> Optional[str]:
        expected_types = join_args(self.expected_types)
        actual_types = join_args(self.actual_types)
        return "Expected type '%s', got '%s' instead" % (expected_types, actual_types)


class MissingReturnStatement(CompilerError):
    """
    An error raised when a function with a return value is missing a return statement
    """

    def __init__(self, line: int, col: int, symbol_id: str):
        self.symbol_id = symbol_id
        super().__init__(line, col)

    @property
    def _error_message(self) -> Optional[str]:
        return "'%s': Missing return statement" % self.symbol_id


class NotSupportedOperation(CompilerError):
    """
    An error raised when an operation that is not supported by Neo VM is used
    """

    def __init__(self, line: int, col: int, symbol_id: str):
        self.symbol_id = symbol_id
        super().__init__(line, col)

    @property
    def _error_message(self) -> Optional[str]:
        return "The following operation is not supported: '%s'" % self.symbol_id


class UnexpectedArgument(CompilerError):
    """
    An error thrown when more arguments are used in a function than the number of arguments in the function's signature
    """

    def __init__(self, line: int, col: int):
        super().__init__(line, col)

    @property
    def _error_message(self) -> Optional[str]:
        return "Unexpected argument"


class UnfilledArgument(CompilerError):
    """
    An error thrown when less arguments are used in a function than the number of arguments in the function's signature
    """

    def __init__(self, line: int, col: int, param: str):
        self.param = param
        super().__init__(line, col)

    @property
    def _error_message(self) -> Optional[str]:
        return "Parameter '%s' unfilled" % self.param


class UnresolvedReference(CompilerError):
    """
    An error raised when an undefined symbol is used
    """

    def __init__(self, line: int, col: int, symbol_id: str):
        self.symbol_id = symbol_id
        super().__init__(line, col)

    @property
    def _error_message(self) -> Optional[str]:
        return "Unresolved reference '%s'" % self.symbol_id

    def __eq__(self, other) -> bool:
        if not isinstance(other, type(self)):
            return False
        return self._error_message == other._error_message


class UnresolvedOperation(CompilerError):
    """
    An error raised when an undefined symbol is used
    """

    def __init__(self, line: int, col: int, type_id: str, operation_id: str):
        self.type_id = type_id
        self.operation_id = operation_id
        super().__init__(line, col)

    @property
    def _error_message(self) -> Optional[str]:
        return "Unresolved reference: '%s' does not have a definition of '%s' operator" % (self.type_id, self.operation_id)


class TooManyReturns(CompilerError):
    """
    An error raised when a function returns a tuple
    """

    def __init__(self, line: int, col: int):
        super().__init__(line, col)

    @property
    def _error_message(self) -> Optional[str]:
        return "Too many returns"


class TypeHintMissing(CompilerError):
    """
    An error raised when type hint cannot be found
    """

    def __init__(self, line: int, col: int, symbol_id: str = None):
        self.symbol_id = symbol_id
        super().__init__(line, col)

    @property
    def _error_message(self) -> Optional[str]:
        if self.symbol_id is not None:
            return "Type hint is missing for the symbol '%s'" % self.symbol_id


def join_args(iterable: Iterable[str]) -> str:
    return str.join("', '", iterable)
