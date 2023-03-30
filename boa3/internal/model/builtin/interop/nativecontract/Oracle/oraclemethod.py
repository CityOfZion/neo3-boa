import ast
from typing import Dict, List

from boa3.internal.model.builtin.interop.nativecontract.Oracle.getoraclescripthashmethod import OracleContract
from boa3.internal.model.builtin.interop.nativecontract.nativecontractmethod import NativeContractMethod
from boa3.internal.model.type.itype import IType
from boa3.internal.model.variable import Variable


class OracleMethod(NativeContractMethod):

    def __init__(self, identifier: str, syscall: str, args: Dict[str, Variable] = None,
                 defaults: List[ast.AST] = None, return_type: IType = None,
                 internal_call_args: int = None):
        super().__init__(OracleContract.getter, identifier, syscall, args, defaults, return_type, internal_call_args)
