from typing import List

from boa3.model.operation.binary.binaryoperation import BinaryOperation
from boa3.model.operation.operator import Operator
from boa3.model.type.type import IType, Type


class Concat(BinaryOperation):
    _valid_types: List[IType] = [Type.str]

    def __init__(self, left: IType = Type.str, right: IType = Type.str):
        self.operator: Operator = Operator.Plus
        super().__init__(left, right)

    def validate_type(self, *types: IType) -> bool:
        if len(types) != self._get_number_of_operands:
            return False
        left: IType = types[0]
        right: IType = types[1]

        return left == right and left in self._valid_types

    def _get_result(self, left: IType, right: IType) -> IType:
        if self.validate_type(left, right):
            return left
        else:
            return Type.none

