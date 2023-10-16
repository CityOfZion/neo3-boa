from __future__ import annotations

from typing import Any, Dict, Optional

from boa3.internal.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.internal.model.expression import IExpression
from boa3.internal.model.method import Method
from boa3.internal.model.property import Property
from boa3.internal.model.type.classes.classarraytype import ClassArrayType
from boa3.internal.model.variable import Variable


class WitnessRuleType(ClassArrayType):
    """
    A class used to represent Neo WitnessRule class
    """

    def __init__(self):
        super().__init__('WitnessRule')
        from boa3.internal.model.builtin.interop.blockchain.witnessruleactiontype import WitnessRuleActionType
        from boa3.internal.model.builtin.interop.blockchain.witnessconditiontype import WitnessConditionType

        self._variables: Dict[str, Variable] = {
            'action': Variable(WitnessRuleActionType.build()),
            'condition': Variable(WitnessConditionType.build())
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
            self._constructor: Method = WitnessRuleMethod(self)
        return self._constructor

    @classmethod
    def build(cls, value: Any = None) -> WitnessRuleType:
        if value is None or cls._is_type_of(value):
            return _WitnessRule

    @classmethod
    def _is_type_of(cls, value: Any):
        return isinstance(value, WitnessRuleType)


_WitnessRule = WitnessRuleType()


class WitnessRuleMethod(IBuiltinMethod):

    def __init__(self, return_type: WitnessRuleType):
        identifier = '-WitnessRule__init__'
        args: Dict[str, Variable] = {}
        super().__init__(identifier, args, return_type=return_type)

    def validate_parameters(self, *params: IExpression) -> bool:
        return len(params) == 0

    def generate_internal_opcodes(self, code_generator):
        from boa3.internal.model.builtin.interop.blockchain.witnessconditiontype import WitnessConditionType
        from boa3.internal.model.builtin.interop.blockchain.witnessruleactiontype import WitnessRuleActionType

        code_generator.convert_builtin_method_call(WitnessConditionType.build().constructor_method(), is_internal=True)  # condition
        code_generator.convert_builtin_method_call(WitnessRuleActionType.build().constructor_method(), is_internal=True)  # action
        code_generator.convert_new_array(length=2, array_type=self.type)

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> Optional[str]:
        return
