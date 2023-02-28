from typing import Dict

from boa3.internal.model.builtin.interop.interopevent import InteropEvent
from boa3.internal.model.variable import Variable


class NotifyMethod(InteropEvent):

    def __init__(self):
        self._event_name_key = 'notification_name'

        from boa3.internal.model.type.type import Type
        identifier = 'notify'
        syscall = 'System.Runtime.Notify'
        args: Dict[str, Variable] = {'state': Variable(Type.any),
                                     self._event_name_key: Variable(Type.str)
                                     }
        import ast
        event_name_default = ast.parse("'{0}'".format(identifier)
                                       ).body[0].value
        super().__init__(identifier, syscall, args, defaults=[event_name_default])

    @property
    def generate_name(self) -> bool:
        return False

    @property
    def args_to_generate(self) -> Dict[str, Variable]:
        return {key_name: value_type
                for key_name, value_type in self.args.items()
                if key_name != self._event_name_key}
