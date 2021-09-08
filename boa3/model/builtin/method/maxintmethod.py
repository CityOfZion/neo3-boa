from typing import Optional

from boa3.model.builtin.method.maxmethod import MaxMethod
from boa3.model.type.itype import IType


class MaxIntMethod(MaxMethod):

    def __init__(self, arg_value: Optional[IType] = None):
        from boa3.model.type.type import Type
        super().__init__(arg_value if Type.int.is_type_of(arg_value) else Type.int)
