from typing import Dict, Any, Optional

from boa3.internal.model.builtin.method import IBuiltinMethod
from boa3.internal.model.builtin.method.strmethod import StrMethod
from boa3.internal.model.type.classes.userclass import UserClass
from boa3.internal.model.type.itype import IType
from boa3.internal.model.variable import Variable
from boa3.internal.neo.vm.opcode.Opcode import Opcode


class StrClassMethod(StrMethod):

    def __init__(self, arg_value: Optional[IType] = None):
        from boa3.internal.model.type.classes import userclass

        if arg_value is None:
            arg_value = userclass._EMPTY_CLASS

        args: Dict[str, Variable] = {
            'object': Variable(arg_value),
        }

        super().__init__(args)

    @property
    def arg_type(self) -> UserClass:
        return self._arg_value.type

    def build(self, value: Any) -> IBuiltinMethod:
        if isinstance(value, UserClass):
            if 'object' in self.args and value.is_type_of(self.args['object'].type):
                return self

            return StrClassMethod(value)

        return super().build(value)

    def generate_internal_opcodes(self, code_generator):
        from boa3.internal.model.builtin.interop.interop import Interop
        from boa3.internal.model.type.type import Type

        # class to dict, then print as json
        code_generator.insert_opcode(Opcode.UNPACK, add_to_stack=[Type.any, Type.int])
        code_generator.remove_stack_top_item()
        code_generator.convert_new_map(Type.dict)

        # add each value to the dict
        for variable_name in self.arg_type.instance_variables:
            code_generator.insert_opcode(Opcode.TUCK, add_to_stack=[Type.any])
            code_generator.convert_literal(variable_name)
            item_address = code_generator.bytecode_size
            code_generator.swap_reverse_stack_items(3, rotate=True)
            code_generator.convert_set_item(item_address, index_inserted_internally=True)

        # print as json
        code_generator.convert_builtin_method_call(Interop.JsonSerialize, is_internal=True)
