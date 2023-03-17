import ast
from typing import Dict, List, Tuple

from boa3.internal.model.builtin.method.intmethod import IntMethod
from boa3.internal.model.variable import Variable
from boa3.internal.neo.vm.opcode.Opcode import Opcode


class IntIntMethod(IntMethod):

    def __init__(self):
        from boa3.internal.model.type.type import Type
        args: Dict[str, Variable] = {
            'value': Variable(Type.int),
        }

        value_default = ast.parse("{0}".format(Type.int.default_value)
                                  ).body[0].value

        super().__init__(args, [value_default])

    @property
    def _opcode(self) -> List[Tuple[Opcode, bytes]]:
        # returns the same int
        return []
