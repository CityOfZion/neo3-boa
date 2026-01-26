import abc
import ast

from boa3.internal.model import set_internal_call
from boa3.internal.model.builtin.interop.storage.storagecontext.storagecontexttype import StorageContextType
from boa3.internal.model.builtin.interop.storage.storagegetcontextmethod import StorageGetContextMethod
from boa3.internal.model.type.itype import IType
from boa3.internal.model.type.type import Type
from boa3.internal.model.variable import Variable


class NeoStorageInterop(abc.ABC):
    """
    An abstract class used to differentiate Local and not Local Neo Storage interop syscalls
    """
    LOCAL_SUFFIX = 'local'
    CONTEXT_SUFFIX = 'with_context'

    @abc.abstractmethod
    def syscall_name(self) -> str:
        pass

    @abc.abstractmethod
    def args_default(self, *arg_types: IType) -> tuple[dict[str, Variable], list[ast.AST] | None]:
        pass

    @abc.abstractmethod
    def change_generation_order(self, indexes_list: list, args: dict[str, Variable]) -> list[int]:
        pass

    @abc.abstractmethod
    def new_identifier(self, identifier_: str, arg_type: str) -> str:
        pass


class StorageContextGet(NeoStorageInterop):
    def syscall_name(self) -> str:
        return 'System.Storage.Get'

    def args_default(self, *arg_types: IType) -> tuple[dict[str, Variable], list[ast.AST] | None]:
        context_type = StorageContextType.build()

        args: dict[str, Variable] = {'key': Variable(Type.bytes),
                                     'context': Variable(context_type)}
        default_id = StorageGetContextMethod(context_type).identifier
        context_default = set_internal_call(ast.parse(f"{default_id}()"
                                                      ).body[0].value)

        return args, [context_default]

    def change_generation_order(self, indexes_list: list, args: dict[str, Variable]) -> list[int]:
        context_index = list(args).index('context')

        if indexes_list[-1] != context_index:
            # context must be the last generated argument
            indexes_list.remove(context_index)
            indexes_list.append(context_index)

        return indexes_list

    def new_identifier(self, identifier_: str, arg_type: str) -> str:
        return '-{0}_{1}_{2}'.format(identifier_, arg_type, NeoStorageInterop.CONTEXT_SUFFIX)


class StorageLocalGet(NeoStorageInterop):
    def syscall_name(self) -> str:
        return 'System.Storage.Local.Get'

    def args_default(self, *arg_types: IType) -> tuple[dict[str, Variable], list[ast.AST] | None]:
        args: dict[str, Variable] = {'key': Variable(Type.bytes)}
        return args, None

    def change_generation_order(self, indexes_list: list, args: dict[str, Variable]) -> list[int]:
        return indexes_list

    def new_identifier(self, identifier_: str, arg_type: str) -> str:
        return '-{0}_{1}_{2}'.format(identifier_, arg_type, NeoStorageInterop.LOCAL_SUFFIX)


class StorageContextPut(NeoStorageInterop):
    def syscall_name(self) -> str:
        return 'System.Storage.Put'

    def args_default(self, *arg_types: IType) -> tuple[dict[str, Variable], list[ast.AST] | None]:
        context_type = StorageContextType.build()
        value_type = arg_types[0]

        args: dict[str, Variable] = {'key': Variable(Type.bytes),
                                     'value': Variable(value_type),
                                     'context': Variable(context_type)}
        default_id = StorageGetContextMethod(context_type).identifier
        context_default = set_internal_call(ast.parse(f"{default_id}()"
                                                      ).body[0].value)

        return args, [context_default]

    def change_generation_order(self, indexes_list: list, args: dict[str, Variable]) -> list[int]:
        context_index = list(args).index('context')

        if indexes_list[-1] != context_index:
            # context must be the last generated argument
            indexes_list.remove(context_index)
            indexes_list.append(context_index)

        return indexes_list

    def new_identifier(self, identifier_: str, arg_type: str) -> str:
        return '-{0}_{1}_{2}'.format(identifier_, arg_type, NeoStorageInterop.CONTEXT_SUFFIX)


class StorageLocalPut(NeoStorageInterop):
    def syscall_name(self) -> str:
        return 'System.Storage.Local.Put'

    def args_default(self, *arg_types: IType) -> tuple[dict[str, Variable], list[ast.AST] | None]:
        value_type = arg_types[0]
        args: dict[str, Variable] = {'key': Variable(Type.bytes),
                                     'value': Variable(value_type)}
        return args, None

    def change_generation_order(self, indexes_list: list, args: dict[str, Variable]) -> list[int]:
        return indexes_list

    def new_identifier(self, identifier_: str, arg_type: str) -> str:
        return '-{0}_{1}_{2}'.format(identifier_, arg_type, NeoStorageInterop.LOCAL_SUFFIX)


