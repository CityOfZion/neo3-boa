from typing import Any, Self

from boa3.internal.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.internal.model.expression import IExpression
from boa3.internal.model.method import Method
from boa3.internal.model.property import Property
from boa3.internal.model.type.classes.classarraytype import ClassArrayType
from boa3.internal.model.type.collection.sequence.uint160type import UInt160Type
from boa3.internal.model.variable import Variable


class NotificationType(ClassArrayType):
    """
    A class used to represent Neo Notification class
    """

    def __init__(self):
        super().__init__('Notification')

        from boa3.internal.model.type.type import Type
        self._variables: dict[str, Variable] = {
            'script_hash': Variable(UInt160Type.build()),
            'event_name': Variable(Type.str),
            'state': Variable(Type.tuple)
        }
        self._constructor: Method = None

    @property
    def instance_variables(self) -> dict[str, Variable]:
        return self._variables.copy()

    @property
    def class_variables(self) -> dict[str, Variable]:
        return {}

    @property
    def properties(self) -> dict[str, Property]:
        return {}

    @property
    def static_methods(self) -> dict[str, Method]:
        return {}

    @property
    def class_methods(self) -> dict[str, Method]:
        return {}

    @property
    def instance_methods(self) -> dict[str, Method]:
        return {}

    def constructor_method(self) -> Method | None:
        # was having a problem with recursive import
        if self._constructor is None:
            self._constructor: Method = NotificationMethod(self)
        return self._constructor

    @classmethod
    def build(cls, value: Any = None) -> Self:
        if value is None or cls._is_type_of(value):
            return _Notification

    @classmethod
    def _is_type_of(cls, value: Any):
        return isinstance(value, NotificationType)


_Notification = NotificationType()


class NotificationMethod(IBuiltinMethod):

    def __init__(self, return_type: NotificationType):
        identifier = '-Notification__init__'
        args: dict[str, Variable] = {}
        super().__init__(identifier, args, return_type=return_type)

    def validate_parameters(self, *params: IExpression) -> bool:
        return len(params) == 0

    def generate_internal_opcodes(self, code_generator):
        from boa3.internal.neo3.core.types import UInt160

        uint160_default = UInt160.zero().to_array()

        code_generator.convert_literal(())  # state
        code_generator.convert_literal('')  # event_name
        code_generator.convert_literal(uint160_default)  # script_hash
        code_generator.convert_new_array(length=3, array_type=self.type)

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> str | None:
        return
