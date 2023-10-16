from boa3.internal.model.builtin.method.printmethod import PrintMethod
from boa3.internal.model.type.classes.userclass import UserClass
from boa3.internal.model.type.itype import IType
from boa3.internal.neo.vm.opcode.Opcode import Opcode


class PrintClassMethod(PrintMethod):

    def __init__(self, arg_value: IType):
        if not isinstance(arg_value, UserClass):
            from boa3.internal.model.type.classes import userclass
            arg_value = userclass._EMPTY_CLASS

        super().__init__(arg_value)
        self._arg_type = arg_value

    def _generate_print_opcodes(self, code_generator):
        from boa3.internal.model.builtin.interop.interop import Interop
        from boa3.internal.model.type.type import Type

        # class to dict, then print as json
        code_generator.insert_opcode(Opcode.UNPACK, add_to_stack=[Type.any, Type.int])
        code_generator.remove_stack_top_item()
        code_generator.convert_new_map(Type.dict)

        # add each value to the dict
        for variable_name in self._arg_type.instance_variables:
            code_generator.insert_opcode(Opcode.TUCK, add_to_stack=[Type.any])
            code_generator.convert_literal(variable_name)
            item_address = code_generator.bytecode_size
            code_generator.swap_reverse_stack_items(3, rotate=True)
            code_generator.convert_set_item(item_address, index_inserted_internally=True)

        # print as json
        code_generator.convert_builtin_method_call(Interop.JsonSerialize, is_internal=True)
