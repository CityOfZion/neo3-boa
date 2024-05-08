from typing import Any

from boa3.internal.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.internal.model.expression import IExpression
from boa3.internal.model.type.collection.sequence.sequencetype import SequenceType
from boa3.internal.model.type.collection.sequence.tupletype import TupleType
from boa3.internal.model.type.itype import IType
from boa3.internal.model.variable import Variable
from boa3.internal.neo.vm.opcode.Opcode import Opcode


class PrintMethod(IBuiltinMethod):

    def __init__(self, arg_value: IType | None = None):
        from boa3.internal.model.type.type import Type
        identifier = 'print'
        if not isinstance(arg_value, IType):
            arg_value = Type.str

        args: dict[str, Variable] = {}
        vararg = ('values', Variable(arg_value))
        super().__init__(identifier, args, return_type=Type.none, vararg=vararg)

    @property
    def _arg_values(self) -> Variable:
        return self._vararg[1]

    @property
    def identifier(self) -> str:
        from boa3.internal.model.type.type import Type
        if self._arg_values.type is Type.str:
            return self._identifier
        return '-{0}_from_{1}'.format(self._identifier, self._arg_values.type._identifier)

    def validate_parameters(self, *params: IExpression) -> bool:
        if len(params) != 1:
            return False
        if not isinstance(params[0], IExpression):
            return False
        return isinstance(params[0].type, SequenceType)

    def generate_internal_opcodes(self, code_generator):
        from boa3.internal.model.builtin.builtin import Builtin
        from boa3.internal.model.builtin.interop.interop import Interop
        from boa3.internal.model.operation.binaryop import BinaryOp

        values_to_print = (self._arg_values.type.value_type
                           if hasattr(self._arg_values.type, 'value_type')
                           else self._arg_values.type)
        # if len(arg) > 0:
        code_generator.duplicate_stack_top_item()
        code_generator.convert_builtin_method_call(Builtin.Len, is_internal=True)
        code_generator.convert_literal(0)
        code_generator.convert_operation(BinaryOp.Gt, is_internal=True)

        if_not_empty = code_generator.convert_begin_if()

        #   aux_list = arg.copy().reverse()
        code_generator.convert_copy()
        code_generator.duplicate_stack_top_item()
        code_generator.convert_builtin_method_call(Builtin.SequenceReverse, is_internal=True)

        #   while len(aux_list) > 0
        start_loop = code_generator.convert_begin_while()
        #       _internal_print(aux_list.pop())
        code_generator.duplicate_stack_top_item()
        code_generator.insert_opcode(Opcode.POPITEM, add_to_stack=[values_to_print], pop_from_stack=True)
        self._generate_print_opcodes(code_generator)
        code_generator.convert_builtin_method_call(Interop.Log, is_internal=True)

        start_loop_condition = code_generator.bytecode_size
        code_generator.duplicate_stack_top_item()
        code_generator.convert_builtin_method_call(Builtin.Len, is_internal=True)
        code_generator.convert_literal(0)
        code_generator.convert_operation(BinaryOp.Gt, is_internal=True)

        code_generator.convert_end_while(start_loop, start_loop_condition, is_internal=True)

        code_generator.convert_end_if(if_not_empty, is_internal=True)

        # clear stack
        code_generator.remove_stack_top_item()

    def _generate_print_opcodes(self, code_generator):
        """
        :type code_generator: boa3.internal.compiler.codegenerator.codegenerator.CodeGenerator
        """
        pass

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> str | None:
        return None

    def build(self, value: Any) -> IBuiltinMethod:
        if isinstance(value, list) and len(value) == 1:
            value = value[0]
        if isinstance(value, TupleType):
            value = value.value_type
        if type(value) == type(self._arg_values.type):
            return self

        from boa3.internal.model.builtin.method.printbytestringmethod import PrintByteStringMethod
        from boa3.internal.model.type.classes.userclass import UserClass
        from boa3.internal.model.type.type import Type

        if Type.bool.is_type_of(value):
            from boa3.internal.model.builtin.method.printboolmethod import PrintBoolMethod
            return PrintBoolMethod()

        elif Type.int.is_type_of(value):
            from boa3.internal.model.builtin.method.printintmethod import PrintIntMethod
            return PrintIntMethod()

        elif Type.str.is_type_of(value) or Type.bytes.is_type_of(value):
            return PrintByteStringMethod(value)

        elif isinstance(value, UserClass):
            from boa3.internal.model.builtin.method.printclassmethod import PrintClassMethod
            return PrintClassMethod(value)

        elif Type.sequence.is_type_of(value):
            from boa3.internal.model.builtin.method.printsequencemethod import PrintSequenceMethod
            return PrintSequenceMethod(value)

        return PrintByteStringMethod(value)
