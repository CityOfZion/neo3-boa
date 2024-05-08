from collections.abc import Sequence
from typing import Any

from boa3.internal.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.internal.model.type.itype import IType
from boa3.internal.model.variable import Variable
from boa3.internal.neo.vm.opcode.Opcode import Opcode


class AbortMethod(IBuiltinMethod):

    def __init__(self, message_type=None):
        import ast
        from boa3.internal.model.type.itype import IType
        from boa3.internal.model.type.type import Type

        identifier = 'abort'

        if isinstance(message_type, IType):
            args: dict[str, Variable] = {
                'msg': Variable(Type.optional.build(message_type))
            }
            defaults = [
                ast.parse(f'{Type.none.default_value}').body[0].value
            ]

        else:
            args: dict[str, Variable] = {}
            defaults = []

        super().__init__(identifier, args, defaults, return_type=Type.none)

    @property
    def identifier(self) -> str:
        if 'msg' not in self.args:
            return super().identifier

        return '-{0}_{1}'.format(self._identifier, self.args['msg'].type.identifier)

    def generate_internal_opcodes(self, code_generator):
        code_generator.insert_opcode(Opcode.ABORT)

    @property
    def _args_on_stack(self) -> int:
        return 0

    def build(self, value: Any):
        if not isinstance(value, Sequence):
            value = [value]

        if len(value) == len(self.args):
            return self

        if len(value) > 0:
            obj = AbortStrMethod()
        else:
            from boa3.internal.model.builtin.builtin import Builtin
            obj = Builtin.Abort
        return obj

    @property
    def _body(self) -> str | None:
        return None


class AbortStrMethod(AbortMethod):
    def __init__(self):
        from boa3.internal.model.type.type import Type
        message_type = Type.str
        super().__init__(message_type)

    def msg_arg_type(self) -> IType:
        from boa3.internal.model.type.type import Type
        return self.args['msg'].type if 'msg' in self.args else Type.optional.build(Type.str)

    def generate_internal_opcodes(self, code_generator):
        from boa3.internal.model.type.type import Type

        msg = code_generator._stack[-1] if len(code_generator._stack) else self.msg_arg_type()
        # if msg is str | None both variables are going to be set as True
        is_not_str = not Type.str.is_type_of(msg)
        is_not_none = not Type.none.is_type_of(msg)

        if is_not_str and is_not_none:
            # need to check the type at runtime
            code_generator.duplicate_stack_top_item()
            code_generator.insert_type_check(Type.str.stack_item)

            check_valid = code_generator.convert_begin_if()
            code_generator.change_jump(check_valid, Opcode.JMPIF)
            super().generate_internal_opcodes(code_generator)
            code_generator.convert_end_if(check_valid, is_internal=True)
            type_check_done = True
        else:
            type_check_done = False

        code_generator.convert_abort(has_message=True, is_internal=type_check_done)
