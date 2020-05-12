from typing import Optional, Dict

from boa3.model.operation.binary.addition import Addition
from boa3.model.operation.binary.binaryoperation import BinaryOperation
from boa3.model.operation.binary.concat import Concat
from boa3.model.operation.binary.division import Division
from boa3.model.operation.binary.floordivision import FloorDivision
from boa3.model.operation.binary.modulo import Modulo
from boa3.model.operation.binary.multiplication import Multiplication
from boa3.model.operation.binary.power import Power
from boa3.model.operation.binary.subtraction import Subtraction
from boa3.model.operation.operator import Operator
from boa3.model.type.type import IType


class BinaryOp:
    __operations: Dict[str, BinaryOperation] = {
        # Arithmetic operations
        'Add': Addition(),
        'Sub': Subtraction(),
        'Mul': Multiplication(),
        'Div': Division(),
        'IntDiv': FloorDivision(),
        'Mod': Modulo(),
        'Pow': Power(),
        'Concat': Concat()
    }

    # Arithmetic operations
    Add = __operations['Add']
    Sub = __operations['Sub']
    Mul = __operations['Mul']
    Div = __operations['Div']
    IntDiv = __operations['IntDiv']
    Mod = __operations['Mod']
    Pow = __operations['Pow']
    Concat = __operations['Concat']

    @classmethod
    def validate_type(cls, operator: Operator, left: IType, right: IType) -> Optional[BinaryOperation]:
        """
        Gets a binary operation given the operator and the operands types.

        :param operator: binary operator
        :param left: type of the left operand
        :param right: type of the right operand
        :return: The operation if exists. None otherwise;
        :rtype: BinaryOperation or None
        """
        for id, op in cls.__operations.items():
            if op.is_valid(operator, left, right):
                return op.build(left, right)

    @classmethod
    def get_operation_by_operator(cls, operator: Operator) -> Optional[BinaryOperation]:
        """
        Gets a binary operation given the operator.

        :param operator: binary operator
        :return: The operation if exists. If exists more than one operation with the same operator, returns the first
        found. None otherwise;
        :rtype: BinaryOperation or None
        """
        for id, op in cls.__operations.items():
            if op.operator is operator:
                return op

    @classmethod
    def get_operation(cls, operation: BinaryOperation) -> Optional[BinaryOperation]:
        """
        Gets a binary operation given another operation.

        :param operation: binary operation
        :return: The operation if exists. None otherwise;
        :rtype: BinaryOperation or None
        """
        for id, op in cls.__operations.items():
            if type(operation) == type(op):
                return op
