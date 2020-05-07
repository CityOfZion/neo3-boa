from typing import List

from boa3.model.operation.operator import Operator
from boa3.model.operation.unary.unaryoperation import UnaryOperation
from boa3.model.type.type import IType, Type


class Positive(UnaryOperation):
    _valid_types: List[IType] = [Type.int]

    def __init__(self, operand: IType = Type.int):
        self.operator: Operator = Operator.Plus
        super().__init__(operand)

    def validate_type(self, *types: IType) -> bool:
        if len(types) != self._get_number_of_operands:
            return False
        operand: IType = types[0]

        return operand in self._valid_types

    def _get_result(self, operand: IType) -> IType:
        if self.validate_type(operand):
            return operand
        else:
            return Type.none
