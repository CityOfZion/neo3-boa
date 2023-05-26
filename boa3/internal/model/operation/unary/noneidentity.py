from boa3.internal.model.operation.operator import Operator
from boa3.internal.model.operation.unary.unaryoperation import UnaryOperation
from boa3.internal.model.type.type import IType, Type
from boa3.internal.neo.vm.opcode.Opcode import Opcode


class NoneIdentity(UnaryOperation):
    """
    A class used to represent an 'is None' comparison

    :ivar operator: the operator of the operation. Inherited from :class:`IOperation`
    :ivar operand: the operand type. Inherited from :class:`UnaryOperation`
    :ivar result: the result type of the operation.  Inherited from :class:`IOperation`
    """

    def __init__(self, operand: IType = Type.int):
        self.operator: Operator = Operator.Is
        super().__init__(operand)

    @property
    def number_of_operands(self) -> int:
        # it is a Python binary operation that is equivalent to a Neo VM unary operation
        return 2

    @property
    def op_on_stack(self) -> int:
        return super().number_of_operands

    def validate_type(self, *types: IType) -> bool:
        if len(types) == self.op_on_stack:
            return True
        if len(types) != self.number_of_operands:
            return False
        left: IType = types[0]
        right: IType = types[1]

        return left is Type.none or right is Type.none

    def _get_result(self, operand: IType) -> IType:
        if self.validate_type(operand):
            return Type.bool
        else:
            return Type.none

    def generate_internal_opcodes(self, code_generator):
        code_generator.insert_opcode(Opcode.ISNULL)
