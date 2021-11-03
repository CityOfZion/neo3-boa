from typing import List, Optional, Tuple

from boa3 import constants
from boa3.model.builtin.method import IBuiltinMethod
from boa3.model.type.classes.userclass import UserClass
from boa3.model.variable import Variable
from boa3.neo.vm.opcode.Opcode import Opcode


class ClassInitMethod(IBuiltinMethod):
    def __init__(self, user_class: UserClass):
        self_var = Variable(user_class)
        args = {
            'self': self_var
        }
        if len(user_class.bases) == 1:
            # TODO: change when class inheritance with multiple bases is implemented
            # use update to keep the original order
            args.update(user_class.bases[0].constructor_method().args)
            # but change the self type
            args['self'] = self_var

        super().__init__(identifier=constants.INIT_METHOD_ID,
                         args=args,
                         return_type=user_class)
        self.is_init = True
        self.origin_class = user_class
        # __init__ method behave like class methods
        from boa3.model.builtin.builtin import Builtin
        self.decorators.append(Builtin.ClassMethodDecorator)

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> Optional[str]:
        return None

    @property
    def opcode(self) -> List[Tuple[Opcode, bytes]]:
        if self.origin_class is None or len(self.origin_class.bases) == 0:
            return super().opcode

        opcodes = []

        for base in self.origin_class.bases:
            base_constructor = base.constructor_method()
            call_base_init = []
            num_args = len(base_constructor.args)

            opcode = Opcode.get_dup(num_args)
            if opcode is Opcode.PICK:
                load_arg = [
                    Opcode.get_push_and_data(num_args - 1),
                    (opcode, b'')
                ]
            else:
                load_arg = [(opcode, b'')]

            call_base_init.extend(load_arg * num_args)
            call_base_init.append((Opcode.CALL, base_constructor))
            call_base_init.append((Opcode.DROP, b''))

            opcodes.extend(call_base_init)

        additional_args = len(self.args) - 1  # num of arguments, not counting self
        if additional_args > 0:
            opcodes.extend([(Opcode.NIP, b'')] * additional_args)
        return opcodes
