from abc import ABC, abstractmethod
from typing import Optional, Dict

from boa3.model.builtin.decorator.builtindecorator import IBuiltinDecorator
from boa3.model.type.itype import IType
from boa3.model.variable import Variable
from boa3.neo.vm.opcode.Opcode import Opcode


class IBuiltinMethod(IBuiltinDecorator, ABC):
    def __init__(self, identifier: str, args: Dict[str, Variable] = None, return_type: IType = None):
        self.identifier = identifier
        super().__init__(identifier, args, return_type)

    @property
    def opcode(self) -> Optional[Opcode]:
        """
        Gets the opcode for the method.

        :return: the opcode if exists. None otherwise.
        """
        return None

    @property
    def args_on_stack(self) -> int:
        """
        Gets the number of arguments that must be on stack before the opcode is called.

        :return: the number of arguments if opcode is not None. Zero otherwise.
        """
        if self.opcode is None:
            return 0
        else:
            num_args = self._args_on_stack
            if num_args < 0:
                return 0
            elif num_args > len(self.args):
                return len(self.args)
            return num_args

    @property
    @abstractmethod
    def _args_on_stack(self) -> int:
        """
        Gets the number of arguments that must be on stack before the opcode is called.

        :return: the number of arguments.
        """
        return 0

    @property
    def body(self) -> Optional[str]:
        """
        Gets the body of the method.

        :return: Return the code of the method body if there is no opcode. None otherwise.
        """
        if self.opcode is None:
            return self._body
        else:
            return None

    @property
    @abstractmethod
    def _body(self) -> Optional[str]:
        """
        Gets the body of the method.

        :return: Return the code of the method body.
        """
        return None
