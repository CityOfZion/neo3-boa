from typing import Any, Self

from boa3.internal.model.builtin.method import IBuiltinMethod
from boa3.internal.model.expression import IExpression
from boa3.internal.model.method import Method
from boa3.internal.model.symbol import ISymbol
from boa3.internal.model.type.primitive.inttype import IntType
from boa3.internal.model.type.type import Type
from boa3.internal.model.variable import Variable
from boa3.internal.neo3.network.payloads.verification import WitnessRuleAction


class WitnessRuleActionType(IntType):
    """
    A class used to represent Neo interop WitnessRuleAction type
    """

    def __init__(self):
        super().__init__()
        self._identifier = 'WitnessRuleAction'

    @property
    def default_value(self) -> Any:
        return WitnessRuleAction.DENY

    @classmethod
    def build(cls, value: Any = None) -> Self:
        if value is None or cls._is_type_of(value):
            return _WitnessRuleAction

    @classmethod
    def _is_type_of(cls, value: Any = None):
        return isinstance(value, (WitnessRuleAction, WitnessRuleActionType))

    @property
    def symbols(self) -> dict[str, ISymbol]:
        """
        Gets the class symbols of this type

        :return: a dictionary that maps each symbol in the module with its name
        """
        _symbols = super().symbols
        _symbols.update({name: Variable(self) for name in WitnessRuleAction.__members__.keys()})

        return _symbols

    def get_value(self, symbol_id) -> Any:
        """
        Gets the literal value of a symbol

        :return: the value if this type has this symbol. None otherwise.
        """
        if symbol_id in self.symbols:
            return WitnessRuleAction.__members__[symbol_id]

        return None

    def constructor_method(self) -> Method | None:
        if self._constructor is None:
            self._constructor: Method = WitnessRuleActionMethod(self)
        return self._constructor


_WitnessRuleAction = WitnessRuleActionType()


class WitnessRuleActionMethod(IBuiltinMethod):

    def __init__(self, return_type: WitnessRuleActionType):
        identifier = '-WitnessRuleAction__init__'
        args: dict[str, Variable] = {
            'x': Variable(Type.int)
        }
        super().__init__(identifier, args, return_type=return_type)

    def validate_parameters(self, *params: IExpression) -> bool:
        return len(params) == 1

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> str | None:
        return None
