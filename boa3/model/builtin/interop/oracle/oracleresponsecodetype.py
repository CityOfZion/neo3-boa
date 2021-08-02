from typing import Any, Dict

from boa3.model.symbol import ISymbol
from boa3.model.type.itype import IType
from boa3.model.type.primitive.inttype import IntType


class OracleResponseCodeType(IntType):
    """
    A class used to represent Neo's OracleResponseCode.
    """

    def __init__(self):
        super().__init__()
        self._identifier = 'OracleResponseCode'

    @classmethod
    def build(cls, value: Any = None) -> IType:
        if value is None or cls._is_type_of(value):
            return _OracleResponseCode

    @classmethod
    def _is_type_of(cls, value: Any):
        from boa3.builtin.interop.oracle.oracleresponsecode import OracleResponseCode
        return isinstance(value, (OracleResponseCode, OracleResponseCodeType))

    @property
    def symbols(self) -> Dict[str, ISymbol]:
        """
        Gets the class symbols of this type.

        :return: a dictionary that maps each symbol in the module with its name
        """
        from boa3.builtin.interop.role.roletype import Role
        from boa3.model.variable import Variable

        return {name: Variable(self) for name in Role.__members__.keys()}

    def get_value(self, symbol_id) -> Any:
        """
        Gets the literal value of a symbol.

        :return: the value if this type has this symbol. None otherwise
        """
        if symbol_id in self.symbols:
            from boa3.builtin.interop.oracle.oracleresponsecode import OracleResponseCode
            return OracleResponseCode.__members__[symbol_id]

        return None


_OracleResponseCode = OracleResponseCodeType()
