from __future__ import annotations

from typing import Any, Dict, Optional

from boa3.internal.model.method import Method
from boa3.internal.model.property import Property
from boa3.internal.model.type.classes.classstructtype import ClassStructType
from boa3.internal.model.variable import Variable


class ContractGroupType(ClassStructType):
    """
    A class used to represent Neo ContractGroup class
    """

    def __init__(self):
        super().__init__('ContractGroup')
        from boa3.internal.model.type.collection.sequence.ecpointtype import ECPointType
        from boa3.internal.model.type.type import Type

        self._variables: Dict[str, Variable] = {
            'pubkey': Variable(ECPointType.build()),
            'signature': Variable(Type.bytes)
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
        return self._constructor

    @classmethod
    def build(cls, value: Any = None) -> ContractGroupType:
        if value is None or cls._is_type_of(value):
            return _ContractGroup

    @classmethod
    def _is_type_of(cls, value: Any):
        return isinstance(value, ContractGroupType)


_ContractGroup = ContractGroupType()
