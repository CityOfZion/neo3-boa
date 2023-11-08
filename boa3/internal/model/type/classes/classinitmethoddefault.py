from typing import Optional

from boa3.internal import constants
from boa3.internal.model.identifiedsymbol import IdentifiedSymbol
from boa3.internal.model.method import Method
from boa3.internal.model.type.classes.userclass import UserClass
from boa3.internal.model.variable import Variable


class ClassInitMethod(IdentifiedSymbol, Method):
    def __init__(self, user_class: UserClass):
        self_var = Variable(user_class)
        args = {
            'self': self_var
        }
        base_init = None
        if len(user_class.bases) == 1:
            # TODO: change when class inheritance with multiple bases is implemented #2kq1gmc
            # use update to keep the original order
            base_init = user_class.bases[0].constructor_method()
            args.update(base_init.args)
            # but change the self type
            args['self'] = self_var

        Method.__init__(self, args=args, return_type=user_class)
        IdentifiedSymbol.__init__(self, identifier=constants.INIT_METHOD_ID)

        self.defined_by_entry = False
        self.is_init = True
        self.origin_class = user_class
        # __init__ method behave like class methods
        from boa3.internal.model.builtin.builtin import Builtin
        self.decorators.append(Builtin.ClassMethodDecorator)

        if base_init is not None:
            origin = self.origin if self.origin else self
            base_init.add_call_origin(origin)

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> Optional[str]:
        return None
