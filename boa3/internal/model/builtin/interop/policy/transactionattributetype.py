from typing import Any

from boa3.internal.model.builtin.method import IBuiltinMethod
from boa3.internal.model.expression import IExpression
from boa3.internal.model.method import Method
from boa3.internal.model.symbol import ISymbol
from boa3.internal.model.type.itype import IType
from boa3.internal.model.type.primitive.inttype import IntType
from boa3.internal.model.type.type import Type
from boa3.internal.model.variable import Variable
from boa3.internal.neo3.network.payloads.transactionattributetype import \
    TransactionAttributeType as TransactionAttribute


class TransactionAttributeType(IntType):
    """
    A class used to represent Neo TransactionAttributeType
    """

    def __init__(self):
        super().__init__()
        self._identifier = 'TransactionAttributeType'

    @classmethod
    def build(cls, value: Any) -> IType:
        if cls._is_type_of(value):
            from boa3.internal.model.builtin.interop.interop import Interop
            return Interop.TransactionAttributeType

    @classmethod
    def _is_type_of(cls, value: Any):
        return isinstance(value, (TransactionAttribute, TransactionAttributeType))

    @property
    def symbols(self) -> dict[str, ISymbol]:
        """
        Gets the class symbols of this type

        :return: a dictionary that maps each symbol in the module with its name
        """
        _symbols = super().symbols
        _symbols.update({name: Variable(self) for name in TransactionAttribute.__members__.keys()})

        return _symbols

    def get_value(self, symbol_id) -> Any:
        """
        Gets the literal value of a symbol

        :return: the value if this type has this symbol. None otherwise.
        """
        if symbol_id in self.symbols:
            return TransactionAttribute.__members__[symbol_id]

        return None

    def constructor_method(self) -> Method | None:
        if self._constructor is None:
            self._constructor: Method = TransactionAttributeMethod(self)
        return self._constructor


class TransactionAttributeMethod(IBuiltinMethod):

    def __init__(self, return_type: TransactionAttributeType):
        identifier = '-TransactionAttributeType__init__'
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
