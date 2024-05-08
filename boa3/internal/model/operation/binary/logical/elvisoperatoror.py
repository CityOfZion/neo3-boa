from boa3.internal.model.operation.binary.binaryoperation import BinaryOperation
from boa3.internal.model.operation.operator import Operator
from boa3.internal.model.type.type import IType, Type


class ElvisOperatorOr(BinaryOperation):
    """
    A class used to represent the boolean or operation

    :ivar operator: the operator of the operation. Inherited from :class:`IOperation`
    :ivar left: the left operand type. Inherited from :class:`BinaryOperation`
    :ivar right: the left operand type. Inherited from :class:`BinaryOperation`
    :ivar result: the result type of the operation.  Inherited from :class:`IOperation`
    """
    _valid_types: list[IType] = [Type.bool]

    def __init__(self, left: IType = Type.bool, right: IType = None):
        self.operator: Operator = Operator.Or
        super().__init__(left, right)

    def validate_type(self, *types: IType) -> bool:
        if len(types) != self.number_of_operands:
            return False
        left: IType = types[0]
        right: IType = types[1]

        return True

    def _get_result(self, left: IType, right: IType) -> IType:
        if left.is_type_of(right) and right.is_type_of(left):
            return right
        else:
            return Type.union.build([left, right])

    def generate_internal_opcodes(self, code_generator):
        from boa3.internal.model.builtin.builtin import Builtin

        code_generator.swap_reverse_stack_items(2)
        code_generator.duplicate_stack_top_item()
        code_generator.convert_builtin_method_call(Builtin.Bool, is_internal=True)

        is_true = code_generator.convert_begin_if()
        code_generator.remove_stack_item(2)

        is_false = code_generator.convert_begin_else(is_true, is_internal=True)
        code_generator.remove_stack_top_item()
        code_generator.convert_end_if(is_false, is_internal=True)
