import abc
from typing import Dict, Optional

from boa3.internal.model.builtin.builtinproperty import IBuiltinProperty
from boa3.internal.model.method import Method
from boa3.internal.model.property import Property
from boa3.internal.model.type.classes.classarraytype import ClassArrayType
from boa3.internal.model.variable import Variable


class INativeContractClass(ClassArrayType, abc.ABC):
    def __init__(self, identifier: str, contract_hash_property: IBuiltinProperty):
        super().__init__(identifier)

        self._variables: Dict[str, Variable] = {}
        self._class_methods: Dict[str, Method] = {}
        self._constructor: Method = None
        self._properties = {
            'hash': contract_hash_property
        }

    @property
    def instance_variables(self) -> Dict[str, Variable]:
        return self._variables.copy()

    @property
    def class_variables(self) -> Dict[str, Variable]:
        return {}

    @property
    def properties(self) -> Dict[str, Property]:
        return self._properties

    @property
    def static_methods(self) -> Dict[str, Method]:
        return {}

    @property
    def class_methods(self) -> Dict[str, Method]:
        return self._class_methods

    @property
    def instance_methods(self) -> Dict[str, Method]:
        return {}

    def constructor_method(self) -> Optional[Method]:
        return self._constructor
