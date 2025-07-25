from typing import Any

from boa3.internal.model.builtin.method import IBuiltinMethod
from boa3.internal.model.expression import IExpression
from boa3.internal.model.method import Method
from boa3.internal.model.symbol import ISymbol
from boa3.internal.model.type.itype import IType
from boa3.internal.model.type.primitive.bytestype import BytesType
from boa3.internal.model.type.type import Type
from boa3.internal.model.variable import Variable
from boa3.internal.neo.vm.opcode.Opcode import Opcode


class OpcodeType(BytesType):
    """
    A class used to represent Neo interop Opcode type
    """

    def __init__(self):
        super().__init__()
        self._identifier = 'Opcode'

    @property
    def default_value(self) -> Any:
        return Opcode.NOP

    @classmethod
    def build(cls, value: Any = None) -> IType:
        if value is None or cls._is_type_of(value):
            return _Opcode

    @classmethod
    def _is_type_of(cls, value: Any):
        return isinstance(value, (Opcode, OpcodeType))

    @property
    def symbols(self) -> dict[str, ISymbol]:
        """
        Gets the class symbols of this type

        :return: a dictionary that maps each symbol in the module with its name
        """
        _symbols = super().symbols
        _symbols.update({name: Variable(self) for name in Opcode.__members__.keys()})

        return _symbols

    def get_value(self, symbol_id) -> Any:
        """
        Gets the literal value of a symbol

        :return: the value if this type has this symbol. None otherwise.
        """
        if symbol_id in self.symbols:
            return Opcode.__members__[symbol_id]

        return None

    def constructor_method(self) -> Method | None:
        if self._constructor is None:
            self._constructor: Method = OpcodeMethod(self)
        return self._constructor


_Opcode = OpcodeType()


class OpcodeMethod(IBuiltinMethod):

    def __init__(self, return_type: OpcodeType):
        identifier = '-Opcode__init__'
        args: dict[str, Variable] = {
            'x': Variable(Type.bytes)
        }
        super().__init__(identifier, args, return_type=return_type)

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
        enum_values = [value for value in Opcode]

        for index, value in enumerate(enum_values):
            code_generator.duplicate_stack_item(code_generator.stack_size)
            code_generator.convert_literal(value)
            code_generator.convert_operation(BinaryOp.Eq, is_internal=True)
            if index > 0:
                code_generator.convert_operation(BinaryOp.Or, is_internal=True)

        code_generator.convert_literal(f"Invalid {self.return_type.identifier} parameter value")
        code_generator.convert_assert(has_message=True)
