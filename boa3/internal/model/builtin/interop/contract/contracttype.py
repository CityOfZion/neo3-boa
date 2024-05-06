from typing import Any, Self

from boa3.internal.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.internal.model.expression import IExpression
from boa3.internal.model.method import Method
from boa3.internal.model.property import Property
from boa3.internal.model.type.classes.classarraytype import ClassArrayType
from boa3.internal.model.variable import Variable


class ContractType(ClassArrayType):
    """
    A class used to represent Neo Contract class
    """

    def __init__(self):
        super().__init__('Contract')
        from boa3.internal.model.builtin.interop.contract.contractmanifest import ContractManifestType
        from boa3.internal.model.type.type import Type
        from boa3.internal.model.type.collection.sequence.uint160type import UInt160Type

        self._variables: dict[str, Variable] = {
            'id': Variable(Type.int),
            'update_counter': Variable(Type.int),
            'hash': Variable(UInt160Type.build()),
            'nef': Variable(Type.bytes),
            'manifest': Variable(ContractManifestType.build())
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
            self._constructor: Method = ContractMethod(self)
        return self._constructor

    @classmethod
    def build(cls, value: Any = None) -> Self:
        if value is None or cls._is_type_of(value):
            return _Contract

    @classmethod
    def _is_type_of(cls, value: Any):
        return isinstance(value, ContractType)


_Contract = ContractType()


class ContractMethod(IBuiltinMethod):

    def __init__(self, return_type: ContractType):
        identifier = '-Contract__init__'
        args: dict[str, Variable] = {}
        super().__init__(identifier, args, return_type=return_type)

    def validate_parameters(self, *params: IExpression) -> bool:
        return len(params) == 0

    def generate_internal_opcodes(self, code_generator):
        from boa3.internal.model.builtin.interop.contract.contractmanifest import ContractManifestType
        from boa3.internal.neo3.core.types import UInt160

        uint160_default = UInt160.zero().to_array()

        code_generator.convert_new_map(ContractManifestType.build())  # manifest
        code_generator.convert_literal(b'')  # nef
        code_generator.convert_literal(uint160_default)  # hash
        code_generator.convert_literal(0)  # update_counter
        code_generator.convert_literal(0)  # id
        code_generator.convert_new_array(length=5, array_type=self.type)

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> str | None:
        return
