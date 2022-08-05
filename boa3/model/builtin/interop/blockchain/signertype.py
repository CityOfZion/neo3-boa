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


class SignerType(ClassArrayType):
    """
    A class used to represent Neo Signer class
    """

    def __init__(self):
        super().__init__('Signer')
        from boa3.model.builtin.interop.blockchain.witnessscopeenumtype import WitnessScopeType
        from boa3.model.builtin.interop.blockchain.witnessruletype import WitnessRuleType
        from boa3.model.type.type import Type
        from boa3.model.type.collection.sequence.uint160type import UInt160Type

        uint160 = UInt160Type.build()
        list_uint160 = Type.list.build([uint160])

        self._variables: Dict[str, Variable] = {
            'account': Variable(uint160),
            'scopes': Variable(WitnessScopeType.build()),
            'allowed_contracts': Variable(list_uint160),
            'allowed_groups': Variable(list_uint160),
            'rules': Variable(Type.list.build([WitnessRuleType.build()]))
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
            self._constructor: Method = SignerMethod(self)
        return self._constructor

    @classmethod
    def build(cls, value: Any = None) -> SignerType:
        if value is None or cls._is_type_of(value):
            return _Signer

    @classmethod
    def _is_type_of(cls, value: Any):
        return isinstance(value, SignerType)


_Signer = SignerType()


class SignerMethod(IBuiltinMethod):

    def __init__(self, return_type: SignerType):
        identifier = '-Signer__init__'
        args: Dict[str, Variable] = {}
        super().__init__(identifier, args, return_type=return_type)

    def validate_parameters(self, *params: IExpression) -> bool:
        return len(params) == 0

    @property
    def opcode(self) -> List[Tuple[Opcode, bytes]]:
        from boa3.neo.vm.type.Integer import Integer

        uint160_default = Integer(constants.SIZE_OF_INT160).to_byte_array() + bytes(constants.SIZE_OF_INT160)

        return [
            (Opcode.NEWARRAY0, b''),  # rules
            (Opcode.NEWARRAY0, b''),  # allowed_groups
            (Opcode.NEWARRAY0, b''),  # allowed_contracts
            (Opcode.PUSH0, b''),  # scopes
            (Opcode.PUSHDATA1, uint160_default),  # account
            (Opcode.PUSH5, b''),
            (Opcode.PACK, b'')
        ]

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> Optional[str]:
        return
