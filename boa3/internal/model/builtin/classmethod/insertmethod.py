from typing import Any, Dict, List, Optional

from boa3.internal.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.internal.model.expression import IExpression
from boa3.internal.model.type.collection.sequence.mutable.mutablesequencetype import MutableSequenceType
from boa3.internal.model.variable import Variable


class InsertMethod(IBuiltinMethod):
    def __init__(self, sequence_type: MutableSequenceType = None):
        if not isinstance(sequence_type, MutableSequenceType):
            from boa3.internal.model.type.type import Type
            sequence_type = Type.mutableSequence

        self_arg = Variable(sequence_type)
        index_arg = Variable(sequence_type.valid_key)
        item_arg = Variable(sequence_type.value_type)

        identifier = 'insert'
        args: Dict[str, Variable] = {'self': self_arg,
                                     '__index': index_arg,
                                     '__object': item_arg}
        super().__init__(identifier, args)

    @property
    def _arg_self(self) -> Variable:
        return self.args['self']

    def validate_parameters(self, *params: IExpression) -> bool:
        if len(params) != 3:
            return False
        if not all(isinstance(param, IExpression) for param in params):
            return False

        from boa3.internal.model.type.itype import IType
        sequence_type: IType = params[0].type
        index_type: IType = params[1].type
        value_type: IType = params[2].type

        if not isinstance(sequence_type, MutableSequenceType):
            return False
        return sequence_type.key_type.is_type_of(index_type) and sequence_type.value_type.is_type_of(value_type)

    def validate_negative_arguments(self) -> List[int]:
        return [list(self.args).index('__index')]

    def generate_internal_opcodes(self, code_generator):
        from boa3.internal.model.builtin.builtin import Builtin
        from boa3.internal.model.operation.binaryop import BinaryOp
        from boa3.internal.neo.vm.opcode.Opcode import Opcode

        code_generator.duplicate_stack_item(3)
        code_generator.duplicate_stack_top_item()
        code_generator.convert_builtin_method_call(Builtin.Len, is_internal=True)
        code_generator.insert_opcode(Opcode.DEC)

        code_generator.duplicate_stack_item(2)
        code_generator.duplicate_stack_item(2)
        code_generator.convert_get_item(index_inserted_internally=True)

        # array.append(value)
        code_generator.duplicate_stack_item(3)
        code_generator.swap_reverse_stack_items(2)
        code_generator.convert_builtin_method_call(Builtin.SequenceAppend, is_internal=True)

        # x = len(array) - 1

        # while x > index:
        while_begin = code_generator.convert_begin_while()

        #   array[x] = array[x - 1]
        code_generator.duplicate_stack_top_item()
        code_generator.insert_opcode(Opcode.DEC)

        code_generator.duplicate_stack_item(3)
        code_generator.duplicate_stack_top_item()
        code_generator.swap_reverse_stack_items(3)
        code_generator.convert_get_item(index_inserted_internally=True)

        code_generator.duplicate_stack_item(3)
        value_address = code_generator.bytecode_size
        code_generator.swap_reverse_stack_items(2)
        code_generator.convert_set_item(value_address, index_inserted_internally=True)

        #   x =- 1
        code_generator.insert_opcode(Opcode.DEC)

        while_condition = code_generator.bytecode_size
        code_generator.duplicate_stack_top_item()
        code_generator.duplicate_stack_item(4)
        code_generator.convert_operation(BinaryOp.Gt)

        code_generator.convert_end_while(while_begin, while_condition, is_internal=True)

        # clean stack from loop variables
        code_generator.remove_stack_top_item()
        code_generator.remove_stack_top_item()

        # array[index] = object
        value_address = code_generator.bytecode_size
        code_generator.swap_reverse_stack_items(2)
        code_generator.convert_set_item(value_address, index_inserted_internally=True)

    def push_self_first(self) -> bool:
        return self.has_self_argument

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> Optional[str]:
        return None

    def build(self, value: Any) -> IBuiltinMethod:
        if type(value) == type(self.args['self'].type):
            return self
        if isinstance(value, MutableSequenceType):
            return InsertMethod(value)
        return super().build(value)
