import ast
from typing import Dict, List, Tuple

from boa3.model.builtin.method.listmethod import ListMethod
from boa3.model.type.itype import IType
from boa3.model.variable import Variable
from boa3.neo.vm.opcode.Opcode import Opcode


class ListSequenceMethod(ListMethod):

    def __init__(self, sequence_type: IType = None):
        from boa3.model.type.type import Type
        if sequence_type is None:
            sequence_type = Type.sequence

        args: Dict[str, Variable] = {
            'value': Variable(sequence_type),
        }

        value_default = ast.parse("{0}".format(Type.sequence.default_value)
                                  ).body[0].value

        return_type = Type.list.build_collection(sequence_type.value_type)

        super().__init__(args, return_type, [value_default])

    @property
    def prepare_for_packing(self) -> List[Tuple[Opcode, bytes]]:

        if self._prepare_for_packing is None:

            self._prepare_for_packing = [(Opcode.UNPACK, b'')]

        return super().prepare_for_packing
