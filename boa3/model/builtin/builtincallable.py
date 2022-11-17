import ast
from abc import ABC
from typing import Dict, List, Optional, Tuple

from boa3.model.callable import Callable
from boa3.model.identifiedsymbol import IdentifiedSymbol
from boa3.model.type.itype import IType
from boa3.model.variable import Variable
from boa3.neo.vm.opcode.Opcode import Opcode


class IBuiltinCallable(Callable, IdentifiedSymbol, ABC):
    def __init__(self, identifier: str, args: Dict[str, Variable] = None,
                 vararg: Optional[Tuple[str, Variable]] = None,
                 kwargs: Optional[Dict[str, Variable]] = None,
                 defaults: List[ast.AST] = None, return_type: IType = None):
        super().__init__(args, vararg, kwargs, defaults, return_type)
        self._identifier = identifier
        self._generated_opcode = None
        self.defined_by_entry = False  # every builtin symbol must have this variable set as False

    @property
    def opcode(self) -> List[Tuple[Opcode, bytes]]:
        """
        Gets the opcode for the method.

        :return: the opcode and its data if exists. None otherwise.
        """
        # don't need to recalculate for every time this property is called
        if self._generated_opcode is None:
            self._generated_opcode = self._opcode
        return self._generated_opcode

    def reset(self):
        # reset the opcodes to ensure the correct output when calling consecutive compilations
        self._generated_opcode = None
        self.reset_calls()

    @property
    def _opcode(self) -> List[Tuple[Opcode, bytes]]:
        return []

    @property
    def identifier(self) -> str:
        return self._identifier
