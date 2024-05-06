from typing import Any, Self

from boa3.internal.model.builtin.interop.nativecontract import LedgerContract
from boa3.internal.model.builtin.native.inativecontractclass import INativeContractClass
from boa3.internal.model.method import Method


class LedgerClass(INativeContractClass):
    """
    A class used to represent Ledger native contract
    """

    def __init__(self):
        super().__init__('Ledger', LedgerContract)

    @property
    def class_methods(self) -> dict[str, Method]:
        # avoid recursive import
        from boa3.internal.model.builtin.interop.interop import Interop

        if len(self._class_methods) == 0:
            self._class_methods = {
                'get_block': Interop.GetBlock,
                'get_current_index': Interop.CurrentIndex.getter,
                'get_transaction': Interop.GetTransaction,
                'get_transaction_from_block': Interop.GetTransactionFromBlock,
                'get_transaction_height': Interop.GetTransactionHeight,
                'get_transaction_signers': Interop.GetTransactionSigners,
                'get_transaction_vm_state': Interop.GetTransactionVMState
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
