import ast
from typing import Dict, List

from boa3.model.builtin.interop.nativecontract.Nep17.getnep17scripthashmethod import GetNep17ScriptHashMethod, \
    Nep17Contract
from boa3.model.builtin.interop.nativecontract.nativecontractmethod import NativeContractMethod
from boa3.model.type.itype import IType
from boa3.model.variable import Variable


class Nep17Method(NativeContractMethod):

    def __init__(self, identifier: str, syscall: str, args: Dict[str, Variable] = None,
                 defaults: List[ast.AST] = None, return_type: IType = None, script_hash: bytes = None):
        contract = Nep17Contract if script_hash is None else GetNep17ScriptHashMethod(script_hash)
        super().__init__(contract, identifier, syscall, args, defaults, return_type)
