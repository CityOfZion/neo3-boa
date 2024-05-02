from typing import Any, Self

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

        self._variables: dict[str, Variable] = {}
        self._instance_methods: dict[str, Method] = {}
        self._constructor: Method = None

    @property
    def instance_variables(self) -> dict[str, Variable]:
        return self._variables.copy()

    @property
    def class_variables(self) -> dict[str, Variable]:
        return {}

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

    def constructor_method(self) -> Method | None:
        return self._constructor

    @classmethod
    def build(cls, value: Any = None) -> Self:
        if value is None or cls._is_type_of(value):
            return _StorageContext

    @classmethod
    def _is_type_of(cls, value: Any):
        return isinstance(value, StorageContextType)


_StorageContext = StorageContextType()
