from typing import Optional

from boa3.internal.model.builtin.classmethod.copymethod import CopyMethod
from boa3.internal.model.type.itype import IType


class CopyListMethod(CopyMethod):

    def __init__(self, arg_value: Optional[IType] = None):
        from boa3.internal.model.type.type import Type
        super().__init__(arg_value if Type.list.is_type_of(arg_value) else Type.list)
