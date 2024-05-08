import ast
from abc import ABC
from typing import Self

from boa3.internal.model import set_internal_call
from boa3.internal.model.expression import IExpression
from boa3.internal.model.type.type import IType, Type
from boa3.internal.model.variable import Variable
from boa3.internal.neo.vm.VMCode import VMCode


class Callable(IExpression, ABC):
    """
    A class used to represent a function or a class method

    :ivar args: a dictionary that maps each arg with its name. Empty by default.
    :ivar is_public: a boolean value that specifies if the method is public. False by default.
    :ivar return_type: the return type of the method. None by default.
    """

    def __init__(self,
                 args: dict[str, Variable] = None,
                 vararg: tuple[str, Variable] | None = None,
                 kwargs: dict[str, Variable] | None = None,
                 defaults: list[ast.AST] = None,
                 return_type: IType = Type.none, is_public: bool = False,
                 decorators: list[Self] = None,
                 external_name: str = None,
                 is_safe: bool = False,
                 origin_node: ast.AST | None = None,
                 deprecated: bool = False
                 ):

        if args is None:
            args = {}
        self.args: dict[str, Variable] = args.copy()

        if not isinstance(defaults, list):
            defaults = []
        self.defaults: list[ast.AST] = defaults

        self._vararg: tuple[str, Variable] | None = None
        if (isinstance(vararg, tuple) and len(vararg) == 2
                and isinstance(vararg[0], str) and isinstance(vararg[1], Variable)):

            from boa3.internal.model.type.typeutils import TypeUtils

            vararg_id, vararg_var = vararg
            if vararg_var.type is not Type.any:
                default_code = "{0}({1}, {2})".format(TypeUtils.cast.raw_identifier,
                                                      Type.tuple.build_collection(vararg_var.type),
                                                      Type.tuple.default_value)
            else:
                default_code = "{0}".format(Type.tuple.default_value)

            default_value = set_internal_call(ast.parse(default_code).body[0].value)

            self.args[vararg_id] = Variable(Type.tuple.build_any_length(vararg_var.type))
            self.defaults.append(default_value)
            self._vararg = vararg

        if kwargs is None:
            kwargs = {}
        self._kwargs: dict[str, Variable] = kwargs.copy()

        self.return_type: IType = return_type

        if decorators is None:
            decorators = []
        from boa3.internal.model.decorator import IDecorator
        self.decorators: list[IDecorator] = [decorator for decorator in decorators
                                             if isinstance(decorator, IDecorator)]

        from boa3.internal.model.builtin.decorator import PublicDecorator
        public_decorator = next((decorator for decorator in self.decorators
                                 if isinstance(decorator, PublicDecorator)),
                                None)

        self.is_public: bool = is_public or public_decorator is not None
        if self.is_public:
            if isinstance(public_decorator, PublicDecorator):
                external_name = public_decorator.name
            elif self.defined_by_entry:
                external_name = None

        self.external_name: str | None = external_name
        self.is_safe: bool = is_safe or (isinstance(public_decorator, PublicDecorator) and public_decorator.safe)

        self._self_calls: set[ast.AST] = set()

        super().__init__(origin_node, deprecated)

        self.init_address: int | None = None
        self.init_bytecode: VMCode | None = None
        self.init_defaults_bytecode: VMCode | None = None
        self.end_bytecode: VMCode | None = None

    @property
    def type(self) -> IType:
        return self.return_type

    @property
    def symbols(self) -> dict[str, Variable]:
        """
        Gets all the symbols in the method

        :return: a dictionary that maps each symbol in the module with its name
        """
        return self.args.copy()

    @property
    def args_without_default(self) -> dict[str, Variable]:
        num_defaults = len(self.defaults)
        if num_defaults > 0:
            return {key: self.args[key] for key in list(self.args.keys())[:-num_defaults]}
        return self.args

    @property
    def positional_args(self) -> dict[str, Variable]:
        return {key: value for key, value in self.args.items() if key not in self._kwargs}

    @property
    def has_cls_or_self(self) -> bool:
        return any(decorator.has_cls_or_self for decorator in self.decorators)

    @property
    def cls_or_self_type(self) -> IType | None:
        if not self.has_cls_or_self or len(self.args) == 0:
            return None

        return list(self.args.values())[0].type

    @property
    def has_starred_argument(self) -> bool:
        return self._vararg is not None

    @property
    def start_address(self) -> int | None:
        """
        Gets the address where this method starts in the bytecode

        :return: the first address of the method
        """
        if self.init_bytecode is None and self.init_defaults_bytecode is None:
            return self.init_address
        else:
            from boa3.internal.compiler.codegenerator.vmcodemapping import VMCodeMapping
            return VMCodeMapping.instance().get_start_address(self.init_bytecode)

    @property
    def start_bytecode(self) -> VMCode | None:
        return (self.init_defaults_bytecode if len(self.defaults) > 0
                else self.init_bytecode)

    @property
    def end_address(self) -> int | None:
        """
        Gets the address of this method's last operation in the bytecode

        :return: the last address of the method
        """
        if self.end_bytecode is None:
            return self.start_address
        else:
            from boa3.internal.compiler.codegenerator.vmcodemapping import VMCodeMapping
            return VMCodeMapping.instance().get_end_address(self.end_bytecode)

    @property
    def is_called(self) -> bool:
        return len(self._self_calls) > 0

    def reset_calls(self):
        self._self_calls.clear()

    @property
    def is_compiled(self) -> bool:
        return self.start_address is not None and self.end_address is not None

    def add_call_origin(self, origin: ast.AST) -> bool:
        try:
            self._self_calls.add(origin)
            return True
        except BaseException:
            return False

    def __str__(self) -> str:
        args_types: list[str] = [str(arg.type) for arg in self.args.values()]
        if self.return_type is not Type.none:
            signature = '({0}) -> {1}'.format(', '.join(args_types), self.return_type)
        else:
            signature = '({0})'.format(', '.join(args_types))
        public = 'public ' if self.is_public else ''
        return '{0}{1}'.format(public, signature)

    def __repr__(self) -> str:
        name = self.identifier if hasattr(self, 'identifier') else self.__class__.__name__
        return f'{name}{str(self)}'
