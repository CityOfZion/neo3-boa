import ast
from typing import Dict, List

from boa3.model.builtin.interop.nativecontract.Oracle.getoraclescripthashmethod import OracleContract
from boa3.model.builtin.interop.nativecontract.nativecontractmethod import NativeContractMethod
from boa3.model.type.itype import IType
from boa3.model.variable import Variable


class OracleMethod(NativeContractMethod):

    def __init__(self, identifier: str, syscall: str, args: Dict[str, Variable] = None,
                 defaults: List[ast.AST] = None, return_type: IType = None):
        super().__init__(OracleContract.getter, identifier, syscall, args, defaults, return_type)
