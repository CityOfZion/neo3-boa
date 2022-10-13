from typing import Dict, List, Tuple

from boa3.model.builtin.interop.stdlib import ItoaMethod
from boa3.model.builtin.method.strmethod import StrMethod
from boa3.model.variable import Variable
from boa3.neo.vm.opcode.Opcode import Opcode


class StrIntMethod(StrMethod):

    def __init__(self):
        from boa3.model.type.type import Type
        args: Dict[str, Variable] = {
            'object': Variable(Type.int),
        }

        super().__init__(args)

    @property
    def _opcode(self) -> List[Tuple[Opcode, bytes]]:
        return (
            [
                (Opcode.PUSH10, b''),
                (Opcode.SWAP, b''),
                (Opcode.PUSH2, b''),
                (Opcode.PACK, b''),
            ] +
            ItoaMethod().opcode
        )
