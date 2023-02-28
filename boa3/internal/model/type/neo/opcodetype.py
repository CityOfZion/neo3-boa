from typing import Any, Dict

from boa3.internal.model.symbol import ISymbol
from boa3.internal.model.type.itype import IType
from boa3.internal.model.type.primitive.bytestype import BytesType


class OpcodeType(BytesType):
    """
    A class used to represent Neo interop Opcode type
    """

    def __init__(self):
        super().__init__()
        self._identifier = 'Opcode'

    @property
    def default_value(self) -> Any:
        from boa3.internal.neo.vm.opcode.Opcode import Opcode
        return Opcode.NOP

    @classmethod
    def build(cls, value: Any = None) -> IType:
        if value is None or cls._is_type_of(value):
            return _Opcode

    @classmethod
    def _is_type_of(cls, value: Any):
        from boa3.internal.neo.vm.opcode.Opcode import Opcode
        return isinstance(value, (Opcode, OpcodeType))

    @property
    def symbols(self) -> Dict[str, ISymbol]:
        """
        Gets the class symbols of this type

        :return: a dictionary that maps each symbol in the module with its name
        """
        from boa3.internal.neo.vm.opcode.Opcode import Opcode
        from boa3.internal.model.variable import Variable

        _symbols = super().symbols
        _symbols.update({name: Variable(self) for name in Opcode.__members__.keys()})

        return _symbols

    def get_value(self, symbol_id) -> Any:
        """
        Gets the literal value of a symbol

        :return: the value if this type has this symbol. None otherwise.
        """
        if symbol_id in self.symbols:
            from boa3.internal.neo.vm.opcode.Opcode import Opcode
            return Opcode.__members__[symbol_id]

        return None


_Opcode = OpcodeType()
