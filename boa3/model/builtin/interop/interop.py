from enum import Enum
from typing import List, Dict

from boa3.model.builtin.interop.runtime.checkwitnessmethod import CheckWitnessMethod
from boa3.model.builtin.interop.runtime.getcallingscripthashmethod import CallingScriptHashProperty
from boa3.model.builtin.interop.runtime.logmethod import LogMethod
from boa3.model.builtin.interop.runtime.notifymethod import NotifyMethod
from boa3.model.builtin.interop.runtime.triggermethod import TriggerMethod
from boa3.model.builtin.interop.runtime.triggertype import TriggerType as TriggerTyping
from boa3.model.builtin.interop.storage.storagedeletemethod import StorageDeleteMethod
from boa3.model.builtin.interop.storage.storagegetmethod import StorageGetMethod
from boa3.model.builtin.interop.storage.storageputmethod import StoragePutMethod
from boa3.model.identifiedsymbol import IdentifiedSymbol


class InteropPackage(str, Enum):
    Runtime = 'runtime'
    Storage = 'storage'


class Interop:

    @classmethod
    def interop_symbols(cls, package: str = None) -> List[IdentifiedSymbol]:
        if package in InteropPackage.__members__.values():
            return cls._interop_symbols[package]

        lst: List[IdentifiedSymbol] = []
        for symbols in cls._interop_symbols.values():
            lst.extend(symbols)
        return lst

    # Runtime Interops
    CheckWitness = CheckWitnessMethod()
    Notify = NotifyMethod()
    Log = LogMethod()
    TriggerType = TriggerTyping()
    GetTrigger = TriggerMethod(TriggerType)
    CallingScriptHash = CallingScriptHashProperty()

    # Storage Interops
    StorageGet = StorageGetMethod()
    StoragePut = StoragePutMethod()
    StorageDelete = StorageDeleteMethod()

    _interop_symbols: Dict[InteropPackage, List[IdentifiedSymbol]] = {
        InteropPackage.Runtime: [CheckWitness,
                                 Notify,
                                 Log,
                                 TriggerType,
                                 GetTrigger,
                                 CallingScriptHash
                                 ],
        InteropPackage.Storage: [StorageGet,
                                 StoragePut,
                                 StorageDelete
                                 ]
    }
