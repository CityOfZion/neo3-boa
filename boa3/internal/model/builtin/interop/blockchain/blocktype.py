from typing import Any, Self

from boa3.internal.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.internal.model.expression import IExpression
from boa3.internal.model.method import Method
from boa3.internal.model.property import Property
from boa3.internal.model.type.classes.classarraytype import ClassArrayType
from boa3.internal.model.variable import Variable


class BlockType(ClassArrayType):
    """
    A class used to represent Neo Block class
    """

    def __init__(self):
        super().__init__('Block')
        from boa3.internal.model.type.type import Type
        from boa3.internal.model.type.collection.sequence.uint160type import UInt160Type
        from boa3.internal.model.type.collection.sequence.uint256type import UInt256Type

        uint256 = UInt256Type.build()

        self._variables: dict[str, Variable] = {
            'hash': Variable(uint256),
            'version': Variable(Type.int),
            'previous_hash': Variable(uint256),
            'merkle_root': Variable(uint256),
            'timestamp': Variable(Type.int),
            'nonce': Variable(Type.int),
            'index': Variable(Type.int),
            'next_consensus': Variable(UInt160Type.build()),
            'transaction_count': Variable(Type.int)
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
            self._constructor: Method = BlockMethod(self)
        return self._constructor

    @classmethod
    def build(cls, value: Any = None) -> Self:
        if value is None or cls._is_type_of(value):
            return _Block

    @classmethod
    def _is_type_of(cls, value: Any):
        return isinstance(value, BlockType)


_Block = BlockType()


class BlockMethod(IBuiltinMethod):

    def __init__(self, return_type: BlockType):
        identifier = '-Block__init__'
        args: dict[str, Variable] = {}
        super().__init__(identifier, args, return_type=return_type)

    def validate_parameters(self, *params: IExpression) -> bool:
        return len(params) == 0

    def generate_internal_opcodes(self, code_generator):
        from boa3.internal.neo3.core.types import UInt160, UInt256

        uint160_default = UInt160.zero().to_array()
        uint256_default = UInt256.zero().to_array()

        code_generator.convert_literal(0)  # transaction_count
        code_generator.convert_literal(uint160_default)  # next_consensus
        code_generator.convert_literal(0)  # index
        code_generator.convert_literal(0)  # nonce
        code_generator.convert_literal(0)  # timestamp
        code_generator.convert_literal(uint256_default)  # merkle_root
        code_generator.convert_literal(uint256_default)  # previous_hash
        code_generator.convert_literal(0)  # version
        code_generator.convert_literal(uint256_default)  # hash
        code_generator.convert_new_array(length=9, array_type=self.type)

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> str | None:
        return
