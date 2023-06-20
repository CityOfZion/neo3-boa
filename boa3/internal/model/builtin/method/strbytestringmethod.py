import ast
from typing import Dict, List, Tuple

from boa3.internal.model.builtin.method.strmethod import StrMethod
from boa3.internal.model.variable import Variable
from boa3.internal.neo.vm.opcode.Opcode import Opcode


class StrBytesMethod(StrMethod):

    def __init__(self):
        from boa3.internal.model.type.type import Type

        args: Dict[str, Variable] = {
            'object': Variable(Type.union.build([Type.bytes, Type.str])),
        }
        object_default = ast.parse("'{0}'".format(Type.str.default_value)).body[0].value

        super().__init__(args, [object_default])

    @property
    def _opcode(self) -> List[Tuple[Opcode, bytes]]:
        return []
