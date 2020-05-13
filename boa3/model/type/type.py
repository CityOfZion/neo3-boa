from typing import Dict

from boa3.model.type.bool import Bool
from boa3.model.type.int import Int
from boa3.model.type.itype import IType
from boa3.model.type.none import NoneType
from boa3.model.type.str import Str


class Type:
    @classmethod
    def values(cls) -> Dict[str, IType]:
        value_dict = {}
        for type in vars(cls).values():
            if isinstance(type, IType):
                value_dict[type.identifier] = type
        return value_dict

    # Primitive Types
    int = Int()
    bool = Bool()
    str = Str()
    none = NoneType()
