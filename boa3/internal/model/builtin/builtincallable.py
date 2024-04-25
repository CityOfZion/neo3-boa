import ast
from abc import ABC

from boa3.internal.model.builtin.builtinsymbol import IBuiltinSymbol
from boa3.internal.model.callable import Callable
from boa3.internal.model.type.itype import IType
from boa3.internal.model.variable import Variable
from boa3.internal.neo.vm.opcode.Opcode import Opcode


class IBuiltinCallable(Callable, IBuiltinSymbol, ABC):
    def __init__(self,
                 identifier: str,
                 args: dict[str, Variable] = None,
                 vararg: tuple[str, Variable] | None = None,
                 kwargs: dict[str, Variable] | None = None,
                 defaults: list[ast.AST] = None,
                 return_type: IType = None,
                 deprecated: bool = False,
                 new_location: str = None
                 ):
        super().__init__(args, vararg, kwargs, defaults, return_type, deprecated=deprecated)
        self._identifier = identifier
        self._generated_opcode = None
        self._new_location = new_location
        self.defined_by_entry = False  # every builtin symbol must have this variable set as False

    @property
    def new_location(self) -> str | None:
        return self._new_location

    def set_new_location(self, new_location: str, identifier: str = None):
        """
        Set the location that is going to be shown in the deprecation warning in case if this symbol is deprecated.
        """
        from boa3.internal import constants
        if identifier is None or len(identifier.strip()) == 0:
            identifier = self._identifier

        self._new_location = constants.ATTRIBUTE_NAME_SEPARATOR.join((new_location, identifier))

    @property
    def opcode(self) -> list[tuple[Opcode, bytes]]:
        """
        Gets the opcode for the method.

        :return: the opcode and its data if exists. None otherwise.
        """
        # don't need to recalculate for every time this property is called
        if self._generated_opcode is None:
            self._generated_opcode = self._opcode
        return self._generated_opcode

    def generate_opcodes(self, code_generator):
        """
        Generate the Neo VM opcodes for the method.

        :type code_generator: boa3.internal.compiler.codegenerator.codegenerator.CodeGenerator
        """
        self.generate_internal_opcodes(code_generator)

    def generate_internal_opcodes(self, code_generator):
        """
        Generate the Neo VM opcodes for the method.

        :type code_generator: boa3.internal.compiler.codegenerator.codegenerator.CodeGenerator
        """
        pass

    def reset(self):
        # reset the opcodes to ensure the correct output when calling consecutive compilations
        self._generated_opcode = None
        self.reset_calls()

    @property
    def _opcode(self) -> list[tuple[Opcode, bytes]]:
        return []

    @property
    def identifier(self) -> str:
        return self._identifier
