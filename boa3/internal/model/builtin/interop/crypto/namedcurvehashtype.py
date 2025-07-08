from typing import Any

from boa3.internal.model.builtin.method import IBuiltinMethod
from boa3.internal.model.expression import IExpression
from boa3.internal.model.method import Method
from boa3.internal.model.symbol import ISymbol
from boa3.internal.model.type.itype import IType
from boa3.internal.model.type.primitive.inttype import IntType
from boa3.internal.model.variable import Variable
from boa3.internal.neo3.contracts.namedcurvehash import NamedCurveHash


class NamedCurveHashType(IntType):
    """
    A class used to represent Neo NamedCurveHash type
    """

    def __init__(self):
        super().__init__()
        self._identifier = 'NamedCurveHash'

    @classmethod
    def build(cls, value: Any = None) -> IType:
        if value is None or cls._is_type_of(value):
            return _NamedCurve

    @classmethod
    def _is_type_of(cls, value: Any):
        return isinstance(value, (NamedCurveHash, NamedCurveHashType))

    @property
    def symbols(self) -> dict[str, ISymbol]:
        """
        Gets the class symbols of this type

        :return: a dictionary that maps each symbol in the module with its name
        """
        from boa3.internal.model.variable import Variable

        _symbols = super().symbols
        _symbols.update({name: Variable(self) for name in NamedCurveHash.__members__.keys()})

        return _symbols

    def get_value(self, symbol_id) -> Any:
        """
        Gets the literal value of a symbol

        :return: the value if this type has this symbol. None otherwise.
        """
        if symbol_id in self.symbols and symbol_id in NamedCurveHash.__members__:
            return NamedCurveHash.__members__[symbol_id]

        return None

    def constructor_method(self) -> Method | None:
        if self._constructor is None:
            self._constructor: Method = NamedCurveHashMethod(self)
        return self._constructor


_NamedCurve = NamedCurveHashType()


class NamedCurveHashMethod(IBuiltinMethod):

    def __init__(self, return_type: NamedCurveHashType):
        from boa3.internal.model.type.type import Type
        identifier = '-NamedCurveHash__init__'
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
