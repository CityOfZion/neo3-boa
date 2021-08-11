from typing import List, Optional, Tuple

from boa3 import constants
from boa3.model.builtin.method import IBuiltinMethod
from boa3.model.type.classes.userclass import UserClass
from boa3.model.variable import Variable
from boa3.neo.vm.opcode.Opcode import Opcode


class ClassInitMethod(IBuiltinMethod):
    def __init__(self, user_class: UserClass):
        self.origin_class = user_class
        args = {
            'self': Variable(user_class)
        }

        super().__init__(identifier=constants.INIT_METHOD_ID,
                         args=args,
                         return_type=user_class)
        self.is_init = True
        # __init__ method behave like class methods
        from boa3.model.builtin.builtin import Builtin
        self.decorators.append(Builtin.ClassMethodDecorator)

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def opcode(self) -> List[Tuple[Opcode, bytes]]:
        variables_count = len(self.origin_class.variables)

        empty_array = [
            (Opcode.NEWARRAY0, b'')
        ]

        array_with_size = [
            Opcode.get_push_and_data(variables_count),
            (Opcode.NEWARRAY, b'')
        ]

        return array_with_size if variables_count > 0 else empty_array

    @property
    def _body(self) -> Optional[str]:
        return None
