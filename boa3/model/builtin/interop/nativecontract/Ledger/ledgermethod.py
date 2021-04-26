import ast
from typing import Dict, List

from boa3.model.builtin.interop.nativecontract.Ledger.getledgerscripthashmethod import LedgerContract
from boa3.model.builtin.interop.nativecontract.nativecontractmethod import NativeContractMethod
from boa3.model.type.itype import IType
from boa3.model.variable import Variable


class LedgerMethod(NativeContractMethod):

    def __init__(self, identifier: str, native_identifier: str, args: Dict[str, Variable] = None,
                 defaults: List[ast.AST] = None, return_type: IType = None):
        super().__init__(LedgerContract.getter, identifier, native_identifier, args, defaults, return_type)
