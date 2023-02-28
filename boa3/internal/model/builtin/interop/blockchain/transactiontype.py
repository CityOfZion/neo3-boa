from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

from boa3.internal import constants
from boa3.internal.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.internal.model.expression import IExpression
from boa3.internal.model.method import Method
from boa3.internal.model.property import Property
from boa3.internal.model.type.classes.classarraytype import ClassArrayType
from boa3.internal.model.variable import Variable
from boa3.internal.neo.vm.opcode.Opcode import Opcode


class TransactionType(ClassArrayType):
    """
    A class used to represent Neo Transaction class
    """

    def __init__(self):
        super().__init__('Transaction')
        from boa3.internal.model.type.type import Type
        from boa3.internal.model.type.collection.sequence.uint160type import UInt160Type
        from boa3.internal.model.type.collection.sequence.uint256type import UInt256Type

        self._variables: Dict[str, Variable] = {
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
    def class_variables(self) -> Dict[str, Variable]:
        return {}

    @property
    def instance_variables(self) -> Dict[str, Variable]:
        return self._variables.copy()

    @property
    def properties(self) -> Dict[str, Property]:
        return {}

    @property
    def static_methods(self) -> Dict[str, Method]:
        return {}

    @property
    def class_methods(self) -> Dict[str, Method]:
        return {}

    @property
    def instance_methods(self) -> Dict[str, Method]:
        return {}

    def constructor_method(self) -> Optional[Method]:
        # was having a problem with recursive import
        if self._constructor is None:
            self._constructor: Method = TransactionMethod(self)
        return self._constructor

    @classmethod
    def build(cls, value: Any = None) -> TransactionType:
        if value is None or cls._is_type_of(value):
            return _Transaction

    @classmethod
    def _is_type_of(cls, value: Any):
        return isinstance(value, TransactionType)


_Transaction = TransactionType()


class TransactionMethod(IBuiltinMethod):

    def __init__(self, return_type: TransactionType):
        identifier = '-Transaction__init__'
        args: Dict[str, Variable] = {}
        super().__init__(identifier, args, return_type=return_type)

    def validate_parameters(self, *params: IExpression) -> bool:
        return len(params) == 0

    @property
    def _opcode(self) -> List[Tuple[Opcode, bytes]]:
        from boa3.internal.neo.vm.type.Integer import Integer

        uint160_default = Integer(constants.SIZE_OF_INT160).to_byte_array() + bytes(constants.SIZE_OF_INT160)
        uint256_default = Integer(constants.SIZE_OF_INT256).to_byte_array() + bytes(constants.SIZE_OF_INT256)

        return [
            (Opcode.PUSHDATA1, Integer(0).to_byte_array()),  # script
            (Opcode.PUSH0, b''),  # valid_until_block
            (Opcode.PUSH0, b''),  # network_fee
            (Opcode.PUSH0, b''),  # system_fee
            (Opcode.PUSHDATA1, uint160_default),  # sender
            (Opcode.PUSH0, b''),  # nonce
            (Opcode.PUSH0, b''),  # version
            (Opcode.PUSHDATA1, uint256_default),  # hash
            (Opcode.PUSH8, b''),
            (Opcode.PACK, b'')
        ]

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> Optional[str]:
        return
