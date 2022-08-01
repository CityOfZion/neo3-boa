from __future__ import annotations

from typing import Any, Dict, Optional

from boa3.model.method import Method
from boa3.model.property import Property
from boa3.model.type.classes.classarraytype import ClassArrayType
from boa3.model.variable import Variable


class CryptoLibClass(ClassArrayType):
    """
    A class used to represent CryptoLib native contract
    """

    def __init__(self):
        super().__init__('CryptoLib')

        self._variables: Dict[str, Variable] = {}
        self._class_methods: Dict[str, Method] = {}
        self._constructor: Optional[Method] = None

    @property
    def instance_variables(self) -> Dict[str, Variable]:
        return self._variables.copy()

    @property
    def class_variables(self) -> Dict[str, Variable]:
        return {}

    @property
    def properties(self) -> Dict[str, Property]:
        return {}

    @property
    def static_methods(self) -> Dict[str, Method]:
        return {}

    @property
    def class_methods(self) -> Dict[str, Method]:
        # avoid recursive import
        from boa3.model.builtin.interop.crypto import (Murmur32Method, Sha256Method, Ripemd160Method,
                                                       VerifyWithECDsaMethod)

        if len(self._class_methods) == 0:
            self._class_methods = {
                'murmur32': Murmur32Method(),
                'sha256': Sha256Method(),
                'ripemd160': Ripemd160Method(),
                'verify_with_ecdsa': VerifyWithECDsaMethod(),
            }
        return self._class_methods

    @property
    def instance_methods(self) -> Dict[str, Method]:
        return {}

    def constructor_method(self) -> Optional[Method]:
        return self._constructor

    @classmethod
    def build(cls, value: Any = None) -> CryptoLibClass:
        if value is None or cls._is_type_of(value):
            return _CryptoLib

    @classmethod
    def _is_type_of(cls, value: Any):
        return isinstance(value, CryptoLibClass)


_CryptoLib = CryptoLibClass()
