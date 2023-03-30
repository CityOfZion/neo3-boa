import ast
from abc import ABC
from typing import Dict, List, Tuple

from boa3.internal.model.builtin.method.builtinevent import IBuiltinEvent
from boa3.internal.model.variable import Variable
from boa3.internal.neo.vm.opcode.Opcode import Opcode


class InteropEvent(IBuiltinEvent, ABC):

    def __init__(self, identifier: str, sys_call: str,
                 args: Dict[str, Variable] = None, defaults: List[ast.AST] = None):
        self._sys_call: str = sys_call
        super().__init__(identifier, args, defaults)

    @property
    def interop_method_hash(self) -> bytes:
        return self._method_hash(self._sys_call)

    def _method_hash(self, method_name: str) -> bytes:
        from boa3.internal.constants import SIZE_OF_INT32
        from boa3.internal.neo import cryptography
        from boa3.internal.neo.vm.type.String import String

        return cryptography.sha256(String(method_name).to_bytes())[:SIZE_OF_INT32]

    @property
    def _opcode(self) -> List[Tuple[Opcode, bytes]]:
        return [(Opcode.SYSCALL, self.interop_method_hash)]
