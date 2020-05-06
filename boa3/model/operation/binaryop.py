from enum import Enum

from boa3.model.operation.operation import IOperation
from boa3.model.operation.operator import Operator
from boa3.model.type.type import IType, Type


class __BinaryOperation(IOperation):
    def __init__(self, operator: Operator, right_op_type: IType, left_op_type: IType, result_type: IType, *args, **kwargs):
        super().__init__(operator, result_type, *args, **kwargs)
        self.right_op_type = right_op_type
        self.left_op_type = left_op_type
        self._fields += (
            'right_op_type',
            'left_op_type'
        )


class BinaryOp(__BinaryOperation, Enum):
    Add = (Operator.Plus, Type.int, Type.int, Type.int)
    Sub = (Operator.Minus, Type.int, Type.int, Type.int)
    Mul = (Operator.Mult, Type.int, Type.int, Type.int)
    IntDiv = (Operator.IntDiv, Type.int, Type.int, Type.int)
    Div = (Operator.Div, Type.int, Type.int, Type.int)
    Mod = (Operator.Mod, Type.int, Type.int, Type.int)
    Pow = (Operator.Pow, Type.int, Type.int, Type.int)
    Concat = (Operator.Plus, Type.str, Type.str, Type.str)
