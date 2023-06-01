from __future__ import annotations

import ast
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple

from boa3.internal.model.builtin.builtincallable import IBuiltinCallable
from boa3.internal.model.method import Method
from boa3.internal.model.type.itype import IType
from boa3.internal.model.variable import Variable


class IBuiltinMethod(IBuiltinCallable, Method, ABC):
    def __init__(self, identifier: str, args: Dict[str, Variable] = None,
                 defaults: List[ast.AST] = None, return_type: IType = None,
                 vararg: Optional[Tuple[str, Variable]] = None,
                 kwargs: Optional[Dict[str, Variable]] = None):
        super().__init__(identifier, args, vararg, kwargs, defaults, return_type)

    @property
    def is_supported(self) -> bool:
        """
        Verifies if the builtin method is supported by the compiler

        :return: True if it is supported. False otherwise.
        """
        return True

    def not_supported_str(self, callable_id: str) -> str:
        return '{0}({1})'.format(callable_id,
                                 ','.join([arg.type.identifier for arg in self.args.values()]))

    @property
    def is_cast(self) -> bool:
        """
        Returns whether this method is for casting types
        """
        return False

    @property
    def cast_types(self) -> Optional[Tuple[IType, IType]]:
        """
        If `is_cast` is True, must return the original type and the target type of the cast.
        Otherwise, must return None
        """
        return None

    @property
    def args_on_stack(self) -> int:
        """
        Gets the number of arguments that must be on stack before the opcode is called.

        :return: the number of arguments if opcode is not empty. Zero otherwise.
        """
        if self.pack_arguments:
            return 1

        num_args = self._args_on_stack
        if num_args < 0:
            return 0
        elif num_args > len(self.args):
            return len(self.args)
        return num_args

    def push_self_first(self) -> bool:
        """
        Verifies if the `self` value of the method needs to be pushed to the Neo execution stack before the
        other arguments.

        :return: a boolean value indicating if the `self` argument must be pushed before. Returns False if there isn't
                 a `self` argument in the function
        """
        return False

    def validate_self(self, self_type: IType) -> bool:
        """
        Verifies if the given value is valid to the function `self` argument

        :param self_type: type of the value
        :return: a boolean value that represents if the value is valid. Returns False if there isn't a `self` argument
                 in the function
        """
        if not self.has_self_argument:
            return False
        return self.args['self'].type.is_type_of(self_type)

    @property
    def has_self_argument(self) -> bool:
        """
        Verifies if the function has a `self` argument.

        :return: True if there is this argument. False otherwise.
        """
        return 'self' in self.args

    @property
    @abstractmethod
    def _args_on_stack(self) -> int:
        """
        Gets the number of arguments that must be on stack before the opcode is called.

        :return: the number of arguments.
        """
        return 0

    @property
    def stores_on_slot(self) -> bool:
        """
        Returns whether this method needs to update the value from a variable

        :return: whether the method needs to update a variable
        """
        return False

    @property
    def requires_reordering(self) -> bool:
        """
        Returns whether this method requires a reordering of user inputted parameters

        :return: whether the method requires the parameters to be ordered differently as inputted from the user
        """
        return False

    def reorder(self, arguments: list):
        """
        Reorder the arguments if the method requires it.

        If `requires_reordering` returns True, this method must be implemented

        :param arguments: list of arguments to be reordered
        """
        pass

    @property
    def generation_order(self) -> List[int]:
        """
        Gets the indexes order that need to be used during code generation.
        If the order for generation is the same as inputted in code, returns reversed(range(0,len_args))

        :return: Index order for code generation
        """
        indexes = list(reversed(range(0, len(self.args))))
        if self.push_self_first():
            indexes.remove(0)     # remove the first index from whatever position it is
            indexes.insert(0, 0)  # and move to the first position

        return indexes

    def validate_negative_arguments(self) -> List[int]:
        """
        Returns a list of the arguments that have to be positive values and need validation.

        :return: list with the arguments indexes that need to be fixed.
        :rtype: List[int]
        """
        return []

    @property
    def pack_arguments(self) -> bool:
        """
        Return whether this method requires its parameters to be packed into an array

        :return: whether this method requires an array
        """
        return False

    def evaluate_literal(self, *args: Any) -> Any:
        """
        Tries to evaluate the result during compile time. If it cannot be evaluated, returns Undefined.

        :return: arguments to try to run the method
        :rtype: Any
        """
        from boa3.internal.analyser.model.optimizer import Undefined
        return Undefined

    @property
    def body(self) -> Optional[str]:
        """
        Gets the body of the method.

        :return: Return the code of the method body if there is no opcode. None otherwise.
        """
        return self._body if len(self.opcode) <= 0 else None

    @property
    @abstractmethod
    def _body(self) -> Optional[str]:
        """
        Gets the body of the method.

        :return: Return the code of the method body.
        """
        return None

    def build(self, value: Any) -> IBuiltinMethod:
        """
        Creates a method instance with the given value as self

        :param value: value to build the type
        :return: The built method if the value is valid. The current object otherwise
        :rtype: IBuiltinMethod
        """
        return self
