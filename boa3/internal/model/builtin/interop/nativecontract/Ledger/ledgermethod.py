import ast

from boa3.internal.model.builtin.interop.nativecontract.Ledger.getledgerscripthashmethod import LedgerContract
from boa3.internal.model.builtin.interop.nativecontract.nativecontractmethod import NativeContractMethod
from boa3.internal.model.type.itype import IType
from boa3.internal.model.variable import Variable


class LedgerMethod(NativeContractMethod):

    def __init__(self, identifier: str, native_identifier: str, args: dict[str, Variable] = None,
                 defaults: list[ast.AST] = None, return_type: IType = None,
                 internal_call_args: int = None):
        super().__init__(LedgerContract.getter, identifier, native_identifier,
                         args, defaults, return_type, internal_call_args)
