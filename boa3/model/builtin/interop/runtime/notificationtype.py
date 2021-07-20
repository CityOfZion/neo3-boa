from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

from boa3.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.model.expression import IExpression
from boa3.model.method import Method
from boa3.model.property import Property
from boa3.model.type.classes.classarraytype import ClassArrayType
from boa3.model.type.collection.sequence.uint160type import UInt160Type
from boa3.model.variable import Variable
from boa3.neo.vm.opcode.Opcode import Opcode


class NotificationType(ClassArrayType):
    """
    A class used to represent Neo Notification class
    """

    def __init__(self):
        super().__init__('Notification')

        from boa3.model.type.type import Type
        self._variables: Dict[str, Variable] = {
            'script_hash': Variable(UInt160Type.build()),
            'event_name': Variable(Type.str),
            'state': Variable(Type.tuple)
        }
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
        return {}

    @property
    def instance_methods(self) -> Dict[str, Method]:
        return {}

    def constructor_method(self) -> Optional[Method]:
        # was having a problem with recursive import
        if self._constructor is None:
            self._constructor: Method = NotificationMethod(self)
        return self._constructor

    @classmethod
    def build(cls, value: Any = None) -> NotificationType:
        if value is None or cls._is_type_of(value):
            return _Notification

    @classmethod
    def _is_type_of(cls, value: Any):
        return isinstance(value, NotificationType)


_Notification = NotificationType()


class NotificationMethod(IBuiltinMethod):

    def __init__(self, return_type: NotificationType):
        identifier = '-Notification__init__'
        args: Dict[str, Variable] = {}
        super().__init__(identifier, args, return_type=return_type)

    def validate_parameters(self, *params: IExpression) -> bool:
        return len(params) == 0

    @property
    def opcode(self) -> List[Tuple[Opcode, bytes]]:
        from boa3.neo.vm.type.Integer import Integer
        return [
            (Opcode.NEWARRAY0, b''),
            (Opcode.PUSHDATA1, Integer(0).to_byte_array()),
            (Opcode.PUSHDATA1, Integer(20).to_byte_array() + bytes(20)),
            (Opcode.PUSH3, b''),
            (Opcode.PACK, b'')
        ]

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> Optional[str]:
        return
