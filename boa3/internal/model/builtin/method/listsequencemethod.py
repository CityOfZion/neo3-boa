import ast

from boa3.internal.model.builtin.method.listmethod import ListMethod
from boa3.internal.model.type.itype import IType
from boa3.internal.model.variable import Variable
from boa3.internal.neo.vm.opcode.Opcode import Opcode


class ListSequenceMethod(ListMethod):

    def __init__(self, sequence_type: IType = None):
        from boa3.internal.model.type.type import Type
        if sequence_type is None:
            sequence_type = Type.sequence

        args: dict[str, Variable] = {
            'value': Variable(sequence_type),
        }

        value_default = ast.parse("{0}".format(Type.sequence.default_value)
                                  ).body[0].value

        return_type = Type.list.build_collection(sequence_type.value_type)

        super().__init__(args, return_type, [value_default])

    def generate_pack_opcodes(self, code_generator):
        code_generator.insert_opcode(Opcode.UNPACK)
