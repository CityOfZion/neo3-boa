from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

from boa3.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.model.expression import IExpression
from boa3.model.method import Method
from boa3.model.property import Property
from boa3.model.type.classes.classarraytype import ClassArrayType
from boa3.model.variable import Variable
from boa3.neo.vm.opcode.Opcode import Opcode


class WitnessConditionType(ClassArrayType):
    """
    A class used to represent Neo WitnessCondition class
    """

    def __init__(self):
        super().__init__('WitnessCondition')
        from boa3.model.builtin.interop.blockchain.witnessconditionenumtype import WitnessConditionType as WitnessConditionEnum

        self._variables: Dict[str, Variable] = {
            'type': Variable(WitnessConditionEnum.build())
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
            self._constructor: Method = WitnessConditionMethod(self)
        return self._constructor

    @classmethod
    def build(cls, value: Any = None) -> WitnessConditionType:
        if value is None or cls._is_type_of(value):
            return _WitnessCondition

    @classmethod
    def _is_type_of(cls, value: Any):
        return isinstance(value, WitnessConditionType)


_WitnessCondition = WitnessConditionType()


class WitnessConditionMethod(IBuiltinMethod):

    def __init__(self, return_type: WitnessConditionType):
        identifier = '-WitnessCondition__init__'
        args: Dict[str, Variable] = {}
        super().__init__(identifier, args, return_type=return_type)

    def validate_parameters(self, *params: IExpression) -> bool:
        return len(params) == 0

    @property
    def opcode(self) -> List[Tuple[Opcode, bytes]]:
        from boa3.model.builtin.interop.blockchain.witnessconditionenumtype import WitnessConditionType as WitnessConditionEnum

        return [
            Opcode.get_push_and_data(WitnessConditionEnum.build().default_value),  # type
            (Opcode.PUSH1, b''),
            (Opcode.PACK, b'')
        ]

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> Optional[str]:
        return
