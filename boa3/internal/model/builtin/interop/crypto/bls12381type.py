from typing import Any

from boa3.internal.model.builtin.interop.interopinterfacetype import InteropInterfaceType
from boa3.internal.model.method import Method
from boa3.internal.model.type.itype import IType


class Bls12381Type(InteropInterfaceType):
    """
    A class used to represent Neo BLS12_281 type
    """

    def __init__(self):
        super().__init__(identifier='IBls12381')
        self._constructor: Method = None

    @classmethod
    def build(cls, value: Any = None) -> IType:
        if value is None or cls._is_type_of(value):
            return _Bls12381

    @classmethod
    def _is_type_of(cls, value: Any):
        return isinstance(value, Bls12381Type)

    @property
    def class_variables(self):
        return {}

    @property
    def instance_variables(self):
        return {}

    @property
    def properties(self):
        return {}

    @property
    def static_methods(self):
        return {}

    @property
    def class_methods(self):
        return {}

    @property
    def instance_methods(self):
        return {}

    def constructor_method(self):
        return self._constructor


_Bls12381 = Bls12381Type()
