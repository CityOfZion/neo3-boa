from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

from boa3.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.model.expression import IExpression
from boa3.model.method import Method
from boa3.model.property import Property
from boa3.model.type.classtype import ClassType
from boa3.model.variable import Variable
from boa3.neo.vm.opcode.Opcode import Opcode


class StorageContextType(ClassType):
    """
    A class used to represent Neo StorageContext class
    """

    def __init__(self):
        super().__init__('StorageContext')

        self._variables: Dict[str, Variable] = {}
        self._instance_methods: Dict[str, Method] = {}
        self._constructor: Method = None

    @property
    def variables(self) -> Dict[str, Variable]:
        return self._variables.copy()

    @property
    def properties(self) -> Dict[str, Property]:
        return {}

    @property
    def class_methods(self) -> Dict[str, Method]:
        return {}

    @property
    def instance_methods(self) -> Dict[str, Method]:
        # avoid recursive import
        if len(self._instance_methods) == 0:
            from boa3.model.builtin.interop.storage.storagecontext.storagecontextcreatemapmethod import \
                StorageContextCreateMapMethod

            self._instance_methods = {
                'create_map': StorageContextCreateMapMethod()
            }
        return self._instance_methods

    def constructor_method(self) -> Optional[Method]:
        # was having a problem with recursive import
        if self._constructor is None:
            self._constructor: Method = StorageContextMethod(self)
        return self._constructor

    @classmethod
    def build(cls, value: Any = None) -> StorageContextType:
        if value is None or cls._is_type_of(value):
            return _StorageContext

    @classmethod
    def _is_type_of(cls, value: Any):
        return isinstance(value, StorageContextType)


_StorageContext = StorageContextType()


class StorageContextMethod(IBuiltinMethod):

    def __init__(self, return_type: StorageContextType):
        identifier = '-StorageContext__init__'
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
