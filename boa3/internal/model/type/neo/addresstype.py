from typing import Any

from boa3.internal.model.type.itype import IType
from boa3.internal.model.type.primitive.strtype import StrType


class AddressType(StrType):
    """
    A class used to indicate that a parameter or return on the manifest is an Address. It's a subclass of StrType.
    """

    def __init__(self):
        super().__init__()
        self._identifier = 'Address'

    @classmethod
    def build(cls, value: Any = None) -> IType:
        return _Address


_Address = AddressType()
