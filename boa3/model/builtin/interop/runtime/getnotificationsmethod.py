import ast
from typing import Dict, List, Tuple

from boa3.model.builtin.interop.interopmethod import InteropMethod
from boa3.model.builtin.interop.runtime.notificationtype import NotificationType
from boa3.model.variable import Variable
from boa3.neo.vm.opcode.Opcode import Opcode


class GetNotificationsMethod(InteropMethod):

    def __init__(self, notification_type: NotificationType):
        from boa3.model.type.collection.sequence.uint160type import UInt160Type
        from boa3.model.type.type import Type

        identifier = 'get_notifications'
        syscall = 'System.Runtime.GetNotifications'
        uint160 = UInt160Type.build()

        args: Dict[str, Variable] = {'script_hash': Variable(uint160)}
        args_default = ast.parse("{0}()".format(uint160.raw_identifier)
                                 ).body[0].value

        super().__init__(identifier, syscall, args, [args_default],
                         return_type=Type.list.build([notification_type]))

    @property
    def opcode(self) -> List[Tuple[Opcode, bytes]]:
        # TODO: Change when Optional or Union is implemented
        from boa3.neo.vm.type.Integer import Integer
        from boa3.model.type.type import Type
        opcodes = [
            (Opcode.DUP, b''),
            (Opcode.CONVERT, Type.int.stack_item),
            (Opcode.PUSH0, b''),
            (Opcode.NUMEQUAL, b''),
            (Opcode.JMPIFNOT, Integer(4).to_byte_array(signed=True)),
            (Opcode.DROP, b''),
            (Opcode.PUSHNULL, b'')
        ]
        opcodes.extend(super().opcode)

        return opcodes
