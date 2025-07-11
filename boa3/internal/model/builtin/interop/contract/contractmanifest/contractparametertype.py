from typing import Any

from boa3.internal.model.builtin.method import IBuiltinMethod
from boa3.internal.model.expression import IExpression
from boa3.internal.model.method import Method
from boa3.internal.model.symbol import ISymbol
from boa3.internal.model.type.itype import IType
from boa3.internal.model.type.primitive.inttype import IntType
from boa3.internal.model.type.type import Type
from boa3.internal.model.variable import Variable
from boa3.internal.neo.vm.type.ContractParameterType import ContractParameterType as ContractParameter


class ContractParameterType(IntType):
    """
    A class used to represent Neo interop ContractParameterType type
    """

    def __init__(self):
        super().__init__()
        self._identifier = 'ContractParameterType'

    @property
    def default_value(self) -> Any:
        return ContractParameter.ALL

    @classmethod
    def build(cls, value: Any = None) -> IType:
        if value is None or cls._is_type_of(value):
            return _ContractParameterType

    @classmethod
    def _is_type_of(cls, value: Any):
        return isinstance(value, (ContractParameter, ContractParameterType))

    @property
    def symbols(self) -> dict[str, ISymbol]:
        """
        Gets the class symbols of this type

        :return: a dictionary that maps each symbol in the module with its name
        """
        _symbols = super().symbols
        _symbols.update({name: Variable(self) for name in ContractParameter.__members__.keys()})

        return _symbols

    def get_value(self, symbol_id) -> Any:
        """
        Gets the literal value of a symbol

        :return: the value if this type has this symbol. None otherwise.
        """
        if symbol_id in self.symbols and symbol_id in ContractParameter.__members__:
            return ContractParameter.__members__[symbol_id]

        return None

    def constructor_method(self) -> Method | None:
        if self._constructor is None:
            self._constructor: Method = ContractParameterTypeMethod(self)
        return self._constructor


_ContractParameterType = ContractParameterType()


class ContractParameterTypeMethod(IBuiltinMethod):

    def __init__(self, return_type: ContractParameterType):
        identifier = '-ContractParameterType__init__'
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
