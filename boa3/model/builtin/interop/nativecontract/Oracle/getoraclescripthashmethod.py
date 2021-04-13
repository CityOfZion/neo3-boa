from typing import Dict, List, Optional, Tuple

from boa3.constants import ORACLE_SCRIPT
from boa3.model.builtin.builtinproperty import IBuiltinProperty
from boa3.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.model.variable import Variable
from boa3.neo.vm.opcode.Opcode import Opcode


class GetOracleScriptHashMethod(IBuiltinMethod):
    def __init__(self):
        from boa3.model.type.collection.sequence.uint160type import UInt160Type
        identifier = '-get_oracle_contract'
        args: Dict[str, Variable] = {}
        super().__init__(identifier, args, return_type=UInt160Type.build())

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> Optional[str]:
        return None

    @property
    def opcode(self) -> List[Tuple[Opcode, bytes]]:
        from boa3.neo.vm.type.Integer import Integer

        value = ORACLE_SCRIPT
        return [
            (Opcode.PUSHDATA1, Integer(len(value)).to_byte_array() + value)
        ]


class OracleProperty(IBuiltinProperty):
    def __init__(self):
        identifier = 'Oracle'
        getter = GetOracleScriptHashMethod()
        super().__init__(identifier, getter)


OracleContract = OracleProperty()
