from typing import Any

from boa3.internal.model.type.itype import IType


class EllipsisType(IType):
    """
    A class used to represent Python Ellipsis (...) annotation
    """

    def __init__(self):
        identifier = 'Ellipsis'
        super().__init__(identifier)

    @classmethod
    def build(cls, value: Any) -> IType:
        return ellipsisType

    @classmethod
    def _is_type_of(cls, value: Any):
        return value is Ellipsis or value is ellipsisType

    def union_type(self, other_type: IType) -> IType:
        return other_type

    def intersect_type(self, other_type: IType) -> IType:
        from boa3.internal.model.type.type import Type
        return Type.none


ellipsisType: IType = EllipsisType()
