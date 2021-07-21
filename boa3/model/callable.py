from __future__ import annotations

import ast
from abc import ABC
from typing import Dict, List, Optional, Tuple

from boa3.model import set_internal_call
from boa3.model.expression import IExpression
from boa3.model.type.type import IType, Type
from boa3.model.variable import Variable
from boa3.neo.vm.VMCode import VMCode


class Callable(IExpression, ABC):
    """
    A class used to represent a function or a class method

    :ivar args: a dictionary that maps each arg with its name. Empty by default.
    :ivar is_public: a boolean value that specifies if the method is public. False by default.
    :ivar return_type: the return type of the method. None by default.
    """

    def __init__(self, args: Dict[str, Variable] = None,
                 vararg: Optional[Tuple[str, Variable]] = None,
                 defaults: List[ast.AST] = None,
                 return_type: IType = Type.none, is_public: bool = False,
                 decorators: List[Callable] = None,
                 origin_node: Optional[ast.AST] = None):

        if args is None:
            args = {}
        self.args: Dict[str, Variable] = args.copy()

        if not isinstance(defaults, list):
            defaults = []
        self.defaults: List[ast.AST] = defaults

        self._vararg: Optional[Tuple[str, Variable]] = None
        if (isinstance(vararg, tuple) and len(vararg) == 2
                and isinstance(vararg[0], str) and isinstance(vararg[1], Variable)):

            from boa3.model.type.typeutils import TypeUtils

            vararg_id, vararg_var = vararg
            if vararg_var.type is not Type.any:
                default_code = "{0}({1}, {2})".format(TypeUtils.cast.raw_identifier,
                                                      Type.tuple.build_collection(vararg_var.type),
                                                      Type.tuple.default_value)
            else:
                default_code = "{0}".format(Type.tuple.default_value)

            default_value = set_internal_call(ast.parse(default_code).body[0].value)

            self.args[vararg_id] = Variable(Type.tuple.build_collection([vararg_var.type]))
            self.defaults.append(default_value)
            self._vararg = vararg

        self.return_type: IType = return_type
        self.is_public: bool = is_public

        if decorators is None:
            decorators = []
        from boa3.model.decorator import IDecorator
        self.decorators: List[IDecorator] = [decorator for decorator in decorators
                                             if isinstance(decorator, IDecorator)]

        super().__init__(origin_node)

        self.init_address: Optional[int] = None
        self.init_bytecode: Optional[VMCode] = None
        self.init_defaults_bytecode: Optional[VMCode] = None
        self.end_bytecode: Optional[VMCode] = None

    @property
    def type(self) -> IType:
        return self.return_type

    @property
    def symbols(self) -> Dict[str, Variable]:
        """
        Gets all the symbols in the method

        :return: a dictionary that maps each symbol in the module with its name
        """
        return self.args.copy()

    @property
    def args_without_default(self) -> Dict[str, Variable]:
        num_defaults = len(self.defaults)
        if num_defaults > 0:
            return {key: self.args[key] for key in list(self.args.keys())[:-num_defaults]}
        return self.args

    @property
    def has_cls_or_self(self) -> bool:
        return any(decorator.has_cls_or_self for decorator in self.decorators)

    @property
    def has_starred_argument(self) -> bool:
        return self._vararg is not None

    @property
    def start_address(self) -> Optional[int]:
        """
        Gets the address where this method starts in the bytecode

        :return: the first address of the method
        """
        if self.init_bytecode is None and self.init_defaults_bytecode is None:
            return self.init_address
        else:
            from boa3.compiler.codegenerator.vmcodemapping import VMCodeMapping
            return VMCodeMapping.instance().get_start_address(self.init_bytecode)

    @property
    def start_bytecode(self) -> Optional[VMCode]:
        return (self.init_defaults_bytecode if len(self.defaults) > 0
                else self.init_bytecode)

    @property
    def end_address(self) -> Optional[int]:
        """
        Gets the address of this method's last operation in the bytecode

        :return: the last address of the method
        """
        if self.end_bytecode is None:
            return self.start_address
        else:
            from boa3.compiler.codegenerator.vmcodemapping import VMCodeMapping
            return VMCodeMapping.instance().get_end_address(self.end_bytecode)

    def __str__(self) -> str:
        args_types: List[str] = [str(arg.type) for arg in self.args.values()]
        if self.return_type is not Type.none:
            signature = '({0}) -> {1}'.format(', '.join(args_types), self.return_type)
        else:
            signature = '({0})'.format(', '.join(args_types))
        public = 'public ' if self.is_public else ''
        return '{0}{1}'.format(public, signature)
