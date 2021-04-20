import ast
from typing import Dict, List, Optional, Tuple

from boa3.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.model.variable import Variable
from boa3.neo.vm.opcode.Opcode import Opcode


class SumMethod(IBuiltinMethod):

    def __init__(self):
        from boa3.model.type.type import Type
        identifier = 'sum'
        args: Dict[str, Variable] = {'__iterable': Variable(Type.sequence.build_collection(Type.int)),
                                     '__start': Variable(Type.int)}

        start_default = ast.parse("{0}".format(Type.int.default_value)
                                  ).body[0].value
        super().__init__(identifier, args, defaults=[start_default], return_type=Type.int)

    @property
    def opcode(self) -> List[Tuple[Opcode, bytes]]:
        from boa3.neo.vm.type.Integer import Integer
        return [
            (Opcode.PUSH0, b''),    # index = 0
            (Opcode.DUP, b''),
            (Opcode.PUSH2, b''),    # len(iterable)
            (Opcode.PICK, b''),
            (Opcode.SIZE, b''),
            (Opcode.GE, b''),       # index > len(iterable)
            (Opcode.JMPIF, Integer(12).to_byte_array(signed=True, min_length=1)),
            (Opcode.REVERSE3, b''),
            (Opcode.OVER, b''),
            (Opcode.PUSH3, b''),    # x = iterable[index]
            (Opcode.PICK, b''),
            (Opcode.PICKITEM, b''),
            (Opcode.ADD, b''),      # result += x
            (Opcode.REVERSE3, b''),
            (Opcode.INC, b''),      # index += 1
            (Opcode.JMP, Integer(-15).to_byte_array(signed=True, min_length=1)),
            (Opcode.DROP, b''),
            (Opcode.DROP, b''),
        ]

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> Optional[str]:
        return None
