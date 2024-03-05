import ast
from collections.abc import Iterable, Sized
from typing import Any

from boa3.internal.model import set_internal_call
from boa3.internal.model.builtin.interop.interopmethod import InteropMethod
from boa3.internal.model.builtin.interop.storage import FindOptionsType
from boa3.internal.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.internal.model.expression import IExpression
from boa3.internal.model.type.itype import IType
from boa3.internal.model.variable import Variable


class StorageFindMethod(InteropMethod):

    def __init__(self, find_options_type: FindOptionsType, prefix_type: IType = None):
        from boa3.internal.model.type.type import Type
        from boa3.internal.model.builtin.interop.storage.storagecontext.storagecontexttype import StorageContextType

        identifier = 'find'
        syscall = 'System.Storage.Find'
        context_type = StorageContextType.build()

        if prefix_type is None:
            prefix_type = Type.bytes

        args: dict[str, Variable] = {'prefix': Variable(prefix_type),
                                     'context': Variable(context_type),
                                     'options': Variable(find_options_type)}

        from boa3.internal.model.builtin.interop.iterator import IteratorType
        return_type = IteratorType.build(Type.dict.build([prefix_type,  # return an Iterator[prefix, bytes]
                                                          Type.bytes]))

        from boa3.internal.model.builtin.interop.storage.storagegetcontextmethod import StorageGetContextMethod
        default_id = StorageGetContextMethod(context_type).identifier
        context_default = set_internal_call(ast.parse("{0}()".format(default_id)
                                                      ).body[0].value)
        options_default = set_internal_call(ast.parse("{0}.{1}".format(find_options_type.identifier,
                                                                       find_options_type.default_value.name)
                                                      ).body[0].value)

        defaults = [context_default, options_default]

        super().__init__(identifier, syscall, args, defaults=defaults, return_type=return_type)

    @property
    def identifier(self) -> str:
        return '-{0}_{1}'.format(self._identifier, self.prefix_arg.type.identifier)

    def validate_parameters(self, *params: IExpression) -> bool:
        if any(not isinstance(param, IExpression) for param in params):
            return False

        args: list[IType] = [arg.type for arg in self.args.values()]
        if len(params) > len(args):
            return False
        if len(params) < len(self.args_without_default):
            return False

        return self.prefix_arg.type.is_type_of(params[0].type)

    @property
    def generation_order(self) -> list[int]:
        """
        Gets the indexes order that need to be used during code generation.
        If the order for generation is the same as inputted in code, returns reversed(range(0,len_args))

        :return: Index order for code generation
        """
        indexes = super().generation_order
        context_index = list(self.args).index('context')

        if indexes[-1] != context_index:
            # context must be the last generated argument
            indexes.remove(context_index)
            indexes.append(context_index)

        return indexes

    @property
    def prefix_arg(self) -> Variable:
        return self.args['prefix']

    @property
    def options_arg(self) -> Variable:
        return self.args['options']

    def build(self, value: Any) -> IBuiltinMethod:
        exp: list[IExpression] = []
        if isinstance(value, Sized):
            if len(value) > 1 or not isinstance(value, Iterable):
                return self
            exp = [exp if isinstance(exp, IExpression) else Variable(exp)
                   for exp in value if isinstance(exp, (IExpression, IType))]

        elif isinstance(exp, (IExpression, IType)):
            exp = [value if isinstance(value, IExpression) else Variable(value)]
        else:
            return self

        if not self.validate_parameters(*exp):
            return self

        method = self
        prefix_type: IType = exp[0].type
        if type(method.prefix_arg.type) != type(prefix_type):
            method = StorageFindMethod(self.options_arg.type, prefix_type)
        return method
