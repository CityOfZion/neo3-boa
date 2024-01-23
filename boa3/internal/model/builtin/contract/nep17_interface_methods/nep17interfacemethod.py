import ast

from boa3.internal.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.internal.model.type.itype import IType
from boa3.internal.model.variable import Variable


class Nep17InterfaceMethod(IBuiltinMethod):

    def __init__(self, args: dict[str, Variable], identifier: str,
                 return_type: IType, defaults: list[ast.AST] = None,
                 native_identifier: str = None):
        super().__init__(identifier, args, return_type=return_type, defaults=defaults)
        if native_identifier is None:
            self.native_identifier = identifier
        else:
            self.native_identifier = native_identifier

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> str | None:
        return None

    def generate_internal_opcodes(self, code_generator):
        from boa3.internal.model.builtin.interop.interop import Interop
        from boa3.internal.model.type.type import Type
        from boa3.builtin.interop.contract import CallFlags

        if len(self.args) != 1:
            code_generator.swap_reverse_stack_items(len(self.args))
            code_generator.swap_reverse_stack_items(len(self.args) - 1)

        code_generator.convert_new_array(len(self.args) - 1)
        code_generator.convert_literal(CallFlags.ALL)
        code_generator.convert_literal(self.native_identifier)
        code_generator.duplicate_stack_item(4)
        code_generator.convert_literal(2)   # Nep17Contract script hash
        code_generator.convert_get_item(index_inserted_internally=True, index_is_positive=True, test_is_negative_index=False)
        code_generator.convert_builtin_method_call(Interop.CallContract, is_internal=True)
        code_generator.remove_stack_item(2)

        if self.return_type is Type.none:
            code_generator.remove_stack_top_item()
