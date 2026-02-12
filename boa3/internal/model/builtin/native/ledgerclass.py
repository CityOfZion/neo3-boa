from typing import Any, Self

from boa3.internal.model.builtin.interop.nativecontract import LedgerContract
from boa3.internal.model.builtin.native import ledger_methods as lm
from boa3.internal.model.builtin.native.inativecontractclass import INativeContractClass
from boa3.internal.model.method import Method


class LedgerClass(INativeContractClass):
    """
    A class used to represent Ledger native contract
    """

    def __init__(self):
        super().__init__('LedgerContract', LedgerContract)

    @property
    def class_methods(self) -> dict[str, Method]:
        # avoid recursive import
        from boa3.internal.model.builtin.interop.interop import Interop

        if len(self._class_methods) == 0:
            self._class_methods = {
                'get_block': lm.GetBlockMethod(Interop.BlockType),
                'get_current_index': lm.CurrentIndexProperty().getter,
                'get_current_hash': lm.CurrentHashProperty().getter,
                'get_transaction': lm.GetTransactionMethod(Interop.TransactionType),
                'get_transaction_from_block': lm.GetTransactionFromBlockMethod(Interop.TransactionType),
                'get_transaction_height': lm.GetTransactionHeightMethod(),
                'get_transaction_signers': lm.GetTransactionSignersMethod(Interop.SignerType),
                'get_transaction_vm_state': lm.GetTransactionVMStateMethod(Interop.VMStateType)
            }
        return super().class_methods

    @classmethod
    def build(cls, value: Any = None) -> Self:
        if value is None or cls._is_type_of(value):
            return _Ledger

    @classmethod
    def _is_type_of(cls, value: Any):
        return isinstance(value, LedgerClass)


_Ledger = LedgerClass()
