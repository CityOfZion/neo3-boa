from abc import ABC


class CompilerError(ABC, Exception):
    """
    An interface for compilation errors
    """
    def __init__(self, line: int, col: int, message: str = None):
        self.line: int = line
        self.col: int = col

        self.message = "%s:%s" % (line, col)
        if message is not None:
            self.message += " - %s" % message

    def __str__(self) -> str:
        return self.message


class TypeHintMissing(CompilerError):
    """
    An error raised when type hint cannot be found
    """
    def __init__(self, line: int, col: int, symbol_id: str = None):
        message = None
        if symbol_id is not None:
            message = "Type hint is missing for the symbol '%s'" % symbol_id
        super().__init__(line, col, message)


class InvalidType(CompilerError):
    """
    An error raised when a type that is not supported by Neo VM is used
    """
    def __init__(self, line: int, col: int, symbol_id: str = None):
        message = "Invalid type"
        if symbol_id is not None:
            message += ": '%s'" % symbol_id
        super().__init__(line, col, message)


class NotSupportedOperation(CompilerError):
    """
    An error raised when an operation that is not supported by Neo VM is used
    """
    def __init__(self, line: int, col: int, symbol_id: str):
        message = "The following operation is not supported: '%s'" % symbol_id
        super().__init__(line, col, message)


class UnresolvedReference(CompilerError):
    """
    An error raised when an undefined symbol is used
    """
    def __init__(self, line: int, col: int, symbol_id: str):
        message = "Unresolved reference '%s'" % symbol_id
        super().__init__(line, col, message)


class MismatchedTypes(CompilerError):
    """
    An error raised when the evaluated and expected types are not the same
    """
    def __init__(self, line: int, col: int, expected_type_id: str, actual_type_id: str):
        message = "Expected type '%s', got '%s' instead" % (expected_type_id, actual_type_id)
        super().__init__(line, col, message)


class TooManyReturns(CompilerError):
    """
    An error raised when a function returns a tuple
    """
    def __init__(self, line: int, col: int):
        message = "Too many returns"
        super().__init__(line, col, message)
