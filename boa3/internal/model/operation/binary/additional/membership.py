from typing import List, Optional, Tuple

from boa3.internal.model.operation.binary.binaryoperation import BinaryOperation
from boa3.internal.model.operation.operator import Operator
from boa3.internal.model.type.collection.icollection import ICollectionType
from boa3.internal.model.type.collection.mapping.mappingtype import MappingType
from boa3.internal.model.type.primitive.primitivetype import PrimitiveType
from boa3.internal.model.type.type import IType, Type
from boa3.internal.neo.vm.opcode.Opcode import Opcode


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

    def generate_internal_opcodes(self, code_generator):
        from boa3.internal.model.builtin.builtin import Builtin
        from boa3.internal.model.operation.binaryop import BinaryOp

        code_generator.duplicate_stack_top_item()
        code_generator.insert_type_check(Type.dict.stack_item)
        # if isinstance(arg1, dict)
        is_dict = code_generator.convert_begin_if()

        #   return value.has_key(arg0)
        code_generator.swap_reverse_stack_items(2)
        code_generator.insert_opcode(Opcode.HASKEY, pop_from_stack=True, add_to_stack=[Type.bool])

        is_dict = code_generator.convert_begin_else(is_dict, is_internal=True)
        code_generator.duplicate_stack_top_item()

        # is_bytestr = isinstance(arg1, (str, bytes))
        code_generator.duplicate_stack_top_item()
        code_generator.insert_type_check(Type.str.stack_item)

        # limit = len(arg1)
        code_generator.swap_reverse_stack_items(2)
        code_generator.convert_builtin_method_call(Builtin.Len, is_internal=True)

        code_generator.duplicate_stack_item(2)
        # if is_bytestr:
        is_bytestr = code_generator.convert_begin_if()

        #   limit = limit - len(arg0) + 1
        code_generator.duplicate_stack_item(4)
        code_generator.convert_builtin_method_call(Builtin.Len, is_internal=True)
        code_generator.convert_operation(BinaryOp.Sub, is_internal=True)
        code_generator.insert_opcode(Opcode.INC)

        code_generator.convert_end_if(is_bytestr)

        # index = 0
        code_generator.convert_literal(0)

        # while index < limit:
        while_start = code_generator.convert_begin_while()

        code_generator.duplicate_stack_item(5)
        code_generator.duplicate_stack_item(5)
        code_generator.duplicate_stack_item(3)
        #   aux = arg0

        code_generator.duplicate_stack_item(6)
        #   if is_bytestr:
        is_bytestr_while = code_generator.convert_begin_if()

        code_generator.duplicate_stack_item(3)
        code_generator.convert_builtin_method_call(Builtin.Len, is_internal=True)
        code_generator.convert_get_substring(is_internal=True)
        code_generator.convert_operation(BinaryOp.NumEq, is_internal=True)
        #       if arg1[index:len(arg0)] == arg0:
        break_if = code_generator.convert_begin_if()
        #           break
        code_generator.convert_loop_break()

        code_generator.convert_end_if(break_if, is_internal=True)
        is_bytestr_while = code_generator.convert_begin_else(is_bytestr_while, is_internal=True)

        code_generator.convert_get_item(index_inserted_internally=True)
        code_generator.convert_operation(BinaryOp.Eq, is_internal=True)
        #   elif arg1[index] == arg0:
        break_elif = code_generator.convert_begin_if()
        #       break
        code_generator.convert_loop_break()

        code_generator.convert_end_if(break_elif, is_internal=True)
        code_generator.convert_end_if(is_bytestr_while, is_internal=True)

        #   index += 1
        code_generator.insert_opcode(Opcode.INC)

        while_condition = code_generator.bytecode_size
        code_generator.duplicate_stack_top_item()
        code_generator.duplicate_stack_item(3)
        code_generator.convert_operation(BinaryOp.Lt, is_internal=True)

        code_generator.convert_end_while(while_start, while_condition, is_internal=True)

        # return limit > index
        #   if the value is found, index won't reach the limit
        code_generator.convert_operation(BinaryOp.Gt, is_internal=True)

        # remove auxiliary values from stack
        code_generator.swap_reverse_stack_items(4)
        code_generator.remove_stack_top_item()
        code_generator.remove_stack_top_item()
        code_generator.remove_stack_top_item()

        code_generator.convert_end_if(is_dict, is_internal=True)
