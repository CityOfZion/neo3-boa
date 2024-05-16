from typing import Any, Self

from boa3.internal.model.builtin.interop.nativecontract import PolicyContract
from boa3.internal.model.builtin.native.inativecontractclass import INativeContractClass
from boa3.internal.model.method import Method


class PolicyClass(INativeContractClass):
    """
    A class used to represent Policy native contract
    """

    def __init__(self):
        super().__init__('PolicyContract', PolicyContract)

    @property
    def class_methods(self) -> dict[str, Method]:
        # avoid recursive import
        from boa3.internal.model.builtin.interop.interop import Interop

        if len(self._class_methods) == 0:
            self._class_methods = {
                'get_fee_per_byte': Interop.GetFeePerByte,
                'get_exec_fee_factor': Interop.GetExecFeeFactor,
                'get_storage_price': Interop.GetStoragePrice,
                'get_attribute_fee': Interop.GetAttributeFee,
                'is_blocked': Interop.IsBlocked,
                'set_attribute_fee': Interop.SetAttributeFee,
            }
        return super().class_methods

    @classmethod
    def build(cls, value: Any = None) -> Self:
        if value is None or cls._is_type_of(value):
            return _Policy

    @classmethod
    def _is_type_of(cls, value: Any):
        return isinstance(value, PolicyClass)


_Policy = PolicyClass()
