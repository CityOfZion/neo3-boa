from boa3.internal.model.builtin.interop.interopmethod import InteropMethod
from boa3.internal.model.builtin.interop.storage.storagecontext.storagecontexttype import StorageContextType
from boa3.internal.model.variable import Variable


class StorageGetReadOnlyContextMethod(InteropMethod):

    def __init__(self, storage_context_type: StorageContextType):
        identifier = 'get_read_only_context'
        native_identifier = 'System.Storage.GetContext'
        args: dict[str, Variable] = {}
        super().__init__(identifier, native_identifier, args, return_type=storage_context_type)
