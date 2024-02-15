from boa3.internal.model.builtin.interop.interop import Interop
from boa3.internal.model.operation.binary.binaryoperation import BinaryOperation
from boa3.internal.model.operation.operator import Operator
from boa3.internal.model.type.type import IType, Type


class StrBytesLessThan(BinaryOperation):
    """
    A class used to represent a string/bytes less than comparison

    :ivar operator: the operator of the operation. Inherited from :class:`IOperation`
    :ivar left: the left operand type. Inherited from :class:`BinaryOperation`
    :ivar right: the left operand type. Inherited from :class:`BinaryOperation`
    :ivar result: the result type of the operation.  Inherited from :class:`IOperation`
    """
    _valid_types: list[IType] = [Type.bytes, Type.str]

    def __init__(self, left: IType = Type.str, right: IType = None):
        self.operator: Operator = Operator.Lt
        super().__init__(left, right)

    def validate_type(self, *types: IType) -> bool:
        if len(types) != self.number_of_operands:
            return False
        left: IType = types[0]
        right: IType = types[1]

        return left == right and any(_type.is_type_of(left) for _type in self._valid_types)

    def _get_result(self, left: IType, right: IType) -> IType:
        if self.validate_type(left, right):
            return Type.bool
        else:
            return Type.none

    def generate_internal_opcodes(self, code_generator):
        from boa3.internal.model.operation.binaryop import BinaryOp

        # comparing strings, on the stack the first string is the right one and the second is the left one
        Interop.MemoryCompare.generate_internal_opcodes(code_generator)
        # -1 means the left string is greater than the right string
        # 1 means the left string is less than the right string
        # 0 means the right string is equals to the left string

        # if comparison equals 1 (the left string is less than the right string), then return True
        code_generator.convert_literal(1)
        code_generator.convert_operation(BinaryOp.NumEq)
        # else, return False
