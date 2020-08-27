import ast
from abc import ABC
from typing import Dict, List, Tuple

from boa3.model.callable import Callable
from boa3.model.identifiedsymbol import IdentifiedSymbol
from boa3.model.type.itype import IType
from boa3.model.variable import Variable
from boa3.neo.vm.opcode.Opcode import Opcode


class IBuiltinCallable(Callable, IdentifiedSymbol, ABC):
    def __init__(self, identifier: str, args: Dict[str, Variable] = None,
                 defaults: List[ast.AST] = None, return_type: IType = None):
        super().__init__(args, defaults, return_type)
        self._identifier = identifier

    @property
    def opcode(self) -> List[Tuple[Opcode, bytes]]:
        """
        Gets the opcode for the method.

        :return: the opcode and its data if exists. None otherwise.
        """
        return []

    @property
    def identifier(self) -> str:
        return self._identifier
