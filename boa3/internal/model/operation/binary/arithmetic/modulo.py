from typing import List

from boa3.internal.model.operation.binary.binaryoperation import BinaryOperation
from boa3.internal.model.operation.operator import Operator
from boa3.internal.model.type.type import IType, Type
from boa3.internal.neo.vm.opcode.Opcode import Opcode


class Modulo(BinaryOperation):
    """
    A class used to represent a numeric modulo operation

    :ivar operator: the operator of the operation. Inherited from :class:`IOperation`
    :ivar left: the left operand type. Inherited from :class:`BinaryOperation`
    :ivar right: the left operand type. Inherited from :class:`BinaryOperation`
    :ivar result: the result type of the operation.  Inherited from :class:`IOperation`
    """
    _valid_types: List[IType] = [Type.int]

    def __init__(self, left: IType = Type.int, right: IType = None):
        self.operator: Operator = Operator.Mod
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

    def generate_opcodes(self, code_generator):
        from boa3.internal.model.operation.binaryop import BinaryOp

        # neo's mod has a different result from python's mod in some cases
        code_generator.swap_reverse_stack_items(2)
        code_generator.duplicate_stack_item(2)

        # result = first % second
        super().generate_opcodes(code_generator)

        # if the result is not zero and the sign is different from the second operator the result is different
        code_generator.duplicate_stack_top_item()
        code_generator.insert_opcode(Opcode.SIGN)   # sign of result
        code_generator.duplicate_stack_item(3)
        code_generator.insert_opcode(Opcode.SIGN)   # sign of second
        code_generator.duplicate_stack_item(2)
        code_generator.convert_operation(BinaryOp.NumNotEq, is_internal=True)

        code_generator.swap_reverse_stack_items(2)
        code_generator.convert_literal(0)
        code_generator.convert_operation(BinaryOp.NumNotEq, is_internal=True)

        # if sign(result) != sign(second) and result != 0:
        code_generator.convert_operation(BinaryOp.And, is_internal=True)
        if_negative = code_generator.convert_begin_if()
        #   result += second
        code_generator.convert_operation(BinaryOp.Add, is_internal=True)
        # else
        else_negative = code_generator.convert_begin_else(if_negative, is_internal=True)
        #   # just clear stack
        code_generator.remove_stack_item(2)
        code_generator.convert_end_if(else_negative, is_internal=True)

    def generate_internal_opcodes(self, code_generator):
        code_generator.insert_opcode(Opcode.MOD)
