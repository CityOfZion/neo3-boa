from typing import List

from boa3.model.builtin.interopmethod.interopmethod import InteropMethod
from boa3.model.builtin.interopmethod.runtime.checkwitnessmethod import CheckWitnessMethod
from boa3.model.builtin.interopmethod.runtime.notifymethod import NotifyMethod
from boa3.model.builtin.interopmethod.storage.storagegetmethod import StorageGetMethod
from boa3.model.builtin.interopmethod.storage.storageputmethod import StoragePutMethod


class Interop:

    @classmethod
    def interop_methods(cls) -> List[InteropMethod]:
        return [interop for interop in vars(cls).values() if isinstance(interop, InteropMethod)]

    # Runtime Interops
    CheckWitness = CheckWitnessMethod()
    Notify = NotifyMethod()

    # Storage Interops
    StorageGet = StorageGetMethod()
    StoragePut = StoragePutMethod()
