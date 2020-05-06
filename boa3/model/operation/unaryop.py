from enum import Enum

from boa3.model.operation.operation import IOperation
from boa3.model.operation.operator import Operator
from boa3.model.type.type import Type, IType


class __UnaryOperation(IOperation):
    def __init__(self, operator: Operator, op_type: IType, result_type: IType, *args, **kwargs):
        super().__init__(operator, result_type, *args, **kwargs)
        self.op_type = op_type
        self._fields += (
            'op_type',
        )


class UnaryOp(__UnaryOperation, Enum):
    Positive = (Operator.Plus, Type.int, Type.int)
    Negative = (Operator.Minus, Type.int, Type.int)
