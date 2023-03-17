from typing import List

from boa3.internal.neo3.contracts.nef import MethodToken


class CompilerOutput:
    def __init__(self, bytecode: bytes, method_tokens: List[MethodToken] = None):
        self._bytecode = bytecode
        self._method_tokens = method_tokens if isinstance(method_tokens, list) else []

    @property
    def bytecode(self) -> bytes:
        return self._bytecode

    @property
    def method_tokens(self) -> List[MethodToken]:
        return self._method_tokens
