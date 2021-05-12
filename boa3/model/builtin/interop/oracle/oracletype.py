from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

from boa3.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.model.expression import IExpression
from boa3.model.method import Method
from boa3.model.property import Property
from boa3.model.type.classtype import ClassType
from boa3.model.variable import Variable
from boa3.neo.vm.opcode.Opcode import Opcode


class OracleType(ClassType):
    """
    A class used to represent Oracle class
    """

    def __init__(self):
        super().__init__('Oracle')

        self._variables: Dict[str, Variable] = {}
        self._class_methods: Dict[str, Method] = {}
        self._constructor: Method = None

    @property
    def variables(self) -> Dict[str, Variable]:
        return self._variables.copy()

    @property
    def properties(self) -> Dict[str, Property]:
        return {}

    @property
    def class_methods(self) -> Dict[str, Method]:
        # avoid recursive import
        from boa3.model.builtin.interop.oracle.oraclerequesmethod import OracleRequesMethod

        if len(self._class_methods) == 0:
            self._class_methods = {
                'request': OracleRequesMethod()
            }
        return self._class_methods

    @property
    def instance_methods(self) -> Dict[str, Method]:
        return {}

    def constructor_method(self) -> Optional[Method]:
        # was having a problem with recursive import
        if self._constructor is None:
            self._constructor: Method = OracleMethod(self)
        return self._constructor

    @classmethod
    def build(cls, value: Any = None) -> OracleType:
        if value is None or cls._is_type_of(value):
            return _Oracle

    @classmethod
    def _is_type_of(cls, value: Any):
        return isinstance(value, OracleType)


_Oracle = OracleType()


class OracleMethod(IBuiltinMethod):

    def __init__(self, return_type: OracleType):
        identifier = '-Oracle__init__'
        args: Dict[str, Variable] = {}
        super().__init__(identifier, args, return_type=return_type)

    def validate_parameters(self, *params: IExpression) -> bool:
        return len(params) == 0

    @property
    def opcode(self) -> List[Tuple[Opcode, bytes]]:
        return [
            (Opcode.NEWARRAY0, b'')
        ]

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> Optional[str]:
        return
