from typing import List, Optional, Tuple

from boa3.model.operation.binary.binaryoperation import BinaryOperation
from boa3.model.operation.operator import Operator
from boa3.model.type.collection.icollection import ICollectionType
from boa3.model.type.collection.mapping.mappingtype import MappingType
from boa3.model.type.primitive.primitivetype import PrimitiveType
from boa3.model.type.type import IType, Type
from boa3.neo.vm.opcode.Opcode import Opcode


class CollectionMembership(BinaryOperation):
    """
    A class used to represent a collection membership operation

    :ivar operator: the operator of the operation. Inherited from :class:`IOperation`
    :ivar left: the left operand type. Inherited from :class:`BinaryOperation`
    :ivar right: the left operand type. Inherited from :class:`BinaryOperation`
    :ivar result: the result type of the operation.  Inherited from :class:`IOperation`
    """
    _valid_types: List[IType] = [Type.collection]

    def __init__(self, left: IType = Type.any, right: IType = None):
        self.operator: Operator = Operator.In

        if not isinstance(right, ICollectionType):
            right = Type.collection

        reference_type = right.key_type if isinstance(right, MappingType) else right.item_type
        if not reference_type.is_type_of(left) or (reference_type is Type.any and left is not Type.any):
            if Type.sequence.is_type_of(left):
                right = Type.collection.build(left)
            else:
                right = Type.collection.build(Type.list.build([left]))

        super().__init__(left, right)

    def validate_type(self, *types: IType) -> bool:
        if len(types) != self.number_of_operands:
            return False
        left: IType = types[0]
        right: IType = types[1]

        if not isinstance(right, ICollectionType):
            return False

        if isinstance(right, PrimitiveType) and (right.is_type_of(left) or left.is_type_of(right)):
            return True

        if isinstance(right, MappingType):
            reference_type = right.key_type
        else:
            reference_type = right.item_type

        return reference_type.is_type_of(left)

    def _get_result(self, left: IType, right: IType) -> IType:
        return Type.bool

    def get_valid_operand_for_validation(self, left_operand: IType,
                                         right_operand: IType = None) -> Tuple[Optional[IType], Optional[IType]]:
        if isinstance(right_operand, ICollectionType):
            left = right_operand.item_type if not isinstance(right_operand, MappingType) else right_operand.key_type
            return left, right_operand

        return left_operand, self.right_type

    @property
    def opcode(self) -> List[Tuple[Opcode, bytes]]:
        from boa3.neo.vm.type.Integer import Integer
        return [
            (Opcode.DUP, b''),
            (Opcode.ISTYPE, Type.mapping.stack_item),   # if isinstance(arg1, dict)
            (Opcode.JMPIFNOT, Integer(6).to_byte_array(signed=True, min_length=1)),
            (Opcode.SWAP, b''),
            (Opcode.HASKEY, b''),                           # return value.has_key(arg0)
            (Opcode.JMP, Integer(54).to_byte_array(signed=True, min_length=1)),
            (Opcode.DUP, b''),
            (Opcode.DUP, b''),
            (Opcode.ISTYPE, Type.str.stack_item),       # is_bytestr = isinstance(arg1, (str, bytes))
            (Opcode.SWAP, b''),
            (Opcode.SIZE, b''),                         # limit = len(arg1)
            (Opcode.OVER, b''),                         # if is_bytestr:
            (Opcode.JMPIFNOT, Integer(7).to_byte_array(signed=True, min_length=1)),
            (Opcode.PUSH3, b''),                            # limit = limit - len(arg0) + 1
            (Opcode.PICK, b''),
            (Opcode.SIZE, b''),
            (Opcode.SUB, b''),
            (Opcode.INC, b''),
            (Opcode.PUSH0, b''),                        # index = 0
            (Opcode.DUP, b''),                          # while index < limit:
            (Opcode.PUSH2, b''),
            (Opcode.PICK, b''),
            (Opcode.LT, b''),
            (Opcode.JMPIFNOT, Integer(28).to_byte_array(signed=True, min_length=1)),
            (Opcode.PUSH4, b''),                            # aux = arg0
            (Opcode.PICK, b''),
            (Opcode.PUSH4, b''),
            (Opcode.PICK, b''),
            (Opcode.PUSH2, b''),
            (Opcode.PICK, b''),
            (Opcode.PUSH5, b''),
            (Opcode.PICK, b''),                             # if is_bytestr:
            (Opcode.JMPIFNOT, Integer(10).to_byte_array(signed=True, min_length=1)),
            (Opcode.PUSH2, b''),                                # if arg1[index:len(arg0)] == arg0:
            (Opcode.PICK, b''),
            (Opcode.SIZE, b''),
            (Opcode.SUBSTR, b''),
            (Opcode.CONVERT, Type.str.stack_item),
            (Opcode.NUMEQUAL, b''),                                 # break
            (Opcode.JMP, Integer(4).to_byte_array(signed=True, min_length=1)),
            (Opcode.PICKITEM, b''),                         # elif arg1[index] == arg0:
            (Opcode.EQUAL, b''),                                    # break
            (Opcode.JMPIF, Integer(5).to_byte_array(signed=True, min_length=1)),
            (Opcode.INC, b''),                              # index += 1
            (Opcode.JMP, Integer(-30).to_byte_array(signed=True, min_length=1)),
            (Opcode.GT, b''),                       # return index < limit
            (Opcode.REVERSE4, b''),                     # if the value is found, index won't reach the limit
            (Opcode.DROP, b''),                     # remove auxiliar values from stack
            (Opcode.DROP, b''),
            (Opcode.DROP, b''),
        ]
