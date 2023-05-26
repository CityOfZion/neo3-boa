from typing import Any

from boa3.internal.model.type.classes.pythonclass import PythonClass
from boa3.internal.model.type.itype import IType
from boa3.internal.neo.vm.type.AbiType import AbiType


class NoneType(PythonClass):
    """
    A class used to represent Python None value
    """

    def __init__(self):
        identifier = 'none'
        super().__init__(identifier)

    @property
    def abi_type(self) -> AbiType:
        return AbiType.Void

    @classmethod
    def build(cls, value: Any) -> IType:
        if cls._is_type_of(value):
            from boa3.internal.model.type.type import Type
            return Type.none

    @classmethod
    def _is_type_of(cls, value: Any):
        from boa3.internal.model.type.type import Type
        return value is None or value is Type.none

    def generate_is_instance_type_check(self, code_generator):
        code_generator.insert_type_check(None)


noneType: IType = NoneType()
