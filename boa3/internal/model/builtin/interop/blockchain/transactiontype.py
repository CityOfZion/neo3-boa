from typing import Any, Self

from boa3.internal.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.internal.model.expression import IExpression
from boa3.internal.model.method import Method
from boa3.internal.model.property import Property
from boa3.internal.model.type.classes.classarraytype import ClassArrayType
from boa3.internal.model.variable import Variable


class TransactionType(ClassArrayType):
    """
    A class used to represent Neo Transaction class
    """

    def __init__(self):
        super().__init__('Transaction')
        from boa3.internal.model.type.type import Type
        from boa3.internal.model.type.collection.sequence.uint160type import UInt160Type
        from boa3.internal.model.type.collection.sequence.uint256type import UInt256Type

        self._variables: dict[str, Variable] = {
            'hash': Variable(UInt256Type.build()),
            'version': Variable(Type.int),
            'nonce': Variable(Type.int),
            'sender': Variable(UInt160Type.build()),
            'system_fee': Variable(Type.int),
            'network_fee': Variable(Type.int),
            'valid_until_block': Variable(Type.int),
            'script': Variable(Type.bytes),
        }
        self._constructor: Method = None

    @property
    def class_variables(self) -> dict[str, Variable]:
        return {}

    @property
    def instance_variables(self) -> dict[str, Variable]:
        return self._variables.copy()

    @property
    def properties(self) -> dict[str, Property]:
        return {}

    @property
    def static_methods(self) -> dict[str, Method]:
        return {}

    @property
    def class_methods(self) -> dict[str, Method]:
        return {}

    @property
    def instance_methods(self) -> dict[str, Method]:
        return {}

    def constructor_method(self) -> Method | None:
        # was having a problem with recursive import
        if self._constructor is None:
            self._constructor: Method = TransactionMethod(self)
        return self._constructor

    @classmethod
    def build(cls, value: Any = None) -> Self:
        if value is None or cls._is_type_of(value):
            return _Transaction

    @classmethod
    def _is_type_of(cls, value: Any):
        return isinstance(value, TransactionType)


_Transaction = TransactionType()


class TransactionMethod(IBuiltinMethod):

    def __init__(self, return_type: TransactionType):
        identifier = '-Transaction__init__'
        args: dict[str, Variable] = {}
        super().__init__(identifier, args, return_type=return_type)

    def validate_parameters(self, *params: IExpression) -> bool:
        return len(params) == 0

    def generate_internal_opcodes(self, code_generator):
        from boa3.internal.neo3.core.types import UInt160, UInt256

        uint160_default = UInt160.zero().to_array()
        uint256_default = UInt256.zero().to_array()

        code_generator.convert_literal(b'')  # script
        code_generator.convert_literal(0)  # valid_until_block
        code_generator.convert_literal(0)  # network_fee
        code_generator.convert_literal(0)  # system_fee
        code_generator.convert_literal(uint160_default)  # sender
        code_generator.convert_literal(0)  # nonce
        code_generator.convert_literal(0)  # version
        code_generator.convert_literal(uint256_default)  # hash
        code_generator.convert_new_array(length=8, array_type=self.type)

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> str | None:
        return
