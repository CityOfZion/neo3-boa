from abc import ABC

from boa3.internal.model.type.classes.classtype import ClassType
from boa3.internal.neo.vm.type.AbiType import AbiType
from boa3.internal.neo.vm.type.StackItem import StackItemType


class ClassArrayType(ClassType, ABC):
    """
    An abstract class used to represent a Python class that is implemented internally using Neo Array type
    """

    @property
    def abi_type(self) -> AbiType:
        return AbiType.Array

    @property
    def stack_item(self) -> StackItemType:
        return StackItemType.Array
