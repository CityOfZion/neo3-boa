from __future__ import annotations

from typing import Any, Dict

from boa3.internal.model.builtin.interop.nativecontract import StdLibContract
from boa3.internal.model.builtin.native.inativecontractclass import INativeContractClass
from boa3.internal.model.method import Method


class StdLibClass(INativeContractClass):
    """
    A class used to represent StdLib native contract
    """

    def __init__(self):
        super().__init__('StdLib', StdLibContract)

    @property
    def class_methods(self) -> Dict[str, Method]:
        # avoid recursive import
        from boa3.internal.model.builtin.interop.interop import Interop

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
        return super().class_methods

    @classmethod
    def build(cls, value: Any = None) -> StdLibClass:
        if value is None or cls._is_type_of(value):
            return _StdLib

    @classmethod
    def _is_type_of(cls, value: Any):
        return isinstance(value, StdLibClass)


_StdLib = StdLibClass()
