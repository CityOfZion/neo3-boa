from typing import Dict, List, Optional, Tuple

from boa3.model.builtin.builtinproperty import IBuiltinProperty
from boa3.model.builtin.interop.contractgethashmethod import ContractGetHashMethod
from boa3.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.model.variable import Variable
from boa3.neo.vm.opcode.Opcode import Opcode


class GetStdLibScriptHashMethod(ContractGetHashMethod):
    def __init__(self):
        from boa3.constants import STD_LIB_SCRIPT
        from boa3.model.type.collection.sequence.uint160type import UInt160Type
        identifier = '-get_std_lib_contract'
        args: Dict[str, Variable] = {}
        super().__init__(STD_LIB_SCRIPT, identifier, args, return_type=UInt160Type.build())

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> Optional[str]:
        return None

    @property
    def _opcode(self) -> List[Tuple[Opcode, bytes]]:
        from boa3.neo.vm.type.Integer import Integer

        value = self.script_hash
        return [
            (Opcode.PUSHDATA1, Integer(len(value)).to_byte_array() + value)
        ]


class StdLibProperty(IBuiltinProperty):
    def __init__(self):
        identifier = 'StdLib'
        getter = GetStdLibScriptHashMethod()
        super().__init__(identifier, getter)


StdLibContract = StdLibProperty()
