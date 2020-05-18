from typing import Optional

from boa3.model.operation.binary.arithmetic.addition import Addition
from boa3.model.operation.binary.arithmetic.concat import Concat
from boa3.model.operation.binary.arithmetic.division import Division
from boa3.model.operation.binary.arithmetic.floordivision import FloorDivision
from boa3.model.operation.binary.arithmetic.modulo import Modulo
from boa3.model.operation.binary.arithmetic.multiplication import Multiplication
from boa3.model.operation.binary.arithmetic.power import Power
from boa3.model.operation.binary.arithmetic.subtraction import Subtraction
from boa3.model.operation.binary.binaryoperation import BinaryOperation
from boa3.model.operation.binary.logical.booleanand import BooleanAnd
from boa3.model.operation.binary.logical.booleanor import BooleanOr
from boa3.model.operation.binary.relational.LessThan import LessThan
from boa3.model.operation.binary.relational.Lessthanorequal import LessThanOrEqual
from boa3.model.operation.binary.relational.greaterthan import GreaterThan
from boa3.model.operation.binary.relational.greaterthanorequal import GreaterThanOrEqual
from boa3.model.operation.binary.relational.identity import Identity
from boa3.model.operation.binary.relational.notidentity import NotIdentity
from boa3.model.operation.binary.relational.numericequality import NumericEquality
from boa3.model.operation.binary.relational.numericinequality import NumericInequality
from boa3.model.operation.binary.relational.objectequality import ObjectEquality
from boa3.model.operation.operator import Operator
from boa3.model.type.type import IType


class BinaryOp:
    # Arithmetic operations
    Add = Addition()
    Sub = Subtraction()
    Mul = Multiplication()
    Div = Division()
    IntDiv = FloorDivision()
    Mod = Modulo()
    Pow = Power()
    Concat = Concat()

    # Relational operations
    NumEq = NumericEquality()
    NumNotEq = NumericInequality()
    Lt = LessThan()
    LtE = LessThanOrEqual()
    Gt = GreaterThan()
    GtE = GreaterThanOrEqual()
    Is = Identity()
    IsNot = NotIdentity()
    Eq = ObjectEquality()

    # Logical operations
    And = BooleanAnd()
    Or = BooleanOr()

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
        for id, op in vars(cls).items():
            if isinstance(op, BinaryOperation) and op.is_valid(operator, left, right):
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
        for id, op in vars(cls).items():
            if isinstance(op, BinaryOperation) and op.operator is operator:
                return op

    @classmethod
    def get_operation(cls, operation: BinaryOperation) -> Optional[BinaryOperation]:
        """
        Gets a binary operation given another operation.

        :param operation: binary operation
        :return: The operation if exists. None otherwise;
        :rtype: BinaryOperation or None
        """
        for id, op in vars(cls).items():
            if type(operation) == type(op):
                return op
