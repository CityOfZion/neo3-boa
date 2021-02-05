import ast
from typing import Dict, List, Tuple

from boa3.model.builtin.interop.interopmethod import InteropMethod
from boa3.model.variable import Variable
from boa3.neo.vm.opcode.Opcode import Opcode


class CallMethod(InteropMethod):

    def __init__(self):
        from boa3.model.type.collection.sequence.uint160type import UInt160Type
        from boa3.model.type.type import Type
        identifier = 'call_contract'
        syscall = 'System.Contract.Call'
        args: Dict[str, Variable] = {
            'script_hash': Variable(UInt160Type.build()),
            'method': Variable(Type.str),
            'args': Variable(Type.sequence)  # TODO: change when *args is implemented
        }
        args_default = ast.parse("{0}".format(Type.sequence.default_value)
                                 ).body[0].value
        super().__init__(identifier, syscall, args, defaults=[args_default], return_type=Type.any)

    @property
    def opcode(self) -> List[Tuple[Opcode, bytes]]:
        from boa3.neo.vm.type.Integer import Integer
        from boa3.neo3.contracts import CallFlags
        call_flags = Integer(CallFlags.ALL).to_byte_array(signed=True, min_length=1)

        return [
            (Opcode.PUSHDATA1, Integer(len(call_flags)).to_byte_array() + call_flags),
            (Opcode.ROT, b''),
            (Opcode.ROT, b'')
        ] + super().opcode
