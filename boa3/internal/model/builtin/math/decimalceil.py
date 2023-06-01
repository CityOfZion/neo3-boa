from typing import Dict, Optional

from boa3.internal.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.internal.model.variable import Variable


class DecimalCeilingMethod(IBuiltinMethod):

    def __init__(self):
        from boa3.internal.model.type.type import Type
        identifier = 'ceil'
        args: Dict[str, Variable] = {'x': Variable(Type.int),
                                     'decimals': Variable(Type.int)}
        super().__init__(identifier, args, return_type=Type.int)

    @property
    def exception_message(self) -> str:
        return "decimals cannot be negative"

    def generate_opcodes(self, code_generator):
        from boa3.internal.model.operation.binaryop import BinaryOp
        from boa3.internal.model.operation.unaryop import UnaryOp

        # if decimals < 0
        code_generator.duplicate_stack_item(2)
        code_generator.convert_literal(0)
        code_generator.convert_operation(BinaryOp.Lt, is_internal=True)
        if_negative_decimal = code_generator.convert_begin_if()
        #   raise error
        code_generator.convert_literal(self.exception_message)
        code_generator.convert_raise_exception()
        code_generator.convert_end_if(if_negative_decimal, is_internal=True)

        # unit = 10 ** decimal
        code_generator.duplicate_stack_top_item()
        code_generator.swap_reverse_stack_items(3)
        code_generator.convert_literal(10)
        code_generator.swap_reverse_stack_items(2)
        code_generator.convert_operation(BinaryOp.Pow, is_internal=True)

        # difference = (-x) % unit
        code_generator.swap_reverse_stack_items(2)
        code_generator.convert_operation(UnaryOp.Negative, is_internal=True)
        code_generator.duplicate_stack_item(2)
        code_generator.convert_operation(BinaryOp.Mod, is_internal=True)

        # if difference < 0
        code_generator.duplicate_stack_top_item()
        code_generator.convert_literal(0)
        code_generator.convert_operation(BinaryOp.Lt, is_internal=True)
        if_negative_mod = code_generator.convert_begin_if()
        #   difference = unit + difference
        code_generator.convert_operation(BinaryOp.Add, is_internal=True)
        # else
        else_negative_mod = code_generator.convert_begin_else(if_negative_mod, is_internal=True)
        #   # just clear stack
        code_generator.remove_stack_item(2)
        code_generator.convert_end_if(else_negative_mod, is_internal=True)

        # result = x + difference
        code_generator.convert_operation(BinaryOp.Add, is_internal=True)
        super().generate_opcodes(code_generator)

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> Optional[str]:
        return
