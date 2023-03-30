from typing import Dict

from boa3.internal.model.builtin.interop.interopmethod import InteropMethod
from boa3.internal.model.builtin.interop.storage.storagecontext.storagecontexttype import StorageContextType
from boa3.internal.model.variable import Variable


class StorageGetContextMethod(InteropMethod):

    def __init__(self, storage_context_type: StorageContextType):
        identifier = 'get_context'
        native_identifier = 'System.Storage.GetContext'
        args: Dict[str, Variable] = {}
        super().__init__(identifier, native_identifier, args, return_type=storage_context_type)
