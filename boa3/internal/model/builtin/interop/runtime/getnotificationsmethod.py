import ast
from typing import Dict, List, Tuple

from boa3.internal.model import set_internal_call
from boa3.internal.model.builtin.interop.interopmethod import InteropMethod
from boa3.internal.model.builtin.interop.runtime.notificationtype import NotificationType
from boa3.internal.model.variable import Variable
from boa3.internal.neo.vm.opcode import OpcodeHelper
from boa3.internal.neo.vm.opcode.Opcode import Opcode


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

    @property
    def _opcode(self) -> List[Tuple[Opcode, bytes]]:
        from boa3.internal.neo.vm.type.Integer import Integer
        from boa3.internal.model.type.type import Type
        jmp_place_holder = (Opcode.JMP, b'\x01')

        verify_arg_is_null = [
            (Opcode.DUP, b''),
            (Opcode.JMPIFNOT, jmp_place_holder),
        ]

        arg_is_not_null = [
            (Opcode.DUP, b''),
            (Opcode.CONVERT, Type.int.stack_item),
            (Opcode.PUSH0, b''),
            (Opcode.NUMEQUAL, b''),
            (Opcode.JMPIFNOT, Integer(4).to_byte_array(signed=True)),
            (Opcode.DROP, b''),
            (Opcode.PUSHNULL, b'')
        ]

        from boa3.internal.compiler.codegenerator import get_bytes_count
        jmp_to_convert = OpcodeHelper.get_jump_and_data(Opcode.JMPIFNOT, get_bytes_count(arg_is_not_null), True)
        verify_arg_is_null[-1] = jmp_to_convert

        return (
            verify_arg_is_null +
            arg_is_not_null +
            super()._opcode
        )
