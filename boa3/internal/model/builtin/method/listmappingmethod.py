from boa3.internal.model.builtin.method.listmethod import ListMethod
from boa3.internal.model.type.itype import IType
from boa3.internal.model.variable import Variable
from boa3.internal.neo.vm.opcode.Opcode import Opcode


class ListMappingMethod(ListMethod):

    def __init__(self, mapping_type: IType = None):
        from boa3.internal.model.type.type import Type
        if mapping_type is None:
            mapping_type = Type.mapping

        args: dict[str, Variable] = {
            'value': Variable(mapping_type),
        }

        return_type = Type.list.build_collection(mapping_type.key_type)

        super().__init__(args, return_type)

    def generate_pack_opcodes(self, code_generator):
        from boa3.internal.model.builtin.builtin import Builtin

        code_generator.convert_builtin_method_call(Builtin.DictKeys, is_internal=True)
        code_generator.insert_opcode(Opcode.UNPACK)
