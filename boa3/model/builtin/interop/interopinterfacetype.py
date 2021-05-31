from abc import ABC

from boa3.model.type.classtype import ClassType
from boa3.neo.vm.type.AbiType import AbiType
from boa3.neo.vm.type.StackItem import StackItemType


class InteropInterfaceType(ClassType, ABC):

    @property
    def stack_item(self) -> StackItemType:
        return StackItemType.InteropInterface

    @property
    def abi_type(self) -> AbiType:
        return AbiType.InteropInterface
