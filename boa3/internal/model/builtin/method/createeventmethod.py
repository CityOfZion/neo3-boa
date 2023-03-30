from typing import Any, Optional

from boa3.internal.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.internal.model.expression import IExpression
from boa3.internal.model.type.itype import IType
from boa3.internal.model.variable import Variable
from boa3.internal.neo.vm.type.AbiType import AbiType


class CreateEventMethod(IBuiltinMethod):
    def __init__(self):
        import ast
        from boa3.internal.model.type.type import Type
        identifier = 'CreateNewEvent'
        args = {
            'arguments': Variable(Type.list.build(Type.tuple)),
            'event_name': Variable(Type.str)
        }
        event_name_default = ast.parse("'{0}'".format(Type.str.default_value)
                                       ).body[0].value
        super().__init__(identifier, args, defaults=[event_name_default], return_type=EventType)

    def validate_parameters(self, *params: IExpression) -> bool:
        return len(params) == len(self.args)

    @property
    def _args_on_stack(self) -> int:
        return 0

    @property
    def _body(self) -> Optional[str]:
        return None


class __EventType(IType):
    """
    A class used to represent an Neo event
    """

    def __init__(self):
        identifier = 'Event'
        super().__init__(identifier)

    @property
    def abi_type(self) -> AbiType:
        return AbiType.Void

    @classmethod
    def build(cls, value: Any) -> IType:
        return EventType

    @classmethod
    def _is_type_of(cls, value: Any):
        return value is EventType


EventType = __EventType()
