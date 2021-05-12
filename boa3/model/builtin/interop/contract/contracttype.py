from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

from boa3.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.model.expression import IExpression
from boa3.model.method import Method
from boa3.model.property import Property
from boa3.model.type.classtype import ClassType
from boa3.model.variable import Variable
from boa3.neo.vm.opcode.Opcode import Opcode


class ContractType(ClassType):
    """
    A class used to represent Neo Contract class
    """

    def __init__(self):
        super().__init__('Contract')
        from boa3.model.type.type import Type
        from boa3.model.type.collection.sequence.uint160type import UInt160Type

        self._variables: Dict[str, Variable] = {
            'id': Variable(Type.int),
            'update_counter': Variable(Type.int),
            'hash': Variable(UInt160Type.build()),
            'nef': Variable(Type.bytes),
            'manifest': Variable(Type.dict)
        }
        self._constructor: Method = None

    @property
    def variables(self) -> Dict[str, Variable]:
        return self._variables.copy()

    @property
    def properties(self) -> Dict[str, Property]:
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
            self._constructor: Method = ContractMethod(self)
        return self._constructor

    @classmethod
    def build(cls, value: Any = None) -> ContractType:
        if value is None or cls._is_type_of(value):
            return _Contract

    @classmethod
    def _is_type_of(cls, value: Any):
        return isinstance(value, ContractType)


_Contract = ContractType()


class ContractMethod(IBuiltinMethod):

    def __init__(self, return_type: ContractType):
        identifier = '-Contract__init__'
        args: Dict[str, Variable] = {}
        super().__init__(identifier, args, return_type=return_type)

    def validate_parameters(self, *params: IExpression) -> bool:
        return len(params) == 0

    @property
    def opcode(self) -> List[Tuple[Opcode, bytes]]:
        from boa3.neo.vm.type.Integer import Integer
        return [
            (Opcode.NEWMAP, b''),
            (Opcode.PUSHDATA1, Integer(0).to_byte_array()),
            (Opcode.PUSHDATA1, Integer(20).to_byte_array() + bytes(20)),
            (Opcode.PUSH0, b''),
            (Opcode.PUSH0, b''),
            (Opcode.PUSH5, b''),
            (Opcode.PACK, b'')
        ]

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> Optional[str]:
        return
