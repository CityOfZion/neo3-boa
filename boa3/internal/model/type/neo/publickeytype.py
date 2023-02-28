from typing import Any

from boa3.internal.model.type.collection.sequence.ecpointtype import ECPointType
from boa3.internal.model.type.itype import IType


class PublicKeyType(ECPointType):
    """
    A class used to indicate that a parameter or return on the manifest is a PublicKey. It's a subclass of ECPointType.
    """

    def __init__(self):
        super().__init__()
        self._identifier = 'PublicKey'

    @classmethod
    def build(cls, value: Any = None) -> IType:
        return _PublicKey


_PublicKey = PublicKeyType()
