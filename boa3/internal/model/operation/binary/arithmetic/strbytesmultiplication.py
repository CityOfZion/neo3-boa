from boa3.internal.model.operation.binary.binaryoperation import BinaryOperation
from boa3.internal.model.operation.operator import Operator
from boa3.internal.model.type.type import IType, Type
from boa3.internal.neo.vm.opcode.Opcode import Opcode


class StrBytesMultiplication(BinaryOperation):
    """
    A class used to represent a string or bytes concatenation operation

    :ivar operator: the operator of the operation. Inherited from :class:`IOperation`
    :ivar left: the left operand type. Inherited from :class:`BinaryOperation`
    :ivar right: the left operand type. Inherited from :class:`BinaryOperation`
    :ivar result: the result type of the operation.  Inherited from :class:`IOperation`
    """
    _valid_types: list[IType] = [Type.str, Type.bytes]

    def __init__(self, left: IType = Type.str, right: IType = Type.int):
        self.operator: Operator = Operator.Mult
        super().__init__(left, right)

    def validate_type(self, *types: IType) -> bool:
        if len(types) != self.number_of_operands:
            return False
        left: IType = types[0]
        right: IType = types[1]

        return any(_type.is_type_of(left) for _type in self._valid_types) and Type.int.is_type_of(right)

    def _get_result(self, left: IType, right: IType) -> IType:
        if self.validate_type(left, right):
            return left
        else:
            return Type.none

    def generate_internal_opcodes(self, code_generator):
        from boa3.internal.model.operation.binaryop import BinaryOp

        # concatString = ''
        code_generator.convert_literal('')
        # reorganize stack
        code_generator.swap_reverse_stack_items(3, rotate=True)
        code_generator.swap_reverse_stack_items(3, rotate=True)

        # while argInt > 0:
        concat_start = code_generator.convert_begin_while()

        #   concatString += argString
        code_generator.swap_reverse_stack_items(3)
        code_generator.duplicate_stack_item(2)
        code_generator.convert_operation(BinaryOp.Concat, is_internal=True)
        #   argInt -= 1
        code_generator.swap_reverse_stack_items(3)
        code_generator.insert_opcode(Opcode.DEC)

        # while condition
        condition_start = code_generator.bytecode_size
        code_generator.duplicate_stack_top_item()
        code_generator.convert_literal(0)
        code_generator.convert_operation(BinaryOp.Gt, is_internal=True)
        code_generator.convert_end_while(concat_start, condition_start, is_internal=True)

        # clear stack
        code_generator.remove_stack_top_item()
        code_generator.remove_stack_top_item()

        code_generator.convert_cast(self.left_type, is_internal=True)
