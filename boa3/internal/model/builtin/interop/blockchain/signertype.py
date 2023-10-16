from __future__ import annotations

from typing import Any, Dict, Optional

from boa3.internal.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.internal.model.expression import IExpression
from boa3.internal.model.method import Method
from boa3.internal.model.property import Property
from boa3.internal.model.type.classes.classarraytype import ClassArrayType
from boa3.internal.model.variable import Variable


class SignerType(ClassArrayType):
    """
    A class used to represent Neo Signer class
    """

    def __init__(self):
        super().__init__('Signer')
        from boa3.internal.model.builtin.interop.blockchain.witnessscopeenumtype import WitnessScopeType
        from boa3.internal.model.builtin.interop.blockchain.witnessruletype import WitnessRuleType
        from boa3.internal.model.type.type import Type
        from boa3.internal.model.type.collection.sequence.uint160type import UInt160Type

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

    def generate_internal_opcodes(self, code_generator):
        from boa3.internal.neo3.core.types import UInt160

        uint160_default = UInt160.zero().to_array()

        code_generator.convert_literal([])  # rules
        code_generator.convert_literal([])  # allowed_groups
        code_generator.convert_literal([])  # allowed_contracts
        code_generator.convert_literal(0)  # scopes
        code_generator.convert_literal(uint160_default)  # account
        code_generator.convert_new_array(length=5, array_type=self.type)

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> Optional[str]:
        return
