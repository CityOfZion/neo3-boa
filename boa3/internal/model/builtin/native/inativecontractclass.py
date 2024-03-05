import abc

from boa3.internal.model.builtin.builtinproperty import IBuiltinProperty
from boa3.internal.model.method import Method
from boa3.internal.model.property import Property
from boa3.internal.model.type.classes.classarraytype import ClassArrayType
from boa3.internal.model.variable import Variable


class INativeContractClass(ClassArrayType, abc.ABC):
    def __init__(self, identifier: str, contract_hash_property: IBuiltinProperty):
        super().__init__(identifier)

        self._variables: dict[str, Variable] = {}
        self._class_methods: dict[str, Method] = {}
        self._constructor: Method = None
        self._properties = {
            'hash': contract_hash_property
        }

    @property
    def instance_variables(self) -> dict[str, Variable]:
        return self._variables.copy()

    @property
    def class_variables(self) -> dict[str, Variable]:
        return {}

    @property
    def properties(self) -> dict[str, Property]:
        return self._properties

    @property
    def static_methods(self) -> dict[str, Method]:
        return {}

    @property
    def class_methods(self) -> dict[str, Method]:
        return self._class_methods

    @property
    def instance_methods(self) -> dict[str, Method]:
        return {}

    def constructor_method(self) -> Method | None:
        return self._constructor
