from boa3.internal.model.operation.binary.binaryoperation import BinaryOperation
from boa3.internal.model.operation.operator import Operator
from boa3.internal.model.type.type import IType, Type
from boa3.internal.neo.vm.opcode.Opcode import Opcode


class ListAddition(BinaryOperation):
    """
    A class used to represent a list addition operation

    :ivar operator: the operator of the operation. Inherited from :class:`IOperation`
    :ivar left: the left operand type. Inherited from :class:`BinaryOperation`
    :ivar right: the left operand type. Inherited from :class:`BinaryOperation`
    :ivar result: the result type of the operation.  Inherited from :class:`IOperation`
    """
    _valid_types: list[IType] = [Type.list]

    def __init__(self, left: IType = Type.list, right: IType = None):
        self.operator: Operator = Operator.Plus
        super().__init__(left, right)

    def validate_type(self, *types: IType) -> bool:
        if len(types) != self.number_of_operands:
            return False
        left: IType = types[0]
        right: IType = types[1]

        return left == right and any(_type.is_type_of(left) for _type in self._valid_types)

    def _get_result(self, left: IType, right: IType) -> IType:
        if self.validate_type(left, right):
            return left
        else:
            return Type.none

    def generate_internal_opcodes(self, code_generator):
        from boa3.internal.model.builtin.builtin import Builtin
        from boa3.internal.model.operation.binaryop import BinaryOp
        from boa3.internal.neo.vm.type.StackItem import StackItemType

        # if isinstance(first, list):
        code_generator.duplicate_stack_item(2)
        code_generator.insert_type_check(StackItemType.Array)
        if_is_list = code_generator.convert_begin_if()

        #   aux = first
        code_generator.swap_reverse_stack_items(2)
        code_generator.convert_copy()
        code_generator.swap_reverse_stack_items(2)

        #   while there's values to add
        #   aux_index = len(second)
        values_type = self.right_type.value_type if hasattr(self.right_type, 'value_type') else Type.any
        code_generator.insert_opcode(Opcode.UNPACK, add_to_stack=[values_type, Type.int])

        #   while aux_index > 0:
        begin_while = code_generator.convert_begin_while()

        get_array_address = code_generator.bytecode_size
        code_generator.duplicate_stack_top_item()
        code_generator.insert_opcode(Opcode.INC)    # push the array to the top of the stack
        code_generator.duplicate_stack_item(expected_stack_item=self.right_type)

        get_value_address = code_generator.bytecode_size
        code_generator.move_stack_item_to_top(3)

        #       aux.append(second[-aux_index])
        code_generator.convert_builtin_method_call(Builtin.SequenceAppend,
                                                   [get_array_address, get_value_address],
                                                   is_internal=True)
        #       aux_index -= 1
        code_generator.insert_opcode(Opcode.DEC)

        #   while condition
        condition_start = code_generator.bytecode_size
        code_generator.duplicate_stack_top_item()
        code_generator.convert_end_while(begin_while, condition_start, is_internal=True)

        #    clear stack
        code_generator.remove_stack_top_item()

        # else:
        else_is_list = code_generator.convert_begin_else(if_is_list, is_internal=True)
        #   simple concat
        code_generator.convert_operation(BinaryOp.Concat, is_internal=True)
        code_generator.convert_end_if(else_is_list, is_internal=True)
