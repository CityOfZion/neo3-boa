from abc import ABC
from typing import Iterable, Optional, Union

from boa3.internal import constants
from boa3.internal.model.builtin.internal.internalmethod import IInternalMethod
from boa3.internal.model.event import Event
from boa3.internal.model.method import Method


class CompilerError(ABC, BaseException):
    """
    An interface for compilation errors
    """

    def __init__(self, line: int, col: int):
        self.line: int = line
        self.col: int = col
        self.filepath: Optional[str] = None

    @property
    def message(self) -> str:
        message = '' if self._error_message is None else ' - ' + self._error_message
        if isinstance(self.filepath, str):
            message += f'\t <{self.filepath}>'
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


class CircularImport(CompilerError):
    """
    An error raised when circular imports are detected
    """

    def __init__(self, line: int, col: int, target_import: str, target_origin: str):
        import os
        self.target_import = target_import
        self.target_origin = target_origin.replace(os.sep, constants.PATH_SEPARATOR)
        super().__init__(line, col)

    @property
    def _error_message(self) -> Optional[str]:
        return "Circular import with '%s' ('%s')" % (self.target_import, self.target_origin)


class DuplicatedIdentifier(CompilerError):
    """
    An error raised when more than one symbol uses the same identifier in the same scope and cannot be overwritten.
    """

    def __init__(self, line: int, col: int, duplicated_id: str = None):
        self._duplicated_id = duplicated_id
        super().__init__(line, col)

    @property
    def _error_message(self) -> Optional[str]:
        return f"Duplicate identifier: '{self._duplicated_id}'"


class DuplicatedManifestIdentifier(CompilerError):
    """
    An error raised when more than one symbol uses the same identifier in the manifest.
    """

    def __init__(self, line: int, col: int, duplicated_id: str = None, duplicated_arg_count: int = None):
        self._duplicated_id = duplicated_id
        self._arg_count = duplicated_arg_count
        super().__init__(line, col)

    @property
    def _error_message(self) -> Optional[str]:
        return f"Duplicate manifest identifier: '{self._duplicated_id}' with {self._arg_count} argument(s)"


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


class InvalidUsage(CompilerError):
    """
    An error raised when a built-in function or decorator is incorrectly defined
    """

    def __init__(self, line: int, col: int, custom_error_message: str = None):
        self.custom_error_message = custom_error_message
        super().__init__(line, col)

    @property
    def _error_message(self) -> Optional[str]:
        message = "Invalid usage"
        if self.custom_error_message is not None:
            message += f": {self.custom_error_message}"
        return message


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


class InternalIncorrectSignature(CompilerError):
    """
    An error raised when an internal method is defined by the user, but with an incorrect signature
    """

    def __init__(self, line: int, col: int, expected_method: IInternalMethod):
        self.expected_method: IInternalMethod = expected_method
        super().__init__(line, col)

    @property
    def _error_message(self) -> Optional[str]:
        return "The implementation of '{0}' is different " \
               "from the expected '{1}'.".format(self.expected_method.raw_identifier,
                                                 self.expected_method)


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
    from boa3.internal.model.symbol import ISymbol

    def __init__(self, line: int, col: int, symbol_id: str, expected_symbol: ISymbol, actual_symbol: ISymbol):
        from boa3.internal.model.symbol import ISymbol

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
        return "'{0}' requires '{1}' attribute, which is missing in the metadata".format(self.symbol_id,
                                                                                         self.metadata_attr_id)


class MismatchedTypes(CompilerError):
    """
    An error raised when the evaluated and expected types are not the same
    """

    def __init__(self, line: int, col: int, expected_type_id: Union[str, Iterable[str]],
                 actual_type_id: Union[str, Iterable[str]]):
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


class MissingInitCall(CompilerError):
    """
    An error raised when a custom class is created with inheritance and it's missing the base __init__ call
    """

    def __init__(self, line: int, col: int):
        super().__init__(line, col)

    @property
    def _error_message(self) -> Optional[str]:
        return "Call to __init__ of super class is missed"


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


class MissingStandardDefinition(CompilerError):
    """
    An error raised when a contract standard is defined in the metadata and are required symbols missing
    """

    def __init__(self, standard_id: str, symbol_id: str, symbol: Union[Method, Event]):
        self.standard = standard_id
        self.symbol_id = symbol_id
        self.symbol = symbol
        super().__init__(0, 0)

    @property
    def _error_message(self) -> Optional[str]:
        safe_symbol_prefix = 'safe ' if self.symbol.is_safe else ''
        return f"'{self.standard}': Missing '{self.symbol_id}' {self.symbol.shadowing_name} definition " \
               f"'{safe_symbol_prefix}{self.symbol}'"

    @property
    def message(self) -> str:
        return self._error_message


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
        return "Unresolved reference: '{0}' does not have a definition of '{1}' operator".format(self.type_id,
                                                                                                 self.operation_id)


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


class SelfArgumentError(CompilerError):
    """
    An error raised when the self argument is wrong
    """

    def __init__(self, line: int, col: int):
        super().__init__(line, col)

    @property
    def _error_message(self) -> Optional[str]:
        return "The self argument was not found or the annotation is incorrect"


def join_args(iterable: Iterable[str]) -> str:
    return str.join("', '", iterable)
