from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from boa3.internal.model.operation.operator import Operator
from boa3.internal.model.symbol import ISymbol
from boa3.internal.model.type.itype import IType


class IOperation(ISymbol, ABC):
    """
    An interface used to represent operations

    :ivar operator: the operator of the operation
    :ivar result: the result type of the operation
    """

    def __init__(self, operator: Operator, result_type: IType):
        self.operator: Operator = operator
        self.result: IType = result_type

    def generate_opcodes(self, code_generator):
        """
        Generate the Neo VM opcodes for the method.

        :type code_generator: boa3.internal.compiler.codegenerator.codegenerator.CodeGenerator
        """
        self.generate_internal_opcodes(code_generator)

    def generate_internal_opcodes(self, code_generator):
        """
        Generate the Neo VM opcodes for the method.

        :type code_generator: boa3.internal.compiler.codegenerator.codegenerator.CodeGenerator
        """
        pass

    @property
    def shadowing_name(self) -> str:
        """
        Gets the type of the evaluated expression

        :return: the resulting type when the expression is evaluated
        """
        return self.operator.value

    @property
    @abstractmethod
    def number_of_operands(self) -> int:
        """
        Gets the number of operands required for this operations

        :return: Number of operands
        """
        pass

    @property
    def op_on_stack(self) -> int:
        """
        Gets the number of arguments that must be on stack before the opcode is called.

        :return: the number of arguments. Same from `number_of_operands` by default.
        """
        return self.number_of_operands

    @abstractmethod
    def validate_type(self, *types: IType) -> bool:
        """
        Verifies if the given operands are valid to the operation

        :param types: types of the operand
        :return: True if all arguments are valid. False otherwise.
        """
        pass

    def is_valid(self, operator: Operator, *types: IType) -> bool:
        """
        Verifies if the given operator and operands are valid to the operation

        :param operator:
        :param types: types of the operand
        :return: True if all arguments are valid. False otherwise.
        """
        if len(types) != self.number_of_operands:
            return False

        return operator is self.operator and self.validate_type(*types)

    @property
    def is_supported(self) -> bool:
        """
        Verifies if the operation is supported by the compiler

        :return: True if it is supported. False otherwise.
        """
        return True

    @classmethod
    @abstractmethod
    def build(cls, *operands: IType) -> Optional[IOperation]:
        """
        Creates an operation with the given operands types

        :param operands: operands types
        :return: The built operation if the operands are valid. None otherwise
        :rtype: IOperation or None
        """
        return None
