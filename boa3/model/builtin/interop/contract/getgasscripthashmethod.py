from typing import Dict, List, Optional, Tuple

from boa3.model.builtin.builtinproperty import IBuiltinProperty
from boa3.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.model.variable import Variable
from boa3.neo.vm.opcode.Opcode import Opcode


class GetGasScriptHashMethod(IBuiltinMethod):
    def __init__(self):
        from boa3.model.type.collection.sequence.uint160type import UInt160Type
        identifier = '-get_gas'
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

        value = b'\x66\x8e\x0c\x1f\x9d\x7b\x70\xa9\x9d\xd9\xe0\x6e\xad\xd4\xc7\x84\xd6\x41\xaf\xbc'
        return [
            (Opcode.PUSHDATA1, Integer(len(value)).to_byte_array() + value)
        ]


class GasProperty(IBuiltinProperty):
    def __init__(self):
        identifier = 'GAS'
        getter = GetGasScriptHashMethod()
        super().__init__(identifier, getter)
