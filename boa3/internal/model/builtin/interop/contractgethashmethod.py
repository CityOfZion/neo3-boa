import ast
from abc import ABC

from boa3.internal.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.internal.model.type.itype import IType
from boa3.internal.model.variable import Variable


class ContractGetHashMethod(IBuiltinMethod, ABC):
    def __init__(self, script_hash: bytes, identifier: str, args: dict[str, Variable] = None,
                 defaults: list[ast.AST] = None, return_type: IType = None,
                 vararg: tuple[str, Variable] | None = None,
                 kwargs: dict[str, Variable] | None = None):
        self._script_hash = script_hash
        super().__init__(identifier, args, defaults, return_type, vararg, kwargs)

    @property
    def script_hash(self) -> bytes:
        return self._script_hash

    def generate_internal_opcodes(self, code_generator):
        code_generator.convert_literal(self.script_hash)
