from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

from boa3.internal.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.internal.model.expression import IExpression
from boa3.internal.model.method import Method
from boa3.internal.model.property import Property
from boa3.internal.model.type.classes.classarraytype import ClassArrayType
from boa3.internal.model.variable import Variable
from boa3.internal.neo.vm.opcode import OpcodeHelper
from boa3.internal.neo.vm.opcode.Opcode import Opcode


class NeoAccountStateType(ClassArrayType):
    """
    A class used to represent Neo NeoAccountState class
    """

    def __init__(self):
        super().__init__('NeoAccountState')
        from boa3.internal.model.type.type import Type
        from boa3.internal.model.type.collection.sequence.ecpointtype import ECPointType

        self._variables: Dict[str, Variable] = {
            'balance': Variable(Type.int),
            'height': Variable(Type.int),
            'vote_to': Variable(ECPointType.build()),
        }
        self._constructor: Optional[Method] = None

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
            self._constructor: Method = NeoAccountStateMethod(self)
        return self._constructor

    @classmethod
    def build(cls, value: Any = None) -> NeoAccountStateType:
        if value is None or cls._is_type_of(value):
            return _NeoAccountState

    @classmethod
    def _is_type_of(cls, value: Any):
        return isinstance(value, NeoAccountStateType)


_NeoAccountState = NeoAccountStateType()


class NeoAccountStateMethod(IBuiltinMethod):

    def __init__(self, return_type: NeoAccountStateType):
        identifier = '-NeoAccountState__init__'
        args: Dict[str, Variable] = {}
        super().__init__(identifier, args, return_type=return_type)

    def validate_parameters(self, *params: IExpression) -> bool:
        return len(params) == 0

    @property
    def _opcode(self) -> List[Tuple[Opcode, bytes]]:
        from boa3.internal.model.type.collection.sequence.ecpointtype import ECPointType
        return [
            OpcodeHelper.get_pushdata_and_data(ECPointType.build().default_value),  # vote_to
            (Opcode.PUSH0, b''),  # height
            (Opcode.PUSH0, b''),  # balance
            (Opcode.PUSH3, b''),
            (Opcode.PACK, b'')
        ]

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> Optional[str]:
        return
