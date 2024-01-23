import ast
from typing import Any

from boa3.internal.model.builtin.method import IBuiltinMethod
from boa3.internal.model.operation.binaryop import BinaryOp
from boa3.internal.model.type.itype import IType
from boa3.internal.model.variable import Variable


class SortMethod(IBuiltinMethod):

    def __init__(self, arg_value: IType | None = None):
        from boa3.internal.model.type.type import Type

        if not Type.list.is_type_of(arg_value):
            arg_value = Type.list

        identifier = 'sort'
        args: dict[str, Variable] = {
            'self': Variable(arg_value),
            'reverse': Variable(Type.bool)
        }
        # TODO: change this when keyword-only arguments are implemented #2ewewtz
        kwargs = {
            'reverse': Variable(Type.bool)
        }
        reverse_default = ast.parse(str(Type.bool.default_value)).body[0].value

        super().__init__(identifier, args, kwargs=kwargs, defaults=[reverse_default])

    @property
    def identifier(self) -> str:
        from boa3.internal.model.type.type import Type

        if self._arg_self.type is Type.list:
            return self._identifier

        if Type.list.is_type_of(self._arg_self.type):
            return '-{0}_{1}'.format(self._identifier, self._arg_self.type.identifier)

        return self._identifier

    @property
    def is_supported(self) -> bool:
        from boa3.internal.model.type.primitive.primitivetype import PrimitiveType
        item_type: IType = self._arg_self.type.item_type
        if isinstance(item_type, PrimitiveType):
            return True

        from boa3.internal.model.type.annotation.uniontype import UnionType
        if (isinstance(item_type, UnionType) and
                all(isinstance(union_type, PrimitiveType) for union_type in item_type.union_types)):
            return True

        return False

    @property
    def _arg_self(self) -> Variable:
        return self.args['self']

    def generate_internal_opcodes(self, code_generator):
        from boa3.internal.model.builtin.builtin import Builtin
        from boa3.internal.neo.vm.opcode.Opcode import Opcode

        # code_generator.remove_stack_top_item()  # ignore key arg
        # reverse, self // reverse -> top

        # start_index = 0
        # i = 1
        # end_address = len(self)
        code_generator.duplicate_stack_item(2)
        code_generator.convert_builtin_method_call(Builtin.Len, is_internal=True)
        code_generator.convert_literal(1)

        # while i <= end_address
        begin_i_while_address = code_generator.convert_begin_while()

        code_generator.duplicate_stack_item(4)  # push array to the stack top
        #   j = i
        code_generator.duplicate_stack_item(2)

        j_while_start_address = code_generator.convert_begin_while()
        #   while j > start_index and arr[j] < arr[j - 1]:
        #       arr[j], arr[j - 1] = arr[j - 1], arr[j]
        code_generator.duplicate_stack_top_item()
        code_generator.insert_opcode(Opcode.DEC)    # (j - 1), j, arr

        arr_j_minus_one_address = code_generator.bytecode_size
        code_generator.duplicate_stack_item(3)
        code_generator.duplicate_stack_item(2)
        code_generator.convert_get_item(index_inserted_internally=True)  # aux = arr[j - 1]

        # arr[j - 1] / j - 1 / j
        code_generator.swap_reverse_stack_items(3, rotate=True)  # j / arr[j - 1] / j - 1
        arr_j_address = code_generator.bytecode_size
        code_generator.duplicate_stack_item(4)
        code_generator.duplicate_stack_item(2)
        code_generator.convert_get_item(index_inserted_internally=True)  # arr[j]

        # arr[j] / j / arr[j - 1] / j - 1 / arr
        code_generator.duplicate_stack_item(4)
        code_generator.duplicate_stack_item(6)
        code_generator.swap_reverse_stack_items(3)
        code_generator.convert_set_item(arr_j_address, index_inserted_internally=True)  # arr[j - 1] = arr[j]

        # j / arr[j - 1] / j - 1 / arr
        code_generator.duplicate_stack_item(4)
        code_generator.swap_reverse_stack_items(3)
        code_generator.convert_set_item(arr_j_minus_one_address, index_inserted_internally=True)  # arr[j] = arr[j - 1]

        j_while_test_address = code_generator.bytecode_size
        # j > start_index
        code_generator.duplicate_stack_top_item()
        code_generator.convert_literal(0)
        code_generator.convert_operation(BinaryOp.Gt, is_internal=True)

        code_generator.duplicate_stack_top_item()
        if_j_positive = code_generator.convert_begin_if()

        # arr[j] (> if reverse else <) arr[j - 1]
        code_generator.duplicate_stack_item(3)
        code_generator.duplicate_stack_item(3)
        code_generator.convert_get_item(index_inserted_internally=True)
        code_generator.duplicate_stack_item(4)
        code_generator.duplicate_stack_item(4)
        code_generator.insert_opcode(Opcode.DEC)
        code_generator.convert_get_item(index_inserted_internally=True)

        # "gt" if reverse else "lt"
        code_generator.duplicate_stack_item(8)
        if_is_reverse = code_generator.convert_begin_if()
        code_generator.convert_operation(BinaryOp.Gt, is_internal=True)

        else_is_reverse = code_generator.convert_begin_else(if_is_reverse, is_internal=True)
        code_generator.convert_operation(BinaryOp.Lt, is_internal=True)

        code_generator.convert_end_if(else_is_reverse, is_internal=True)

        code_generator.convert_operation(BinaryOp.And, is_internal=True)

        code_generator.convert_end_if(if_j_positive, is_internal=True)

        code_generator.convert_end_while(j_while_start_address, j_while_test_address, is_internal=True)

        code_generator.remove_stack_top_item()  # remove j from the stack
        code_generator.remove_stack_top_item()  # remove array from the stack

        #   i += 1
        code_generator.insert_opcode(Opcode.INC)

        condition_i_while_address = code_generator.bytecode_size
        code_generator.duplicate_stack_top_item()
        code_generator.duplicate_stack_item(3)
        code_generator.convert_operation(BinaryOp.Lt, is_internal=True)
        code_generator.convert_end_while(begin_i_while_address, condition_i_while_address, is_internal=True)

        # clean stack
        code_generator.remove_stack_top_item()
        code_generator.remove_stack_top_item()
        code_generator.remove_stack_top_item()
        code_generator.remove_stack_top_item()

    def push_self_first(self) -> bool:
        return self.has_self_argument

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> str | None:
        return None

    def build(self, value: Any) -> IBuiltinMethod:
        if not isinstance(value, list):
            value = [value]

        from boa3.internal.model.type.type import Type
        if len(value) > 0 and Type.list.is_type_of(value[0]):
            return SortMethod(value[0])

        return self
