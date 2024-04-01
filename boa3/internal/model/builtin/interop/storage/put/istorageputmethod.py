import abc
import ast
from collections.abc import Iterable, Sized
from typing import Any

from boa3.internal.model import set_internal_call
from boa3.internal.model.builtin.interop.interopmethod import InteropMethod
from boa3.internal.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.internal.model.expression import IExpression
from boa3.internal.model.type.itype import IType
from boa3.internal.model.variable import Variable


class IStoragePutMethod(InteropMethod, abc.ABC):

    def __init__(self, identifier: str, value_type: IType):
        from boa3.internal.model.type.type import Type
        from boa3.internal.model.builtin.interop.storage.storagecontext.storagecontexttype import StorageContextType

        syscall = 'System.Storage.Put'
        context_type = StorageContextType.build()

        args: dict[str, Variable] = {'key': Variable(Type.bytes),
                                     'value': Variable(value_type),
                                     'context': Variable(context_type)}

        from boa3.internal.model.builtin.interop.storage.storagegetcontextmethod import StorageGetContextMethod
        default_id = StorageGetContextMethod(context_type).identifier
        context_default = set_internal_call(ast.parse(f"{default_id}()"
                                                      ).body[0].value)
        super().__init__(identifier, syscall, args, defaults=[context_default], return_type=Type.none)

    @abc.abstractmethod
    def generate_serialize_value_opcodes(self, code_generator):
        pass

    def generate_internal_opcodes(self, code_generator):
        start_address = code_generator.bytecode_size
        code_generator.swap_reverse_stack_items(3)
        self.generate_serialize_value_opcodes(code_generator)
        end_address = code_generator.last_code_start_address

        if end_address > start_address:
            code_generator.swap_reverse_stack_items(3)
        else:
            code_generator._remove_inserted_opcodes_since(start_address)

        super().generate_internal_opcodes(code_generator)

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
    def key_arg(self) -> Variable:
        return self.args['key']

    @property
    def value_arg(self) -> Variable:
        return self.args['value']

    def build(self, value: Any) -> IBuiltinMethod:
        if not isinstance(value, (Sized, Iterable)):
            return self
        num_args: int = len(self.args)
        if len(value) != num_args or any(not isinstance(exp, (IExpression, IType)) for exp in value[:num_args]):
            return self

        exp = [exp if isinstance(exp, IExpression) else Variable(exp) for exp in value]
        if not self.validate_parameters(*exp):
            return self

        key_type: IType = exp[0].type
        value_type: IType = exp[1].type
        if self.key_arg.type.is_type_of(key_type) and self.value_arg.type.is_type_of(value_type):
            return self

        from boa3.internal.model.builtin.interop.storage.put.storageputintmethod import StoragePutBytesMethod
        method: InteropMethod = StoragePutBytesMethod()
        method.args['key'] = Variable(key_type)
        method.args['value'] = Variable(value_type)
        return method
