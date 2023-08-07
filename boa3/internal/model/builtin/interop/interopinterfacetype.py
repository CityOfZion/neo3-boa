from abc import ABC

from boa3.internal.model.type.classes.classtype import ClassType
from boa3.internal.neo.vm.type.AbiType import AbiType
from boa3.internal.neo.vm.type.StackItem import StackItemType


class InteropInterfaceType(ClassType, ABC):
    """
    An abstract class used to represent a Python class that is implemented internally as a Neo Interop Interface
    """

    @property
    def stack_item(self) -> StackItemType:
        return StackItemType.InteropInterface

    @property
    def abi_type(self) -> AbiType:
        return AbiType.InteropInterface

    def generate_is_instance_type_check(self, code_generator):
        """
        Generates the opcodes to check if a value is of this type

        :type code_generator: boa3.internal.compiler.codegenerator.codegenerator.CodeGenerator
        """
        super(ClassType, self).generate_is_instance_type_check(code_generator)
