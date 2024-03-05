from boa3.internal.model.operation.binary.binaryoperation import BinaryOperation
from boa3.internal.model.operation.operator import Operator
from boa3.internal.model.type.collection.icollection import ICollectionType
from boa3.internal.model.type.collection.mapping.mappingtype import MappingType
from boa3.internal.model.type.primitive.primitivetype import PrimitiveType
from boa3.internal.model.type.type import IType, Type


class CollectionNotMembership(BinaryOperation):
    """
    A class used to represent a collection not membership operation

    :ivar operator: the operator of the operation. Inherited from :class:`IOperation`
    :ivar left: the left operand type. Inherited from :class:`BinaryOperation`
    :ivar right: the left operand type. Inherited from :class:`BinaryOperation`
    :ivar result: the result type of the operation.  Inherited from :class:`IOperation`
    """
    _valid_types: list[IType] = [Type.collection]

    def __init__(self, left: IType = Type.any, right: IType = None):
        self.operator: Operator = Operator.NotIn

        if not isinstance(right, ICollectionType):
            right = Type.collection

        if not right.item_type.is_type_of(left) or right.item_type is Type.any and left is not Type.any:
            right = Type.collection.build(Type.sequence.build(left))

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
                                         right_operand: IType = None) -> tuple[IType | None, IType | None]:
        if isinstance(right_operand, ICollectionType):
            left = right_operand.item_type if not isinstance(right_operand, MappingType) else right_operand.key_type
            return left, right_operand

        return left_operand, self.right_type

    def generate_internal_opcodes(self, code_generator):
        from boa3.internal.model.operation.binary.additional import CollectionMembership
        from boa3.internal.model.operation.unaryop import UnaryOp

        code_generator.convert_operation(CollectionMembership(self.left_type, self.right_type),
                                         is_internal=True)
        code_generator.convert_operation(UnaryOp.Not, is_internal=True)
