from __future__ import annotations

from typing import Any, Dict, Optional

from boa3.model.method import Method
from boa3.model.property import Property
from boa3.model.type.classes.classarraytype import ClassArrayType
from boa3.model.variable import Variable


class OracleType(ClassArrayType):
    """
    A class used to represent Oracle class
    """

    def __init__(self):
        super().__init__('Oracle')

        self._variables: Dict[str, Variable] = {}
        self._class_methods: Dict[str, Method] = {}
        self._constructor: Method = None

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
        from boa3.model.builtin.interop.oracle.oraclegetpricemethod import OracleGetPriceMethod
        from boa3.model.builtin.interop.oracle.oraclerequestmethod import OracleRequestMethod

        if len(self._class_methods) == 0:
            self._class_methods = {
                'get_price': OracleGetPriceMethod(),
                'request': OracleRequestMethod()
            }
        return self._class_methods

    @property
    def instance_methods(self) -> Dict[str, Method]:
        return {}

    def constructor_method(self) -> Optional[Method]:
        return self._constructor

    @classmethod
    def build(cls, value: Any = None) -> OracleType:
        if value is None or cls._is_type_of(value):
            return _Oracle

    @classmethod
    def _is_type_of(cls, value: Any):
        return isinstance(value, OracleType)


_Oracle = OracleType()
