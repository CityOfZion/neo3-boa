from boa3.internal.model.operation.binary.binaryoperation import BinaryOperation
from boa3.internal.model.operation.operator import Operator
from boa3.internal.model.type.type import IType, Type


class UnionTypesOperation(BinaryOperation):
    """
    A class used to represent the union of 2 types with the | operator

    :ivar operator: the operator of the operation. Inherited from :class:`IOperation`
    :ivar left: the left operand type. Inherited from :class:`BinaryOperation`
    :ivar right: the left operand type. Inherited from :class:`BinaryOperation`
    :ivar result: the result type of the operation.  Inherited from :class:`IOperation`
    """

    def __init__(self, left: IType = Type.any, right: IType = None):
        self.operator: Operator = Operator.BitOr
        super().__init__(left, right)

    def validate_type(self, *types: IType) -> bool:
        if len(types) != self.number_of_operands:
            return False

        return True

    def _get_result(self, left: IType, right: IType) -> IType:
        if self.validate_type(left, right):
            return left.union_type(right)
        else:
            return Type.none
