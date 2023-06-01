import ast
from typing import Dict

from boa3.internal.model import set_internal_call
from boa3.internal.model.builtin.interop.interopmethod import InteropMethod
from boa3.internal.model.builtin.interop.runtime.notificationtype import NotificationType
from boa3.internal.model.variable import Variable


class GetNotificationsMethod(InteropMethod):

    def __init__(self, notification_type: NotificationType):
        from boa3.internal.model.type.collection.sequence.uint160type import UInt160Type
        from boa3.internal.model.type.type import Type

        identifier = 'get_notifications'
        syscall = 'System.Runtime.GetNotifications'
        uint160 = UInt160Type.build()

        args: Dict[str, Variable] = {'script_hash': Variable(Type.optional.build(uint160))}
        args_default = set_internal_call(ast.parse("{0}".format(Type.none.default_value)
                                                   ).body[0].value)

        super().__init__(identifier, syscall, args, [args_default],
                         return_type=Type.list.build([notification_type]))

    def generate_internal_opcodes(self, code_generator):
        from boa3.internal.model.operation.binaryop import BinaryOp
        from boa3.internal.model.type.type import Type

        # if arg is not None:
        code_generator.duplicate_stack_top_item()
        arg_is_null = code_generator.convert_begin_if()

        #   if arg == 0:
        code_generator.duplicate_stack_top_item()
        code_generator.convert_cast(Type.int, is_internal=True)
        code_generator.convert_literal(0)
        code_generator.convert_operation(BinaryOp.NumEq, is_internal=True)

        arg_is_zero = code_generator.convert_begin_if()
        #       arg = None
        code_generator.duplicate_stack_top_item()
        code_generator.convert_literal(None)
        code_generator.convert_end_if(arg_is_zero, is_internal=True)

        code_generator.convert_end_if(arg_is_null, is_internal=True)
        super().generate_internal_opcodes(code_generator)