class StorageContextFind(NeoStorageInterop):
    def syscall_name(self) -> str:
        return 'System.Storage.Find'

    def args_default(self, *arg_types: IType) -> tuple[dict[str, Variable], list[ast.AST] | None]:
        context_type = StorageContextType.build()
        prefix_type = arg_types[0]
        find_options_type = arg_types[1]

        args: dict[str, Variable] = {'prefix': Variable(prefix_type),
                                     'context': Variable(context_type),
                                     'options': Variable(find_options_type)}

        default_id = StorageGetContextMethod(context_type).identifier
        context_default = set_internal_call(ast.parse("{0}()".format(default_id)
                                                      ).body[0].value)
        options_default = set_internal_call(ast.parse("{0}.{1}".format(find_options_type.identifier,
                                                                       find_options_type.default_value.name)
                                                      ).body[0].value)

        defaults = [context_default, options_default]

        return args, defaults

    def change_generation_order(self, indexes_list: list, args: dict[str, Variable]) -> list[int]:
        context_index = list(args).index('context')

        if indexes_list[-1] != context_index:
            # context must be the last generated argument
            indexes_list.remove(context_index)
            indexes_list.append(context_index)

        return indexes_list

    def new_identifier(self, identifier_: str, arg_type: str) -> str:
        return '-{0}_{1}_{2}'.format(identifier_, arg_type, NeoStorageInterop.CONTEXT_SUFFIX)


class StorageLocalFind(NeoStorageInterop):
    def syscall_name(self) -> str:
        return 'System.Storage.Local.Find'

    def args_default(self, *arg_types: IType) -> tuple[dict[str, Variable], list[ast.AST] | None]:
        prefix_type = arg_types[0]
        find_options_type = arg_types[1]

        args: dict[str, Variable] = {'prefix': Variable(prefix_type),
                                     'options': Variable(find_options_type)}

        options_default = set_internal_call(ast.parse("{0}.{1}".format(find_options_type.identifier,
                                                                       find_options_type.default_value.name)
                                                      ).body[0].value)

        defaults = [options_default]
        return args, defaults

    def change_generation_order(self, indexes_list: list, args: dict[str, Variable]) -> list[int]:
        return indexes_list

    def new_identifier(self, identifier_: str, arg_type: str) -> str:
        return '-{0}_{1}_{2}'.format(identifier_, arg_type, NeoStorageInterop.LOCAL_SUFFIX)


class StorageContextDelete(NeoStorageInterop):
    def syscall_name(self) -> str:
        return 'System.Storage.Delete'

    def args_default(self, *arg_types: IType) -> tuple[dict[str, Variable], list[ast.AST] | None]:
        context_type = StorageContextType.build()

        args: dict[str, Variable] = {'key': Variable(Type.bytes),
                                     'context': Variable(context_type)}
        default_id = StorageGetContextMethod(context_type).identifier
        context_default = set_internal_call(ast.parse("{0}()".format(default_id)
                                                      ).body[0].value)
        return args, [context_default]

    def change_generation_order(self, indexes_list: list, args: dict[str, Variable]) -> list[int]:
        context_index = list(args).index('context')

        if indexes_list[-1] != context_index:
            # context must be the last generated argument
            indexes_list.remove(context_index)
            indexes_list.append(context_index)

        return indexes_list

    def new_identifier(self, identifier_: str, arg_type: str) -> str:
        return '-{0}_{1}_{2}'.format(identifier_, arg_type, NeoStorageInterop.CONTEXT_SUFFIX)


class StorageLocalDelete(NeoStorageInterop):
    def syscall_name(self) -> str:
        return 'System.Storage.Local.Delete'

    def args_default(self, *arg_types: IType) -> tuple[dict[str, Variable], list[ast.AST] | None]:
        args: dict[str, Variable] = {'key': Variable(Type.bytes)}
        return args, None

    def change_generation_order(self, indexes_list: list, args: dict[str, Variable]) -> list[int]:
        return indexes_list

    def new_identifier(self, identifier_: str, arg_type: str) -> str:
        return '-{0}_{1}_{2}'.format(identifier_, arg_type, NeoStorageInterop.LOCAL_SUFFIX)
