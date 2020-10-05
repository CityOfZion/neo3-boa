from enum import Enum
from typing import Dict, List

from boa3.model.builtin.interop.contract.callmethod import CallMethod
from boa3.model.builtin.interop.contract.getgasscripthashmethod import GasProperty
from boa3.model.builtin.interop.contract.getneoscripthashmethod import NeoProperty
from boa3.model.builtin.interop.runtime.checkwitnessmethod import CheckWitnessMethod
from boa3.model.builtin.interop.runtime.getblocktimemethod import BlockTimeProperty
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
    Contract = 'contract'
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

    # Contract Interops
    CallContract = CallMethod()
    NeoScriptHash = NeoProperty()
    GasScriptHash = GasProperty()

    # Runtime Interops
    CheckWitness = CheckWitnessMethod()
    Notify = NotifyMethod()
    Log = LogMethod()
    TriggerType = TriggerTyping()
    GetTrigger = TriggerMethod(TriggerType)
    CallingScriptHash = CallingScriptHashProperty()
    BlockTime = BlockTimeProperty()

    # Storage Interops
    StorageGet = StorageGetMethod()
    StoragePut = StoragePutMethod()
    StorageDelete = StorageDeleteMethod()

    _interop_symbols: Dict[InteropPackage, List[IdentifiedSymbol]] = {
        InteropPackage.Contract: [CallContract,
                                  NeoScriptHash,
                                  GasScriptHash
                                  ],
        InteropPackage.Runtime: [CheckWitness,
                                 Notify,
                                 Log,
                                 TriggerType,
                                 GetTrigger,
                                 CallingScriptHash,
                                 BlockTime
                                 ],
        InteropPackage.Storage: [StorageGet,
                                 StoragePut,
                                 StorageDelete
                                 ]
    }
