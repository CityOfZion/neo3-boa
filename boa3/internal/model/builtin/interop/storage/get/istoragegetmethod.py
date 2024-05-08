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


class IStorageGetMethod(InteropMethod, abc.ABC):

    def __init__(self, identifier: str, value_type: IType):
        from boa3.internal.model.type.type import Type
        from boa3.internal.model.builtin.interop.storage.storagecontext.storagecontexttype import StorageContextType

        syscall = 'System.Storage.Get'
        context_type = StorageContextType.build()

        args: dict[str, Variable] = {'key': Variable(Type.bytes),
                                     'context': Variable(context_type)}

        from boa3.internal.model.builtin.interop.storage.storagegetcontextmethod import StorageGetContextMethod
        default_id = StorageGetContextMethod(context_type).identifier
        context_default = set_internal_call(ast.parse(f"{default_id}()"
                                                      ).body[0].value)
        super().__init__(identifier, syscall, args, defaults=[context_default], return_type=value_type)

    @abc.abstractmethod
    def generate_default_value_opcodes(self, code_generator):
        pass

    @abc.abstractmethod
    def generate_deserialize_value_opcodes(self, code_generator):
        pass

    def generate_internal_opcodes(self, code_generator):
        super().generate_internal_opcodes(code_generator)
        # if result is None:
        code_generator.duplicate_stack_top_item()
        code_generator.insert_type_check(None)
        if_is_null = code_generator.convert_begin_if()

        #   result = default_value
        code_generator.remove_stack_top_item()
        self.generate_default_value_opcodes(code_generator)

        else_is_null = code_generator.convert_begin_else(if_is_null, is_internal=True)
        self.generate_deserialize_value_opcodes(code_generator)

        if else_is_null < code_generator.last_code_start_address:
            if_is_null = else_is_null
        code_generator.convert_end_if(if_is_null, is_internal=True)

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
        key_type: IType = exp[0].type
        if method.key_arg.type.is_type_of(key_type):
            return self
        else:
            from boa3.internal.model.builtin.interop.storage.get.storagegetbytesmethod import StorageGetBytesMethod
            method = StorageGetBytesMethod()
            method.args['key'] = Variable(key_type)
        return method
