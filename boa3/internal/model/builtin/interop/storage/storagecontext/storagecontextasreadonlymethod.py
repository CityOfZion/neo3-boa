from boa3.internal.model.builtin.interop.interopmethod import InteropMethod
from boa3.internal.model.variable import Variable


class StorageContextAsReadOnlyMethod(InteropMethod):

    def __init__(self):
        from boa3.internal.model.builtin.interop.storage.storagecontext.storagecontexttype import _StorageContext

        identifier = 'as_read_only'
        syscall = 'System.Storage.AsReadOnly'
        args: dict[str, Variable] = {'self': Variable(_StorageContext)}
        super().__init__(identifier, syscall, args, return_type=_StorageContext)
