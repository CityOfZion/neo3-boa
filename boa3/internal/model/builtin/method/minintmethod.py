from typing import Optional

from boa3.internal.model.builtin.method.minmethod import MinMethod
from boa3.internal.model.type.itype import IType


class MinIntMethod(MinMethod):

    def __init__(self, arg_value: Optional[IType] = None):
        from boa3.internal.model.type.type import Type
        super().__init__(arg_value if Type.int.is_type_of(arg_value) else Type.int)
