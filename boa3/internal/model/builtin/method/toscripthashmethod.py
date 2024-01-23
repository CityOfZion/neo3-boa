from collections.abc import Sized
from typing import Any

from boa3.internal.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.internal.model.expression import IExpression
from boa3.internal.model.type.primitive.primitivetype import PrimitiveType
from boa3.internal.model.type.type import IType, Type
from boa3.internal.model.variable import Variable
from boa3.internal.neo.vm.opcode.Opcode import Opcode


class ScriptHashMethod(IBuiltinMethod):

    def __init__(self, data_type: IType = None):
        if (not Type.int.is_type_of(data_type)
                and not Type.str.is_type_of(data_type)
                and not Type.bytes.is_type_of(data_type)):
            data_type = Type.any

        identifier = 'to_script_hash'
        args: dict[str, Variable] = {'value': Variable(data_type)}
        from boa3.internal.model.type.collection.sequence.uint160type import UInt160Type
        super().__init__(identifier, args, return_type=UInt160Type.build())

    @property
    def identifier(self) -> str:
        from boa3.internal.model.type.type import Type
        self_type = self.args['value'].type
        if self_type is Type.any:
            return self._identifier
        return '-{0}_from_{1}'.format(self._identifier, self_type._identifier)

    def validate_parameters(self, *params: IExpression) -> bool:
        if len(params) != 1:
            return False
        if not isinstance(params[0], IExpression):
            return False
        return isinstance(params[0].type, PrimitiveType)

    @property
    def is_supported(self) -> bool:
        return self.args['value'].type is not Type.any

    def generate_internal_opcodes(self, code_generator):
        from boa3.internal import constants
        from boa3.internal.model.builtin.builtin import Builtin
        from boa3.internal.neo.vm.type.StackItem import StackItemType
        from boa3.internal.model.builtin.interop.interop import Interop

        # try:
        try_begin = code_generator.convert_begin_try()

        #   if not isinstance(self, str):
        code_generator.duplicate_stack_top_item()
        code_generator.insert_type_check(StackItemType.ByteString)
        is_str = code_generator.convert_begin_if()
        code_generator.change_jump(is_str, Opcode.JMPIF)

        #       cast(self, str)
        code_generator.convert_cast(Type.str, is_internal=True)
        code_generator.convert_end_if(is_str, is_internal=True)

        #   result = base58_decode
        code_generator.duplicate_stack_top_item()
        code_generator.convert_builtin_method_call(Interop.Base58Decode, is_internal=True)

        #   if len(result) < SIZE_OF_INT160 + 1
        code_generator.duplicate_stack_top_item()
        code_generator.convert_builtin_method_call(Builtin.Len, is_internal=True)
        code_generator.convert_literal(constants.SIZE_OF_INT160 + 1)
        code_generator.swap_reverse_stack_items(2)
        code_generator.duplicate_stack_item(2)
        is_result_size_valid = code_generator.convert_begin_if()
        code_generator.change_jump(is_result_size_valid, Opcode.JMPGE)

        #       raise error
        code_generator.remove_stack_top_item()
        code_generator.remove_stack_top_item()
        code_generator.convert_raise_exception()
        code_generator.convert_end_if(is_result_size_valid, is_internal=True)

        #   result = result[1:]
        code_generator.insert_opcode(Opcode.DEC)
        code_generator.convert_literal(1)
        code_generator.swap_reverse_stack_items(2)
        code_generator.convert_get_substring(is_internal=True)
        code_generator.remove_stack_item(2)

        # except:
        try_end = code_generator.convert_try_except('ValueError')
        #     result = hash160(self)
        code_generator.convert_builtin_method_call(Interop.Hash160, is_internal=True)

        code_generator.convert_end_try(try_begin, try_end)

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> str | None:
        return None

    def build(self, value: Any) -> IBuiltinMethod:
        if 'value' in self.args and self.args['value'].type is not Type.any:
            return self

        from boa3.internal.model.type.collection.sequence.ecpointtype import ECPointType
        from boa3.internal.model.type.primitive.inttype import IntType
        from boa3.internal.model.type.primitive.strtype import StrType
        from boa3.internal.model.type.primitive.bytestype import BytesType

        if isinstance(value, Sized) and len(value) == 1:
            value = value[0]

        if isinstance(value, ECPointType):
            from boa3.internal.model.builtin.method.ecpointtoscripthashmethod import ECPointToScriptHashMethod
            return ECPointToScriptHashMethod()
        elif isinstance(value, (IntType, StrType, BytesType)):
            return ScriptHashMethod(value)
        elif isinstance(value, IType):
            return ScriptHashMethod(Type.bytes)
        return super().build(value)
