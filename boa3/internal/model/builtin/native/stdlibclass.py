from typing import Any, Self

from boa3.internal.model.builtin.interop.nativecontract import StdLibContract
from boa3.internal.model.builtin.native import stdlib
from boa3.internal.model.builtin.native.inativecontractclass import INativeContractClass
from boa3.internal.model.method import Method


class StdLibClass(INativeContractClass):
    """
    A class used to represent StdLib native contract
    """

    def __init__(self):
        super().__init__('StdLib', StdLibContract)

    @property
    def class_methods(self) -> dict[str, Method]:

        if len(self._class_methods) == 0:
            self._class_methods = {
                'serialize': stdlib.SerializeMethod(),
                'deserialize': stdlib.DeserializeMethod(),
                'json_serialize': stdlib.JsonSerializeMethod(),
                'json_deserialize': stdlib.JsonDeserializeMethod(),
                'base64_decode': stdlib.Base64DecodeMethod(),
                'base64_encode': stdlib.Base64EncodeMethod(),
                'base58_decode': stdlib.Base58DecodeMethod(),
                'base58_encode': stdlib.Base58EncodeMethod(),
                'base58_check_decode': stdlib.Base58CheckDecodeMethod(),
                'base58_check_encode': stdlib.Base58CheckEncodeMethod(),
                'hex_decode': stdlib.HexDecodeMethod(),
                'hex_encode': stdlib.HexEncodeMethod(),
                'itoa': stdlib.ItoaMethod(),
                'atoi': stdlib.AtoiMethod(),
                'memory_compare': stdlib.MemoryCompareMethod(),
                'memory_search': stdlib.MemorySearchMethod(),
                'string_split': stdlib.StringSplitMethod(),
                'str_len': stdlib.StrLenMethod(),
            }
        return super().class_methods

    @property
    def json_serialize(self) -> Method:
        return self.class_methods['json_serialize']

    @property
    def base58_decode(self) -> Method:
        return self.class_methods['base58_decode']

    @property
    def itoa(self) -> Method:
        return self.class_methods['itoa']

    @property
    def deserialize(self) -> Method:
        return self.class_methods['deserialize']

    @property
    def memory_compare(self) -> Method:
        return self.class_methods['memory_compare']

    @property
    def serialize(self) -> Method:
        return self.class_methods['serialize']

    @classmethod
    def build(cls, value: Any = None) -> Self:
        if value is None or cls._is_type_of(value):
            return _StdLib

    @classmethod
    def _is_type_of(cls, value: Any):
        return isinstance(value, StdLibClass)


_StdLib = StdLibClass()
