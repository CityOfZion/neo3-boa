from boa3.internal.model.operation.binary.binaryoperation import BinaryOperation
from boa3.internal.model.operation.operator import Operator
from boa3.internal.model.type.type import IType, Type
from boa3.internal.neo.vm.opcode.Opcode import Opcode


class GreaterThan(BinaryOperation):
    """
    A class used to represent a numeric greater than comparison

    :ivar operator: the operator of the operation. Inherited from :class:`IOperation`
    :ivar left: the left operand type. Inherited from :class:`BinaryOperation`
    :ivar right: the left operand type. Inherited from :class:`BinaryOperation`
    :ivar result: the result type of the operation.  Inherited from :class:`IOperation`
    """
    _valid_types: list[IType] = [Type.int]

    def __init__(self, left: IType = Type.int, right: IType = None):
        self.operator: Operator = Operator.Gt
        super().__init__(left, right)

    def validate_type(self, *types: IType) -> bool:
        if len(types) != self.number_of_operands:
            return False
        left: IType = types[0]
        right: IType = types[1]

        return left == right and any(_type.is_type_of(left) for _type in self._valid_types)

    def _get_result(self, left: IType, right: IType) -> IType:
        if self.validate_type(left, right):
            return Type.bool
        else:
            return Type.none

    def generate_internal_opcodes(self, code_generator):
        code_generator.insert_opcode(Opcode.GT)
