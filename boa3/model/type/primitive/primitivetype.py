from abc import ABC

from boa3.model.type.itype import IType


class PrimitiveType(IType, ABC):
    """
    An interface for primitive types
    """

    def __init__(self, identifier: str):
        super().__init__(identifier)
