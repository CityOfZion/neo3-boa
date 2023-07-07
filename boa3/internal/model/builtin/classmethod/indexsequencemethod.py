import ast
from typing import Dict, Optional

from boa3.internal.model.builtin.classmethod.indexmethod import IndexMethod
from boa3.internal.model.expression import IExpression
from boa3.internal.model.type.collection.sequence.sequencetype import SequenceType
from boa3.internal.model.type.itype import IType
from boa3.internal.model.variable import Variable
from boa3.internal.neo.vm.opcode.Opcode import Opcode


class IndexSequenceMethod(IndexMethod):

    def __init__(self, sequence_type: Optional[SequenceType] = None, arg_value: Optional[IType] = None):
        from boa3.internal.model.type.type import Type
        if not isinstance(sequence_type, SequenceType):
            sequence_type = Type.sequence
        if not isinstance(arg_value, IType):
            arg_value = Type.any

        args: Dict[str, Variable] = {
            'self': Variable(sequence_type),
            'x': Variable(arg_value),
            'start': Variable(Type.int),
            'end': Variable(Type.int),
        }

        start_default = ast.parse("{0}".format(0)
                                  ).body[0].value
        end_default = ast.parse("-1").body[0].value.operand
        end_default.n = -1

        super().__init__(args, defaults=[start_default, end_default])

    def validate_parameters(self, *params: IExpression) -> bool:
        if 2 <= len(params) <= 4:
            return False
        if not all(isinstance(param, IExpression) for param in params):
            return False

        from boa3.internal.model.type.itype import IType
        sequence_type: IType = params[0].type

        if not isinstance(sequence_type, SequenceType):
            return False
        from boa3.internal.model.type.collection.sequence.mutable.listtype import ListType
        from boa3.internal.model.type.collection.sequence.tupletype import TupleType
        from boa3.internal.model.type.collection.sequence.rangetype import RangeType
        if not isinstance(sequence_type, (ListType, TupleType, RangeType)):
            return False
        return True

    @property
    def exception_message(self) -> str:
        return "x not in sequence"

    def generate_internal_opcodes(self, code_generator):
        from boa3.internal.model.builtin.builtin import Builtin
        from boa3.internal.model.operation.binaryop import BinaryOp

        # receives: end, start, x, sequence
        code_generator.swap_reverse_stack_items(4)

        # if index < 0:
        code_generator.duplicate_stack_top_item()
        code_generator.convert_literal(0)
        is_negative_index = code_generator.convert_begin_if()
        # # if index >= 0, jump to verify_big_end
        code_generator.change_jump(is_negative_index, Opcode.JMPGE)

        #   # gets the correspondent positive value of end
        #   end = end + len(sequence) + 1
        code_generator.duplicate_stack_item(4)
        code_generator.convert_builtin_method_call(Builtin.Len, is_internal=True)
        code_generator.convert_operation(BinaryOp.Add, is_internal=True)
        code_generator.insert_opcode(Opcode.INC)

        #   if index < 0:
        code_generator.duplicate_stack_top_item()
        code_generator.convert_literal(0)
        is_still_negative_index = code_generator.convert_begin_if()
        #   # if end is not negative anymore, start verifying start
        code_generator.change_jump(is_still_negative_index, Opcode.JMPGE)

        #       index = 0
        code_generator.remove_stack_top_item()
        code_generator.convert_literal(0)

        code_generator.convert_end_if(is_negative_index, is_internal=True)

        # if end > len(sequence)
        code_generator.duplicate_stack_top_item()
        code_generator.duplicate_stack_item(5)
        code_generator.convert_builtin_method_call(Builtin.Len, is_internal=True)
        is_big_end = code_generator.convert_begin_if()
        # # if end <= len(sequence), start verifying start
        code_generator.change_jump(is_big_end, Opcode.JMPLE)

        #   end = len(sequence)
        code_generator.remove_stack_top_item()
        code_generator.duplicate_stack_item(3)
        code_generator.convert_builtin_method_call(Builtin.Len, is_internal=True)

        code_generator.convert_end_if(is_still_negative_index, is_internal=True)
        code_generator.convert_end_if(is_big_end, is_internal=True)
        code_generator.swap_reverse_stack_items(2)

        # if index < 0:
        code_generator.duplicate_stack_top_item()
        code_generator.convert_literal(0)
        is_negative_index = code_generator.convert_begin_if()
        # # if index >= 0, jump to verify_big_start
        code_generator.change_jump(is_negative_index, Opcode.JMPGE)

        #   # gets the correspondent positive value of end
        #   start = start + len(sequence) + 1
        code_generator.duplicate_stack_item(4)
        code_generator.convert_builtin_method_call(Builtin.Len, is_internal=True)
        code_generator.convert_operation(BinaryOp.Add, is_internal=True)
        code_generator.insert_opcode(Opcode.INC)

        #   if index < 0:
        code_generator.duplicate_stack_top_item()
        code_generator.convert_literal(0)
        is_still_negative_index = code_generator.convert_begin_if()
        #   # if start is not negative anymore
        code_generator.change_jump(is_still_negative_index, Opcode.JMPGE)

        #       index = 0
        code_generator.remove_stack_top_item()
        code_generator.convert_literal(0)

        code_generator.convert_end_if(is_negative_index, is_internal=True)

        # if start > len(sequence)
        code_generator.duplicate_stack_top_item()
        code_generator.duplicate_stack_item(5)
        code_generator.convert_builtin_method_call(Builtin.Len, is_internal=True)
        is_big_end = code_generator.convert_begin_if()
        # # if start <= len(sequence), start verifying start
        code_generator.change_jump(is_big_end, Opcode.JMPLE)

        #   start = len(sequence)
        code_generator.remove_stack_top_item()
        code_generator.duplicate_stack_item(3)
        code_generator.convert_builtin_method_call(Builtin.Len, is_internal=True)

        code_generator.convert_end_if(is_still_negative_index, is_internal=True)
        code_generator.convert_end_if(is_big_end, is_internal=True)

        # begin while
        # while self[index] != x:
        while_start = code_generator.convert_begin_while()

        #   index += 1
        code_generator.insert_opcode(Opcode.INC)

        while_condition = code_generator.bytecode_size
        #   if end <= index
        code_generator.duplicate_stack_item(2)
        code_generator.duplicate_stack_item(2)
        invalid_index = code_generator.convert_begin_if()
        code_generator.change_jump(invalid_index, Opcode.JMPGT)
        #       raise error
        code_generator.convert_literal(self.exception_message)
        code_generator.convert_raise_exception()

        invalid_index = code_generator.convert_begin_else(invalid_index, is_internal=True)

        code_generator.convert_end_if(invalid_index, is_internal=True)

        #   self[index] == x:
        code_generator.duplicate_stack_item(4)
        code_generator.duplicate_stack_item(2)
        code_generator.convert_get_item(index_inserted_internally=True)
        code_generator.duplicate_stack_item(4)
        code_generator.convert_operation(BinaryOp.NumNotEq, is_internal=True)

        code_generator.convert_end_while(while_start, while_condition, is_internal=True)

        for _ in range(1, len(self.args)):
            code_generator.remove_stack_item(2)
