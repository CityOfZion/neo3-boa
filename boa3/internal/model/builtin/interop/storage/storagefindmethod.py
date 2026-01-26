from collections.abc import Iterable, Sized
from typing import Any

from boa3.internal.model.builtin.interop.interopmethod import InteropMethod
from boa3.internal.model.builtin.interop.iterator import IteratorType
from boa3.internal.model.builtin.interop.storage import FindOptionsType
from boa3.internal.model.builtin.interop.storage.neostorageinterop import NeoStorageInterop, StorageContextFind, \
    StorageLocalFind
from boa3.internal.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.internal.model.expression import IExpression
from boa3.internal.model.type.itype import IType
from boa3.internal.model.type.type import Type
from boa3.internal.model.variable import Variable


class StorageFindMethod(InteropMethod):

    def __init__(self, find_options_type: FindOptionsType, prefix_type: IType = None,
                 storage_interop: NeoStorageInterop = None):

        if storage_interop is None:
            self._storage_interop = StorageContextFind()
        else:
            self._storage_interop = storage_interop

        identifier = 'find'
        syscall = self._storage_interop.syscall_name()

        if prefix_type is None:
            prefix_type = Type.bytes

        return_type = IteratorType.build(Type.dict.build([prefix_type,  # return an Iterator[prefix, bytes]
                                                          Type.bytes]))

        args, defaults = self._storage_interop.args_default(prefix_type, find_options_type)

        super().__init__(identifier, syscall, args, defaults=defaults, return_type=return_type)

    @property
    def identifier(self) -> str:
        return self._storage_interop.new_identifier(self._identifier, self.prefix_arg.type.identifier)

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

        return self._storage_interop.change_generation_order(indexes, self.args)

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

        if not self.validate_parameters(*exp):
            return self

        method = self
        prefix_type: IType = exp[0].type
        if len(exp) == 1:
            return StorageFindMethod(self.options_arg.type, prefix_type, StorageLocalFind())
        if type(method.prefix_arg.type) != type(prefix_type):
            method = StorageFindMethod(self.options_arg.type, prefix_type)
        return method
