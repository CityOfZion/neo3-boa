from typing import Dict, List, Optional, Tuple

from boa3.internal.model.builtin.classmethod.countmethod import CountMethod
from boa3.internal.model.expression import IExpression
from boa3.internal.model.type.collection.sequence.sequencetype import SequenceType
from boa3.internal.model.type.itype import IType
from boa3.internal.model.variable import Variable


class CountSequenceMethod(CountMethod):

    def __init__(self, sequence_type: Optional[SequenceType] = None, arg_value: Optional[IType] = None):
        from boa3.internal.model.type.type import Type
        if not isinstance(sequence_type, SequenceType):
            sequence_type = Type.sequence
        if not isinstance(arg_value, IType):
            arg_value = Type.any

        args: Dict[str, Variable] = {
            'self': Variable(sequence_type),
            'value': Variable(arg_value)
        }

        super().__init__(args)

    def validate_parameters(self, *params: IExpression) -> bool:
        if len(params) != 2:
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

    def generate_internal_opcodes(self, code_generator):
        from boa3.internal.model.builtin.builtin import Builtin
        from boa3.internal.model.operation.binaryop import BinaryOp
        from boa3.internal.neo.vm.opcode.Opcode import Opcode

        # aux = self.copy()
        code_generator.convert_copy()

        # count = 0
        code_generator.convert_literal(0)

        # index = len(sequence) - 1
        code_generator.duplicate_stack_item(2)
        code_generator.convert_builtin_method_call(Builtin.Len, is_internal=True)
        code_generator.insert_opcode(Opcode.DEC)

        # while index >= 0:
        while_start = code_generator.convert_begin_while()

        jmps_to_inc, jmps_to_condition = self._generic_verification(code_generator)

        #   element = sequence[index]
        code_generator.duplicate_stack_item(3)
        code_generator.duplicate_stack_item(2)
        code_generator.convert_get_item(index_inserted_internally=True)

        #   if element == value:
        code_generator.duplicate_stack_item(5)
        is_equal = code_generator.convert_begin_if()
        code_generator.change_jump(is_equal, Opcode.JMPNE)

        for address in jmps_to_inc:
            code_generator.convert_end_if(address, is_internal=True)

        #       count += 1
        code_generator.swap_reverse_stack_items(2)
        code_generator.insert_opcode(Opcode.INC)
        code_generator.swap_reverse_stack_items(2)

        code_generator.convert_end_if(is_equal)
        for address in jmps_to_condition:
            code_generator.convert_end_if(address, is_internal=True)

        #   index -= 1
        code_generator.insert_opcode(Opcode.DEC)

        # while condition
        while_condition = code_generator.bytecode_size
        code_generator.duplicate_stack_top_item()
        code_generator.insert_opcode(Opcode.SIGN)
        code_generator.convert_literal(0)
        code_generator.convert_operation(BinaryOp.GtE)

        code_generator.convert_end_while(while_start, while_condition, is_internal=True)

        # clean stack
        code_generator.remove_stack_top_item()
        code_generator.swap_reverse_stack_items(3)
        code_generator.remove_stack_top_item()
        code_generator.remove_stack_top_item()

    def _generic_verification(self, code_generator) -> Tuple[List[int], List[int]]:
        """
        Generate the Neo VM opcodes for the method.

        :type code_generator: boa3.internal.compiler.codegenerator.codegenerator.CodeGenerator
        """
        return [], []
