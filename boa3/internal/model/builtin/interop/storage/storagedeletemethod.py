from collections.abc import Iterable, Sized
from typing import Any

from boa3.internal.model.builtin.interop.interopmethod import InteropMethod
from boa3.internal.model.builtin.interop.storage.neostorageinterop import NeoStorageInterop, StorageContextDelete, \
    StorageLocalDelete
from boa3.internal.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.internal.model.expression import IExpression
from boa3.internal.model.type.itype import IType
from boa3.internal.model.variable import Variable


class StorageDeleteMethod(InteropMethod):

    def __init__(self, storage_interop: NeoStorageInterop = None):
        from boa3.internal.model.type.type import Type

        if storage_interop is None:
            self._storage_interop = StorageContextDelete()
        else:
            self._storage_interop = storage_interop

        identifier = 'delete'
        syscall = self._storage_interop.syscall_name()
        args, defaults = self._storage_interop.args_default()
        super().__init__(identifier, syscall, args, defaults=defaults, return_type=Type.none)

    @property
    def identifier(self) -> str:
        return self._storage_interop.new_identifier(self._identifier, self.key_arg.type.identifier)

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
    def key_arg(self) -> Variable:
        return self.args['key']

    def build(self, value: Any) -> IBuiltinMethod:
        exp: list[IExpression] = []
        if isinstance(value, Sized):
            if len(value) > 2 or not isinstance(value, Iterable):
                return self
            exp = [exp if isinstance(exp, IExpression) else Variable(exp)
                   for exp in value if isinstance(exp, (IExpression, IType))]

        method = self
        key_type: IType = exp[0].type
        if len(exp) == 1:
            return StorageDeleteMethod(StorageLocalDelete())
        if not method.key_arg.type.is_type_of(key_type):
            method = StorageDeleteMethod()
            method.args['key'] = Variable(key_type)
        return method
