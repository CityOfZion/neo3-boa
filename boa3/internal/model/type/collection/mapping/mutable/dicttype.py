from typing import Any

from boa3.internal.model.type.collection.mapping.mutable.mutablemappingtype import MutableMappingType
from boa3.internal.model.type.itype import IType


class DictType(MutableMappingType):
    """
    A class used to represent Python dict type
    """

    def __init__(self, keys_type: set[IType] = None, values_type: set[IType] = None):
        identifier = 'dict'
        keys_type = self.filter_types(keys_type)
        values_type = self.filter_types(values_type)
        super().__init__(identifier, keys_type, values_type)

    @property
    def default_value(self) -> Any:
        return dict()

    @classmethod
    def _is_type_of(cls, value: Any):
        return type(value) in [dict, DictType]

    def _init_class_symbols(self):
        super()._init_class_symbols()

        from boa3.internal.model.builtin.builtin import Builtin

        instance_methods = [Builtin.Copy,
                            Builtin.DictKeys,
                            Builtin.DictValues,
                            Builtin.DictPop,
                            Builtin.DictPopDefault,
                            ]

        for instance_method in instance_methods:
            self._instance_methods[instance_method.raw_identifier] = instance_method.build(self)

    def __hash__(self):
        return hash(self.identifier)
