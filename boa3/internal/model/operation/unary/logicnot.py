from typing import List

from boa3.internal.model.operation.operator import Operator
from boa3.internal.model.operation.unary.unaryoperation import UnaryOperation
from boa3.internal.model.type.type import IType, Type
from boa3.internal.neo.vm.opcode.Opcode import Opcode


class LogicNot(UnaryOperation):
    """
    A class used to represent the bit not [ ~ ] operation

    :ivar operator: the operator of the operation. Inherited from :class:`IOperation`
    :ivar operand: the operand type. Inherited from :class:`UnaryOperation`
    :ivar result: the result type of the operation.  Inherited from :class:`IOperation`
    """
    _valid_types: List[IType] = [Type.int, Type.bool]

    def __init__(self, operand: IType = Type.int):
        self.operator: Operator = Operator.BitNot
        super().__init__(operand)

    def validate_type(self, *types: IType) -> bool:
        if len(types) != self.number_of_operands:
            return False
        operand: IType = types[0]

        return any(_type.is_type_of(operand) for _type in self._valid_types)

    def _get_result(self, operand: IType) -> IType:
        if self.validate_type(operand):
            return Type.int
        else:
            return Type.none

    def generate_internal_opcodes(self, code_generator):
        code_generator.insert_opcode(Opcode.INVERT)
