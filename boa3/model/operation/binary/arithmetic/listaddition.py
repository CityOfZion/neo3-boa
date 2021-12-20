from typing import List, Tuple

from boa3.model.operation.binary.binaryoperation import BinaryOperation
from boa3.model.operation.operator import Operator
from boa3.model.type.type import IType, Type
from boa3.neo.vm.opcode.Opcode import Opcode


class ListAddition(BinaryOperation):
    """
    A class used to represent a list addition operation

    :ivar operator: the operator of the operation. Inherited from :class:`IOperation`
    :ivar left: the left operand type. Inherited from :class:`BinaryOperation`
    :ivar right: the left operand type. Inherited from :class:`BinaryOperation`
    :ivar result: the result type of the operation.  Inherited from :class:`IOperation`
    """
    _valid_types: List[IType] = [Type.list]

    def __init__(self, left: IType = Type.list, right: IType = None):
        self.operator: Operator = Operator.Plus
        super().__init__(left, right)

    def validate_type(self, *types: IType) -> bool:
        if len(types) != self.number_of_operands:
            return False
        left: IType = types[0]
        right: IType = types[1]

        return left == right and any(_type.is_type_of(left) for _type in self._valid_types)

    def _get_result(self, left: IType, right: IType) -> IType:
        if self.validate_type(left, right):
            return left
        else:
            return Type.none

    @property
    def opcode(self) -> List[Tuple[Opcode, bytes]]:
        from boa3.neo.vm.type.Integer import Integer
        from boa3.neo.vm.type.StackItem import StackItemType
        return [
            (Opcode.OVER, b''),
            (Opcode.ISTYPE, StackItemType.Array),
            (Opcode.JMPIF, Integer(5).to_byte_array(signed=True, min_length=1)),
            (Opcode.CAT, b''),
            (Opcode.JMP, Integer(18).to_byte_array(signed=True, min_length=1)),
            (Opcode.UNPACK, b''),       # get the values, top of stack will be the array size
            (Opcode.JMP, Integer(9).to_byte_array(signed=True, min_length=1)),  # begin while
            (Opcode.DUP, b''),
            (Opcode.INC, b''),          # push the array to the top of the stack
            (Opcode.PICK, b''),
            (Opcode.PUSH2, b''),
            (Opcode.ROLL, b''),         # get the first value that wasn't appended yet
            (Opcode.APPEND, b''),       # append the value to the array
            (Opcode.DEC, b''),
            (Opcode.DUP, b''),          # when the array is empty, stop the loop
            (Opcode.JMPIF, Integer(-8).to_byte_array(signed=True, min_length=1)),
            (Opcode.DROP, b''),         # the top items in the stack will be the extended array
        ]
