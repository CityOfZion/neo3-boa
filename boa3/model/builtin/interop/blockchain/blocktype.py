from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

from boa3 import constants
from boa3.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.model.expression import IExpression
from boa3.model.method import Method
from boa3.model.property import Property
from boa3.model.type.classes.classarraytype import ClassArrayType
from boa3.model.variable import Variable
from boa3.neo.vm.opcode.Opcode import Opcode


class BlockType(ClassArrayType):
    """
    A class used to represent Neo Block class
    """

    def __init__(self):
        super().__init__('Block')
        from boa3.model.type.type import Type
        from boa3.model.type.collection.sequence.uint160type import UInt160Type
        from boa3.model.type.collection.sequence.uint256type import UInt256Type

        uint256 = UInt256Type.build()

        self._variables: Dict[str, Variable] = {
            'hash': Variable(uint256),
            'version': Variable(Type.int),
            'previous_hash': Variable(uint256),
            'merkle_root': Variable(uint256),
            'timestamp': Variable(Type.int),
            'nonce': Variable(Type.int),
            'index': Variable(Type.int),
            'primary_index': Variable(Type.int),
            'next_consensus': Variable(UInt160Type.build()),
            'transaction_count': Variable(Type.int)
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
            self._constructor: Method = BlockMethod(self)
        return self._constructor

    @classmethod
    def build(cls, value: Any = None) -> BlockType:
        if value is None or cls._is_type_of(value):
            return _Block

    @classmethod
    def _is_type_of(cls, value: Any):
        return isinstance(value, BlockType)


_Block = BlockType()


class BlockMethod(IBuiltinMethod):

    def __init__(self, return_type: BlockType):
        identifier = '-Block__init__'
        args: Dict[str, Variable] = {}
        super().__init__(identifier, args, return_type=return_type)

    def validate_parameters(self, *params: IExpression) -> bool:
        return len(params) == 0

    @property
    def opcode(self) -> List[Tuple[Opcode, bytes]]:
        from boa3.neo.vm.type.Integer import Integer

        uint160_default = Integer(constants.SIZE_OF_INT160).to_byte_array() + bytes(constants.SIZE_OF_INT160)
        uint256_default = Integer(constants.SIZE_OF_INT256).to_byte_array() + bytes(constants.SIZE_OF_INT256)

        return [
            (Opcode.PUSH0, b''),  # transaction_count
            (Opcode.PUSHDATA1, uint160_default),  # next_consensus
            (Opcode.PUSH0, b''),  # primary_index
            (Opcode.PUSH0, b''),  # index
            (Opcode.PUSH0, b''),  # nonce
            (Opcode.PUSH0, b''),  # timestamp
            (Opcode.PUSHDATA1, uint256_default),  # merkle_root
            (Opcode.PUSHDATA1, uint256_default),  # previous_hash
            (Opcode.PUSH0, b''),  # version
            (Opcode.PUSHDATA1, uint256_default),  # hash
            (Opcode.PUSH10, b''),
            (Opcode.PACK, b'')
        ]

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> Optional[str]:
        return
