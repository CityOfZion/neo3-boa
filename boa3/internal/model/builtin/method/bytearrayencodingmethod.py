from typing import Dict, Optional

from boa3.internal.model.builtin.method import ByteArrayMethod
from boa3.internal.model.variable import Variable


class ByteArrayEncodingMethod(ByteArrayMethod):

    def __init__(self):
        from boa3.internal.model.type.type import Type

        args: Dict[str, Variable] = {
            'object': Variable(Type.str),
            'encoding': Variable(Type.str)
        }
        super().__init__(args)

    @property
    def is_supported(self) -> bool:
        # TODO: change when building bytearray from string encoding
        return False

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> Optional[str]:
        return
