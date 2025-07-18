from enum import IntEnum
from typing import Type as TType, Any

from boa3.internal.model.builtin.method import IBuiltinMethod
from boa3.internal.model.expression import IExpression
from boa3.internal.model.method import Method
from boa3.internal.model.symbol import ISymbol
from boa3.internal.model.type.primitive.inttype import IntType
from boa3.internal.model.type.type import Type
from boa3.internal.model.variable import Variable


class IntEnumType(IntType):
    """
    A class used to represent Python IntEnum type
    """

    def __init__(self, enum_type: TType[IntEnum]):
        super().__init__()
        self._identifier = '-IntEnum'
        self._enum_type = enum_type

    @property
    def symbols(self) -> dict[str, ISymbol]:
        """
        Gets the class symbols of this type

        :return: a dictionary that maps each symbol in the module with its name
        """
        _symbols = super().symbols
        _symbols.update({name: Variable(self) for name in self._enum_type.__members__.keys()})

        return _symbols

    def get_value(self, symbol_id) -> Any:
        """
        Gets the literal value of a symbol

        :return: the value if this type has this symbol. None otherwise.
        """
        if symbol_id in self.symbols and symbol_id in self._enum_type.__members__:
            return self._enum_type.__members__[symbol_id]

        return None

    def constructor_method(self) -> Method | None:
        if self._constructor is None:
            self._constructor: Method = IntEnumMethod(self, self._enum_type)
        return self._constructor

    @property
    def exception_message(self) -> str:
        return f"Invalid {self.identifier} parameter value"


class IntEnumMethod(IBuiltinMethod):

    def __init__(self, return_type: IntEnumType, enum_type: TType[IntEnum]):
        identifier = f'-{return_type.identifier}__init__'
        args: dict[str, Variable] = {
            'x': Variable(Type.int)
        }
        super().__init__(identifier, args, return_type=return_type)
        self._enum_type = enum_type

    def validate_parameters(self, *params: IExpression) -> bool:
        return len(params) == 1

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> str | None:
        return None

    def generate_internal_opcodes(self, code_generator):
        from boa3.internal.model.operation.binaryop import BinaryOp
        enum_values = [value for value in self._enum_type]

        for index, value in enumerate(enum_values):
            code_generator.duplicate_stack_item(code_generator.stack_size)
            code_generator.convert_literal(value)
            code_generator.convert_operation(BinaryOp.NumEq, is_internal=True)
            if index > 0:
                code_generator.convert_operation(BinaryOp.Or, is_internal=True)

        code_generator.convert_literal(self.return_type.exception_message)
        code_generator.convert_assert(has_message=True)
