from typing import List

from boa3.model.operation.binary.binaryoperation import BinaryOperation
from boa3.model.operation.unary.unaryoperation import UnaryOperation
from boa3.model.type.type import IType, Type


class NumericUnaryOperation(UnaryOperation):
    __valid_operands_type: List[IType] = [Type.int]

    def __init__(self, operand: IType, result: IType):
        super().__init__(operand, result)

    @classmethod
    def is_operand_valid(cls, operand: IType) -> bool:
        return operand in cls.__valid_operands_type

    @classmethod
    def build(cls, operand: IType) -> UnaryOperation:
        result = operand
        return cls(operand, result)

    @classmethod
    def build_sample(cls) -> UnaryOperation:
        default = cls.__valid_operands_type[0]
        return cls.build(default)

