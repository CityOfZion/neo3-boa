from enum import IntFlag
from functools import reduce
from typing import Type as TType, Any

from boa3.internal.model.builtin.method import IBuiltinMethod
from boa3.internal.model.expression import IExpression
from boa3.internal.model.method import Method
from boa3.internal.model.symbol import ISymbol
from boa3.internal.model.type.primitive.inttype import IntType
from boa3.internal.model.type.type import Type
from boa3.internal.model.variable import Variable


class IntFlagType(IntType):
    """
    A class used to represent Python IntFlag type
    """

    def __init__(self, enum_type: TType[IntFlag]):
        super().__init__()
        self._identifier = '-IntFlag'
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

    @property
    def all_flags(self) -> IntFlag:
        flag_values = [value for value in self._enum_type]
        return reduce(lambda x, y: x | y, flag_values)

    @property
    def next_power_of_two(self) -> int:
        """
        Gets the next power of two value
        """
        highest_enum = self.all_flags
        next_power_of_two = 1
        while next_power_of_two < highest_enum:
            next_power_of_two *= 2

        return next_power_of_two

class IntEnumMethod(IBuiltinMethod):

    def __init__(self, return_type: IntFlagType, enum_type: TType[IntFlag]):
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
        from boa3.internal.model.operation.unaryop import UnaryOp

        code_generator.duplicate_stack_top_item()
        code_generator.convert_literal(self.return_type.all_flags)
        code_generator.convert_operation(UnaryOp.BitNot, is_internal=True)
        code_generator.convert_operation(BinaryOp.BitAnd, is_internal=True)

        code_generator.convert_operation(UnaryOp.Not, is_internal=True)
        code_generator.convert_literal(self.return_type.exception_message)
        code_generator.convert_assert(has_message=True)
