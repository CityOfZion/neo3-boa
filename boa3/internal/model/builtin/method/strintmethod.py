from typing import Dict, List, Tuple

from boa3.internal.model.builtin.interop.stdlib import ItoaMethod
from boa3.internal.model.builtin.method.strmethod import StrMethod
from boa3.internal.model.variable import Variable
from boa3.internal.neo.vm.opcode.Opcode import Opcode


class StrIntMethod(StrMethod):

    def __init__(self):
        from boa3.internal.model.type.type import Type
        args: Dict[str, Variable] = {
            'object': Variable(Type.int),
        }

        super().__init__(args)

    @property
    def _opcode(self) -> List[Tuple[Opcode, bytes]]:
        return ItoaMethod(internal_call_args=1).opcode
