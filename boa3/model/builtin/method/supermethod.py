from typing import Optional

from boa3.model.builtin.method.builtinmethod import IBuiltinMethod


class SuperMethod(IBuiltinMethod):

    def __init__(self):
        # TODO: Change when super() is implemented
        identifier = 'super'
        super().__init__(identifier)

    @property
    def is_supported(self) -> bool:
        # TODO: Change when super() is implemented
        return False

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> Optional[str]:
        return
