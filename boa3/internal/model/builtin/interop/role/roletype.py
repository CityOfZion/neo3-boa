from typing import Any, Dict

from boa3.internal.model.symbol import ISymbol
from boa3.internal.model.type.itype import IType
from boa3.internal.model.type.primitive.inttype import IntType


class RoleType(IntType):
    """
    A class used to represent Neo's Role type.
    """

    def __init__(self):
        super().__init__()
        self._identifier = 'Role'

    @classmethod
    def build(cls, value: Any = None) -> IType:
        if value is None or cls._is_type_of(value):
            return _Role

    @classmethod
    def _is_type_of(cls, value: Any):
        from boa3.builtin.interop.role.roletype import Role
        return isinstance(value, (Role, RoleType))

    @property
    def symbols(self) -> Dict[str, ISymbol]:
        """
        Gets the class symbols of this type.

        :return: a dictionary that maps each symbol in the module with its name
        """
        from boa3.builtin.interop.role.roletype import Role
        from boa3.internal.model.variable import Variable

        _symbols = super().symbols
        _symbols.update({name: Variable(self) for name in Role.__members__.keys()})

        return _symbols

    def get_value(self, symbol_id) -> Any:
        """
        Gets the literal value of a symbol.

        :return: the value if this type has this symbol. None otherwise
        """
        from boa3.builtin.interop.role.roletype import Role

        if symbol_id in self.symbols and symbol_id in Role.__members__:
            return Role.__members__[symbol_id]

        return None


_Role = RoleType()
