from typing import Optional

from boa3.internal.model.builtin.classmethod.copymethod import CopyMethod
from boa3.internal.model.type.itype import IType
from boa3.internal.neo.vm.opcode.Opcode import Opcode


class CopyDictMethod(CopyMethod):

    def __init__(self, arg_value: Optional[IType] = None):
        from boa3.internal.model.type.type import Type
        super().__init__(arg_value if Type.dict.is_type_of(arg_value) else Type.dict)

    def generate_internal_opcodes(self, code_generator):
        code_generator.insert_opcode(Opcode.UNPACK)
        code_generator.insert_opcode(Opcode.PACKMAP)
