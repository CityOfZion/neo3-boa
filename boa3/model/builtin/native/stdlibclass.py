from __future__ import annotations

from typing import Any, Dict, Optional

from boa3.model.method import Method
from boa3.model.property import Property
from boa3.model.type.classes.classarraytype import ClassArrayType
from boa3.model.variable import Variable


class StdLibClass(ClassArrayType):
    """
    A class used to represent StdLib native contract
    """

    def __init__(self):
        super().__init__('StdLib')

        self._variables: Dict[str, Variable] = {}
        self._class_methods: Dict[str, Method] = {}
        self._constructor: Optional[Method] = None

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
        # avoid recursive import
        from boa3.model.builtin.interop.stdlib import (SerializeMethod, DeserializeMethod,
                                                       Base64DecodeMethod, Base64EncodeMethod,
                                                       Base58DecodeMethod, Base58EncodeMethod,
                                                       Base58CheckDecodeMethod, Base58CheckEncodeMethod,
                                                       ItoaMethod, AtoiMethod,
                                                       MemoryCompareMethod, MemorySearchMethod)
        from boa3.model.builtin.interop.json import (JsonDeserializeMethod, JsonSerializeMethod)

        if len(self._class_methods) == 0:
            self._class_methods = {
                'serialize': SerializeMethod(),
                'deserialize': DeserializeMethod(),
                'json_serialize': JsonSerializeMethod(),
                'json_deserialize': JsonDeserializeMethod(),
                'base64_decode': Base64DecodeMethod(),
                'base64_encode': Base64EncodeMethod(),
                'base58_decode': Base58DecodeMethod(),
                'base58_encode': Base58EncodeMethod(),
                'base58_check_decode': Base58CheckDecodeMethod(),
                'base58_check_encode': Base58CheckEncodeMethod(),
                'itoa': ItoaMethod(),
                'atoi': AtoiMethod(),
                'memory_compare': MemoryCompareMethod(),
                'memory_search': MemorySearchMethod(),
            }
        return self._class_methods

    @property
    def instance_methods(self) -> Dict[str, Method]:
        return {}

    def constructor_method(self) -> Optional[Method]:
        return self._constructor

    @classmethod
    def build(cls, value: Any = None) -> StdLibClass:
        if value is None or cls._is_type_of(value):
            return _StdLib

    @classmethod
    def _is_type_of(cls, value: Any):
        return isinstance(value, StdLibClass)


_StdLib = StdLibClass()
