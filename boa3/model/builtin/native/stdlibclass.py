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
        from boa3.model.builtin.interop.interop import Interop

        if len(self._class_methods) == 0:
            self._class_methods = {
                'serialize': Interop.Serialize,
                'deserialize': Interop.Deserialize,
                'json_serialize': Interop.JsonSerialize,
                'json_deserialize': Interop.JsonDeserialize,
                'base64_decode': Interop.Base64Decode,
                'base64_encode': Interop.Base64Encode,
                'base58_decode': Interop.Base58Decode,
                'base58_encode': Interop.Base58Encode,
                'base58_check_decode': Interop.Base58CheckDecode,
                'base58_check_encode': Interop.Base58CheckEncode,
                'itoa': Interop.Itoa,
                'atoi': Interop.Atoi,
                'memory_compare': Interop.MemoryCompare,
                'memory_search': Interop.MemorySearch,
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
