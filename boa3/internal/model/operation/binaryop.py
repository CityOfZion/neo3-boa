from boa3.internal.model.operation.binary.additional import *
from boa3.internal.model.operation.binary.arithmetic import *
from boa3.internal.model.operation.binary.binaryoperation import BinaryOperation
from boa3.internal.model.operation.binary.logical import *
from boa3.internal.model.operation.binary.relational import *
from boa3.internal.model.operation.operation import IOperation
from boa3.internal.model.operation.operator import Operator
from boa3.internal.model.operation.unary.noneidentity import NoneIdentity
from boa3.internal.model.operation.unary.nonenotidentity import NoneNotIdentity
from boa3.internal.model.type.itype import IType


class BinaryOp:
    # Arithmetic operations
    Add = Addition()
    Sub = Subtraction()
    Mul = Multiplication()
    Div = Division()
    IntDiv = FloorDivision()
    ListAdd = ListAddition()
    Mod = Modulo()
    Pow = Power()
    Concat = Concat()
    StrBytesMul = StrBytesMultiplication()

    # Relational operations
    NumEq = NumericEquality()
    NumNotEq = NumericInequality()
    Lt = LessThan()
    LtE = LessThanOrEqual()
    Gt = GreaterThan()
    GtE = GreaterThanOrEqual()
    IsNone = NoneIdentity()
    IsNotNone = NoneNotIdentity()
    Is = Identity()
    IsNot = NotIdentity()
    Eq = ObjectEquality()
    NotEq = ObjectInequality()
    StrBytesGt = StrBytesGreaterThan()
    StrBytesGtE = StrBytesGreaterThanOrEqual()
    StrBytesLt = StrBytesLessThan()
    StrBytesLtE = StrBytesLessThanOrEqual()

    # Logical operations
    And = BooleanAnd()
    Or = BooleanOr()
    ElvisOperatorOr = ElvisOperatorOr()
    BitAnd = LogicAnd()
    BitOr = LogicOr()
    Xor = LogicXor()
    LShift = LeftShift()
    RShift = RightShift()

    # Other operations
    In = CollectionMembership()
    NotIn = CollectionNotMembership()

    @classmethod
    def validate_type(cls, operator: Operator, left: IType, right: IType) -> BinaryOperation | None:
        """
        Gets a binary operation given the operator and the operands types.

        :param operator: binary operator
        :param left: type of the left operand
        :param right: type of the right operand
        :return: The operation if exists. None otherwise;
        :rtype: BinaryOperation or None
        """
        for id, op in vars(cls).items():
            if isinstance(op, IOperation) and op.is_valid(operator, left, right):
                if isinstance(op, BinaryOperation):
                    return op.build(left, right)
                else:
                    from boa3.internal.model.type.type import Type
                    operand = right if left is Type.none else left
                    return op.build(operand)

    @classmethod
    def get_operation_by_operator(cls, operator: Operator, left_operand: IType,
                                  right_operand: IType | None = None) -> BinaryOperation | None:
        """
        Gets a binary operation given the operator.

        :param operator: binary operator
        :param left_operand: left operand of the operator
        :param right_operand: right operand of the operator
        :return: The operation if exists. If exists more than one operation with the same operator, returns the one with
        the same left operand. If none has the same left operand, returns the first found. None otherwise;
        :rtype: BinaryOperation or None
        """
        valid_operations: list[BinaryOperation] = []
        for id, op in vars(cls).items():
            if isinstance(op, BinaryOperation) and op.operator is operator:
                left, right = op.get_valid_operand_for_validation(left_operand, right_operand)
                if left is not None:
                    return op.build(left_operand if right_operand is None else left, right)
                else:
                    valid_operations.append(op)

        return valid_operations[0] if len(valid_operations) > 0 else None

    @classmethod
    def get_operation(cls, operation: BinaryOperation) -> BinaryOperation | None:
        """
        Gets a binary operation given another operation.

        :param operation: binary operation
        :return: The operation if exists. None otherwise;
        :rtype: BinaryOperation or None
        """
        for id, op in vars(cls).items():
            if type(operation) == type(op):
                return op
