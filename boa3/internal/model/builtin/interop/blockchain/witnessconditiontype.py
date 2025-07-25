from typing import Any, Self

from boa3.internal.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.internal.model.expression import IExpression
from boa3.internal.model.method import Method
from boa3.internal.model.property import Property
from boa3.internal.model.type.classes.classarraytype import ClassArrayType
from boa3.internal.model.variable import Variable


class WitnessConditionType(ClassArrayType):
    """
    A class used to represent Neo WitnessCondition class
    """

    def __init__(self):
        super().__init__('WitnessCondition')
        from boa3.internal.model.builtin.interop.blockchain.witnessconditionenumtype import \
            WitnessConditionTypeType as WitnessConditionEnum

        self._variables: dict[str, Variable] = {
            'type': Variable(WitnessConditionEnum.build())
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
            self._constructor: Method = WitnessConditionMethod(self)
        return self._constructor

    @classmethod
    def build(cls, value: Any = None) -> Self:
        if value is None or cls._is_type_of(value):
            return _WitnessCondition

    @classmethod
    def _is_type_of(cls, value: Any):
        return isinstance(value, WitnessConditionType)


_WitnessCondition = WitnessConditionType()


class WitnessConditionMethod(IBuiltinMethod):

    def __init__(self, return_type: WitnessConditionType):
        identifier = '-WitnessCondition__init__'
        args: dict[str, Variable] = {}
        super().__init__(identifier, args, return_type=return_type)

    def validate_parameters(self, *params: IExpression) -> bool:
        return len(params) == 0

    def generate_internal_opcodes(self, code_generator):
        from boa3.internal.model.builtin.interop.blockchain.witnessconditionenumtype import \
            WitnessConditionTypeType as WitnessConditionEnum

        code_generator.convert_literal(WitnessConditionEnum.build().default_value)  # type
        code_generator.convert_new_array(length=1, array_type=self.type)

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> str | None:
        return
