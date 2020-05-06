import ast

from boa3.model.operation.operator import Operator
from boa3.model.type.type import IType


class IOperation(ast.operator):
    """
    An interface user to represent operations
    """
    def __init__(self, operator: Operator, result_type: IType, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._fields = (
            'operator',
            'result_type'
        )
        self.operator = operator
        self.result_type = result_type
