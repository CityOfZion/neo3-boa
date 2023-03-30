from __future__ import annotations

from typing import Any, Dict, Optional

from boa3.internal.model.builtin.interop.interopinterfacetype import InteropInterfaceType
from boa3.internal.model.method import Method
from boa3.internal.model.property import Property
from boa3.internal.model.variable import Variable


class StorageContextType(InteropInterfaceType):
    """
    A class used to represent Neo StorageContext class
    """

    def __init__(self):
        super().__init__('StorageContext')

        self._variables: Dict[str, Variable] = {}
        self._instance_methods: Dict[str, Method] = {}
        self._constructor: Method = None

    @property
    def instance_variables(self) -> Dict[str, Variable]:
        return self._variables.copy()

    @property
    def class_variables(self) -> Dict[str, Variable]:
        return {}

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
        # avoid recursive import
        if len(self._instance_methods) == 0:
            from boa3.internal.model.builtin.interop.storage.storagecontext.storagecontextcreatemapmethod import \
                StorageContextCreateMapMethod
            from boa3.internal.model.builtin.interop.storage.storagecontext.storagecontextasreadonlymethod import \
                StorageContextAsReadOnlyMethod

            self._instance_methods = {
                'create_map': StorageContextCreateMapMethod(),
                'as_read_only': StorageContextAsReadOnlyMethod()
            }
        return self._instance_methods

    def constructor_method(self) -> Optional[Method]:
        return self._constructor

    @classmethod
    def build(cls, value: Any = None) -> StorageContextType:
        if value is None or cls._is_type_of(value):
            return _StorageContext

    @classmethod
    def _is_type_of(cls, value: Any):
        return isinstance(value, StorageContextType)


_StorageContext = StorageContextType()
